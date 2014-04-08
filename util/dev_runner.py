import os, dmon, bottle

os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
bottle.run(host='localhost', port=8001)
