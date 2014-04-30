#!/usr/bin/env python

import datetime
import subprocess
import pymongo
import config

# Database config
client = pymongo.MongoClient(config.db_connection_string)
db = client.dmon

def update_ping(host):
    ping_command = 'ping -c 5 -i 6 %s' % host
    # Run the ping command in a shell
    proc = subprocess.Popen(ping_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    
    if err:
        print 'Error', err

        ping_data = {
            'timestamp': datetime.datetime.utcnow(),
            'loss': 100
        }

        db.ping.insert(ping_data)
        db.ping.remove({'timestamp': {'$lt': ping_data['timestamp'] - datetime.timedelta(days=30)}})
    else:
        ping_data = {
            'timestamp': datetime.datetime.utcnow()
        }
        lines = out.split('\n')
        
        for line in lines:
            if 'packet loss' in line:
                # Hack: parse comma-separated fields; get the one before the last,
                # and fetch the number without the percent sign
                ping_data['loss'] = float(line.split(', ')[-2].split()[0][:-1])
            if 'avg' in line:
                ping_data['rtt'] = float(line.split()[3].split('/')[1])
    
        db.ping.insert(ping_data)
        db.ping.remove({'timestamp': {'$lt': ping_data['timestamp'] - datetime.timedelta(days=30)}})

        
def check_service(name, addr):
    '''Checks if a host is listening on a port using nmap'''
    host, port = addr
    nmap_command = 'nmap -T4 %s -p %d --host-timeout 2s' % addr

    proc = subprocess.Popen(nmap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    
    if err:
        print 'Error', err
    else:
        nmap_data = {
            'timestamp': datetime.datetime.utcnow(),
            'service': name,
            'online': False
        }
        lines = out.split('\n')
        
        for line in lines:
            if '%d/' % (port) in line and 'open' in line:
                nmap_data['online'] = True

        db.servicemon.insert(nmap_data)
        
if __name__ == '__main__':
    db.servicemon.remove()  # Clear previous entries in case a service is removed
    for service, addr in config.services:
        check_service(service, addr)
        
    update_ping(config.ping_host)
