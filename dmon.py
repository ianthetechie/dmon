import os

import pymongo

import json
import datetime as dt
import config

from bson import json_util
from bottle import *


BaseTemplate.defaults['base_url'] = config.base_url

# JSON datetime helper
class JSONDefaultPlugin(JSONPlugin):
    def __init__(self):
        super(JSONDefaultPlugin, self).__init__()
        self.plain_dump = self.json_dumps
        self.json_dumps = lambda body: self.plain_dump(body, default=json_util.default)
        

# Database config
client = pymongo.MongoClient(config.db_connection_string)
db = client.dmon


def timestamp_newer_than(delta):
    return {'timestamp': {'$gt': dt.datetime.utcnow() - delta}}


def get_ping_averages_newer_than(delta):
    avg = {
        '$group': {
            '_id': 0,
            'avg_rtt': {'$avg': '$rtt'},
            'avg_loss': {'$avg': '$loss'},
        }
    }
    
    try:
        result = db.ping.aggregate([
            {'$match': timestamp_newer_than(delta)},
            avg
        ])['result'][0]
    except:
        result = {
            'avg_rtt': -1,
            'avg_loss': 0
        }
        
    return {
        'rtt': result['avg_rtt'],
        'loss': result['avg_loss']
    }


def get_ping_data():
    timeframes = [
        ('1m', dt.timedelta(minutes=1)),
        ('5m', dt.timedelta(minutes=5)),
        ('1h', dt.timedelta(hours=1)),
        ('4h', dt.timedelta(hours=4)),
        ('8h', dt.timedelta(hours=8)),
        ('1d', dt.timedelta(days=1)),
        ('7d', dt.timedelta(days=7)),
        ('30d', dt.timedelta(days=30))]
    
    data = {k: get_ping_averages_newer_than(v) for k,v in timeframes}
    return ([label for label, delta in timeframes], data)


def get_server_status():
    data = [(str(rec['service'].decode('utf-8')), 1 if rec['online'] else 0) for rec in db.servicemon.find()]
    return ([rec[0] for rec in data], dict(data))


@route('/css/<filename:re:.*\.css>')
def get_css(filename):
    css_dir = os.path.join(os.path.dirname(__file__), 'css')
    return static_file(filename, root=css_dir, mimetype='text/css')


@route('/js/<filename:re:.*\.js>')
def get_js(filename):
    js_dir = os.path.join(os.path.dirname(__file__), 'js')
    return static_file(filename, root=js_dir, mimetype='application/javascript')


@route('/<filename:re:.\*.txt>')
def get_server_text(filename):
    root_dir = os.path.dirname(__file__)
    return static_file(filename, root=root_dir, mimetype='text/plain')
    

@route('/')
@view('index')
def index():
    timeframes, ping_data = get_ping_data()
    services, server_data = get_server_status()
    
    return {
        'page_title': config.page_title,
        'page_heading': config.page_heading,
        'page_subheading': config.page_subheading if hasattr(config, 'page_subheading') else None,
        'timeframes': timeframes,
        'current_ping': ping_data,
        'services': services,
        'server_data': server_data
    }


@route('/ping')
def ping():
    return get_ping_data()[1]


@route('/server_status')
def server_status():
    return get_server_status()[1]

install(JSONDefaultPlugin())
