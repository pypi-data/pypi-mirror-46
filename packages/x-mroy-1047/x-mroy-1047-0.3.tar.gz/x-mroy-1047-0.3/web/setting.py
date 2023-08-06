

## write by qingluan
# this is a config file
# include db and debug , static path
import os
from os import path
# here to load all controllers
from qlib.file import ensure_path
from Qtornado.log import LogControl
from Qtornado.db import *
from web.controller import *
from qlib.data import Cache
# load ui modules
import web.ui as ui
import sys
import geoip2.database
from .test_route import DB_PATH
# db engine
# db_engine = pymongo.Connection()['local']
db_connect_cmd = r'database="' + DB_PATH + '"'
db_engine = Cache(DB_PATH,check_same_thread=False)


# static path
rdir_path = os.path.dirname(__file__)
static_path = os.path.join(rdir_path, "static")
files_path = os.path.join(static_path, "files")
geo_path = os.path.join(static_path, "res/geo")
D = os.path.dirname(DB_PATH)
shadowsocks_path = os.path.join(D, "shadowsocks")
ss_saved = "/tmp/ss-random"
ss_proxy = '/tmp/ss-proxy.conf'

ensure_path(static_path)
ensure_path(files_path)
ensure_path(shadowsocks_path)
ensure_path(ss_saved)

def get_ip(ip):
    reader = geoip2.database.Reader(os.path.join(geo_path, "GeoLite2-City.mmdb"))
    res = reader.city(ip)
    return str(res.location.longitude), str(res.location.latitude)

# set log level
LogControl.LOG_LEVEL |= LogControl.OK
LogControl.LOG_LEVEL |= LogControl.INFO
Settings = {
        'db':db_engine,
        'L': LogControl,
        'debug':True,
        'geo': get_ip,
        "ui_modules": ui,
        "ss-saved":ss_saved,
        'proxy-config-file.conf':ss_proxy,
        'autoreload':True,
        'cookie_secret':'This string can be any thing you want',
        'static_path' : static_path,
    }


## follow is router
appication = tornado.web.Application([
                (r'/',IndexHandler),
                # add some new route to router
                (r'/map', MapHandler),
		(r'/get_ip',Get_ipHandler),
		(r'/getstatus',GetStatusHandler),
		(r'/remoteapi',RemoteapiHandler),
		(r'/asyncremoteapi',AsyncremoteapiHandler),
		(r'/create',CreateHandler),
        (r'/out', AuthLogoutHandler),
        (r'/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan', LoginHandler),
        (r'/reg', RegHandler),
#<route></route>
                # (r'/main',MainHandler),
         ],**Settings)


# setting port
port = 8080
