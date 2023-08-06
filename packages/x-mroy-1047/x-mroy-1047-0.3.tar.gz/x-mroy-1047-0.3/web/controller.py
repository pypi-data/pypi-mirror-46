
## this is write by qingluan
# just a inti handler
# and a tempalte offer to coder
import os
import re
import json
import time
import random
import tornado
import tornado.web
import functools
import asyncio
import aiofiles
import concurrent
from base64 import b64encode
from tornado.websocket import WebSocketHandler
from qlib.data import dbobj,Cache
from qlib.log import L
from qlib.net import to
from enuma_elish.book import Book

#from seed.mrpackage.config import Host
#from seed.mrpackage.services import Bitter
from .vultr import Controll, destroy_one, update_db, create_one
from concurrent.futures.thread import ThreadPoolExecutor
from ashares.remote import AsyncConnection
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import Process
background_task_pocket =  ThreadPoolExecutor(max_workers=10)
# background_task_pocket_p = ProcessPoolExecutor(3)

class Host(dbobj):pass
class ErrHost(dbobj):pass

async def run_background(func, callback, *args,loop=None, **kwds):
    if not loop:
        tloop = tornado.ioloop.IOLoop.instance()
    future = await loop.run_in_executor(background_task_pocket, func, *args, **kwds)
    print(future)
    return  callback(future)
#    future = background_task_pocket.submit(func, *args, **kwds)
#    future.add_done_callback(_callback)


async def back_request(url, callback,method='get', headers=None, data=None, loop=None, proxy=None):
    if headers:
        T = functools.partial(to, headers=headers)
    if data:
        T = functools.partial(T, data=data)
    if method:
        T = functools.partial(T, method=method)
    if proxy:
        T = functools.partial(T, proxy=proxy)
    return await run_background(T, callback, url, loop=loop)


class GeoMap(dbobj):pass
class Reg(dbobj):pass
class Token(dbobj):pass
class Mark(dbobj):pass
class User(dbobj):pass

class MyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    tloop = tornado.ioloop.IOLoop.instance()
    def get_event_loop(self):
        """Get the event loop.

        This may be None or an instance of EventLoop.
        """
        # loop = super().get_event_loop()
        
        # Do something with loop ...
        return MyEventLoopPolicy.tloop

async def RefreshStatus():
    loop = asyncio.get_event_loop()
    tasks = {}
    DB_PATH = os.path.expanduser("~/.config/seed/cache.db")
    db = Cache(DB_PATH,check_same_thread=False)
    st = time.time()
    for host in db.query(Host):
        a = AsyncConnection(host=host.host, port=int(host.port), password=host.passwd,name=host.user, keyfile=None)
        a.timeout_t = 30
        tasks[host.host] = asyncio.ensure_future(a.check_ss(enuma=True), loop=loop)
    msg = []

    for i in asyncio.as_completed(tasks.values()):

        res = await i

        if res:
            alive_ip = res[0]
            db.remove(ErrHost, host=alive_ip)
            del tasks[res[0]]
        
    for k in tasks:
        msg.append(ErrHost(host=k))
    db.save_all(*msg)
    # return len(msg)


class BaseHandler(tornado.web.RequestHandler):
    err_ip = set()
    def prepare(self):
        self.db = self.settings['db']
        self.L = self.settings['L']
        self.shodan = lambda x: None
        if 'shodan' in self.settings:
            self.shodan = self.settings['shodan']
        self.get_ip = self.settings['geo']

    def get_current_user(self):
        return (self.get_cookie('user'),self.get_cookie('passwd'))
    def get_current_secure_user(self):
        return (self.get_cookie('user'),self.get_secure_cookie('passwd'))
    def set_current_seccure_user_cookie(self,user,passwd):
        self.set_cookie('user',user)
        self.set_secure_cookie("passwd",passwd)

    def json_arguments(self, key):
        if isinstance(self.request.body, bytes):
            body = self.request.body.decode("utf8",'ignore')
        else:
            body = self.request.body
        return json.loads(body)[key]


def intervalRefresh(interval=200):
    while 1:
        loop = asyncio.get_event_loop()
        uset = loop.run_until_complete(RefreshStatus())
        time.sleep(interval)

intervalDaemon = Process(target=intervalRefresh)
intervalDaemon.daemon = True
intervalDaemon.start()


class SocketHandler(WebSocketHandler):
    """ Web socket """
    clients = set()
    con = dict()

    @staticmethod
    def send_to_all(msg):
        for con in SocketHandler.clients:
            con.write_message(json.dumps(msg))

    @staticmethod
    def send_to_one(msg, id):
        SocketHandler.con[id(self)].write_message(msg)

    def json_reply(self, msg):
        self.write_message(json.dumps(msg))

    def open(self):
        SocketHandler.clients.add(self)
        SocketHandler.con[id(self)] = self

    def on_close(self):
        SocketHandler.clients.remove(self)

    def on_message(self, msg):
        SocketHandler.send_to_all(msg)





class IndexHandler(BaseHandler):

    def prepare(self):
        super(IndexHandler, self).prepare()
        self.template = "template/index.html"

    def get(self):
        user, passwd = self.get_current_secure_user()
        if not user or not passwd:
            self.redirect("/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan")
        # L is log function , which include ok , info , err , fail, wrn
        self.L.ok('got')
        return self.render(self.template, post_page="/")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow
        post_args = self.get_argument("some_argument")
        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']

        # redirect or reply some content
        # self.redirect()
        self.write("hello world")
        self.finish()



class MapHandler(BaseHandler):

    def prepare(self):
        super(MapHandler, self).prepare()
        self.template = "template/map.html"

    def get(self):
        user, passwd = self.get_current_secure_user()
        if not user or not passwd:
            self.redirect("/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan")
        
        # L is log function , which include ok , info , err , fail, wrn
        self.L.ok('got')
        return self.render(self.template, post_page="/map")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow
        post_args = self.get_argument("some_argument")
        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']

        # redirect or reply some content
        # self.redirect()
        self.write("hello world")
        self.finish()



class Get_ipHandler(BaseHandler):
    
    def prepare(self):
        super(Get_ipHandler, self).prepare()
        self.template = "template/get_ip.html"

    def query_hosts(self):
        exmdata = []
        geo_ll = set()
        self.settings['L'].info(BaseHandler.err_ip)
        for d in self.db.query(Host):
            geojsonFeature = {
                "type": "Feature",
                "properties": {
                    "name": "Coors Field",
                    "amenity": "Baseball Stadium",
                    "popupContent": "This is where the Rockies play!",
                    "wrn": None,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [-104.99404, 39.75621]
                }
            }


            desc = d.host
            ip = d.host
            data_m = {
                'label':'Unknow',
                'host': ip,
                'passwd': d.passwd,
                'createTime': d.getTime(),
                'location':d.location,
                'os':d.os,
                # 'loc':''
            }
            mark = self.db.query_one(Mark, host=ip)
            if mark:
                data_m['label'] = mark.label
            if ip == '0.0.0.0':continue
            geo = self.get_ip(d.host)
            geo_mark = '-'.join(geo)
            while geo_mark in geo_ll:
                geo = [str(float(geo[0]) + random.random()), str(float(geo[1]) + random.random())]
                geo_mark = '-'.join(geo)
            geo_ll.add(geo_mark)
            # data_m['loc'] = geo_mark
            geojsonFeature['properties']['name'] = desc
            geojsonFeature['geometry']['coordinates'] = geo
            geojsonFeature['properties']['msg'] = data_m
            if self.db.query_one(ErrHost, host=ip):
                geojsonFeature['properties']['wrn'] = 'wrn'
            # print(geojsonFeature['geometry']['coordinates'])
            exmdata.append(geojsonFeature)

        # print(exmdata)

        d = json.dumps(exmdata)
        return d

    async def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        # self.L.ok('got')
        tloop = tornado.ioloop.IOLoop.current()

        d = await tloop.run_in_executor(background_task_pocket, self.query_hosts)
        self.write(d)
        # self.finish()
        # return self.render(self.template, post_page="/get_ip")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow

        
        post_args = self.json_arguments("data")

        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']

        # redirect or reply some content
        # self.redirect()
        print("DDD ==>",post_args)
        for d in post_args:
            # geo = ','.join(d['geo'])
            geo = d['geo']
            print(d, geo)
            f = self.db.first('net', ip=d['ip'])
            if not f:
                self.db.insert("net", ['ip','geo','desc'], d['ip'], geo, d['desc'])

        self.write("ok")
        self.finish()



class TestHandler(BaseHandler):

    def prepare(self):
        super(TestHandler, self).prepare()
        self.template = "template/test.html"

    def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        self.L.ok('got')
        return self.render(self.template, post_page="/test")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow
        post_args = self.json_arguments("data")

        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']

        # redirect or reply some content
        # self.redirect()
        self.write("hello world")
        self.finish()




class Search_geoHandler(BaseHandler):

    def prepare(self):
        super(Search_geoHandler, self).prepare()
        self.template = "template/search_geo.html"

    def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        self.L.ok('got')
        return self.render(self.template, post_page="/search_geo")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow
        post_args = self.get_argument("name")
        print(">>",post_args)
        geo = self.db.query_one(GeoMap, name=post_args)
        if geo:
            self.write(geo.data)
        else:
            self.write(json.dumps({"features":[]}))
        self.finish()
        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']

        # redirect or reply some content
        # self.redirect()



class GetStatusHandler(BaseHandler):

    def prepare(self):
        super(GetstatusHandler, self).prepare()
        self.template = "template/getstatus.html"

    def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        self.L.ok('got')
        return self.render(self.template, post_page="/getstatus")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow
        post_args = self.get_argument("ip")
        print(">>", post_args)
        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']

        # redirect or reply some content
        # self.redirect()
        host = self.db.query_one(Host, host=post_args['ip'])
        if host:
            a = AsyncConnection(host=host.host, port=int(host.port), password=host.passwd,name=host.user, keyfile=None)
            res = AsyncConnection.run_tasks([a.check_ss()])
            if res:
                res = {'result': res[0][1]}
                self.write(json.dumps(res))
        else:
            res = {"result":[]}
            self.write(json.dumps(res))
            self.finish()



class RemoteapiHandler(BaseHandler):

    def prepare(self):
        super(RemoteapiHandler, self).prepare()
        self.template = "template/remoteapi.html"

    def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        self.L.ok('got')
        return self.render(self.template, post_page="/remoteapi")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow
        
        post_args = self.json_arguments("req")
        if post_args['op'] == 'status':
            hosts = [i.host for i in self.db.query(Host)]
            reg_host = [i.host for i in self.db.query(Reg)]
            res = {
                "res":"ok",
                "log":" show information for all host in local db.",
                "data":[ {"host":host, "reg":True} if host in reg_host else {"host": host, "reg": False} for host in hosts]
            }
        elif post_args['op'] == 'reg':
            hosts = [i.host for i in self.db.query(Host)]
            regs = [i.host for i in self.db.query(Reg)]
            unreg = set(hosts) - set(regs)
            errs = {}
            for h in unreg:
                b = Bitter(h)
                try:
                    b.register()
                except Exception as e:
                    print(e)
                    errs[h] = str(e)
            res = {
                "res":"ok",
                "log":"res",
                "data":errs
            }
        elif post_args['op'] == 'clear':
            [self.db.delete(i) for i in self.db.query(Reg)]
            res = {
                'res':'ok',
                'log':'delete all',
                'data':[]
            }
        # redirect or reply some content
        # self.redirect()
        self.write(json.dumps(res))
        self.finish()



class AsyncremoteapiHandler(BaseHandler):
    
    def prepare(self):
        super(AsyncremoteapiHandler, self).prepare()
        self.template = "template/asyncremoteapi.html"

    def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        user, passwd = self.get_current_secure_user()
        if not user or not passwd:
            self.redirect("/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan")
        
        self.L.ok('got')
        return self.render(self.template, post_page="/asyncremoteapi")


    def back(self, data):
        if 'result' in data['msg']:
            data = json.dumps(data['msg']['result'])
        else:
            data = json.dumps(data['msg'])

        print(data)
        self.write(data)
        self.finish()
        # tornado.ioloop.IOLoop.instance().add_callback(functools.partial(self.write_callback, data))

    def write_callback(self, output):
        self.write(output)
        self.finish()

    async def a_back(self, data):
        if not data:
            self.write(json.dumps({'data':[{'res':'Timeout or failed'}]}))
        else:

            if isinstance(data, dict):
                self.settings["L"].info("use-cache")
                ss_conf = data
                m = [ss_conf['server']]
            else:
                m = data
                self.settings['L'].info(m)
                if not m[1]:
                    self.write(json.dumps({'data':[{'Result':'no ss found!'}]}))
                else:
                    # self.settings['L'].info(m[1])
                    if not m[1].strip().startswith("{"):
                        ss_conf = {'msg':m[1]}
                    else:
                        ss_conf = json.loads(m[1])
            data = []
            if 'port_password' in ss_conf:
                d = ss_conf['port_password']
                data += [{'port': i, 'password': d[i],'method':ss_conf['method'], 'ip':m[0]} for i in d]
            elif 'server_port' in ss_conf:
                data.append({'port':ss_conf['server_port'], 'password':ss_conf['password'],'method':ss_conf['method'], 'ip':m[0]})
            else:
                data.append(ss_conf)
            self.write(json.dumps({'data':data}))

    async def async_run(self, host,name, *args,loop=None, **kargs):

        a = AsyncConnection(host=host.host, port=int(host.port), password=host.passwd,name=host.user, keyfile=None)
        a.timeout_t = 15
        if hasattr(a, name):
            f = getattr(a, name)
        else:
            f = a.ssh
        res_f =  f(*args, **kargs)
        try:
            res = await asyncio.wait_for(res_f, 30)
            await self.a_back(res)
        except concurrent.futures._base.TimeoutError:
            await self.a_back(None)
        
    async def post(self):
        # you should get some argument from follow
        tloop = tornado.ioloop.IOLoop.current()
        token = self.db.query_one(Token)
        if token:
            token = token.token
        post_args = self.json_arguments("req")
        L(post_args, color='green')
        if post_args['op'] == 'status':
            h = post_args['ip']
            host = self.db.query_one(Host, host=h)
            
            p = os.path.join(self.settings['ss-saved'], host.host)
            if os.path.exists(p):
                conf = Book.ss(p, only_dict=True)
                await self.a_back(conf)
            else:
                await self.async_run(host,'check_ss',enuma=True, loop=tloop)

        elif post_args['op'] == 'regionlist':
            
            
            d = to("https://api.vultr.com/v1/regions/list", headers={"API-Key": token}).json()
            self.write(json.dumps(list(d.values())))
            #self.finish()

        elif post_args['op'] == 'scriptlist':

            d = to("https://api.vultr.com/v1/startupscript/list", headers={"API-Key": token}).json()
            self.write(json.dumps(list(d.keys())))


        elif post_args['op'] == 'mark':
            ip= post_args['ip']
            label = post_args['label']
            ol = self.db.query_one(Mark, host=ip)
            if ol:
                self.db.delete(ol)
            mark = Mark(host=ip, label=label)
            mark.save(self.db)

        elif post_args['op'] == 'destroy':
            h = post_args['ip']
            
            def after_get_servers(data):
                d = data.json()
                breakone = False
                for id in d:
                    if d[id]['main_ip'] == h:
                        destroy_one(token, id)
                        breakone = True
                        break
                
                Controll(token).do_update('')
                self.write(json.dumps({"id":"destroy"}))
            await back_request("https://api.vultr.com/v1/server/list", after_get_servers, headers={"API-Key": token}, loop=tloop)

        elif post_args['op'] == 'update':
            
            def after_get_servers(data):
                update_db(data)
                # Controll(api).do_update('')
                self.write(json.dumps({"update":"ok"}))
            await back_request("https://api.vultr.com/v1/server/list", after_get_servers, headers={"API-Key": token},loop=tloop)

        elif post_args['op'] == 'settoken':
            api = post_args['token']
            t = Token(token=api)
            t.save(self.db)
            self.write(json.dumps({"msg":"ok"}))

        elif post_args['op'] == 'create_server':
            # api = post_args['token']
            msg = post_args['msg']
            osn = post_args['os']
            label = post_args['label']
            print(post_args)
            osid = 270
            planid = 201
            if osn=='centos':
                osid = 167
            dcid = msg.split("DCID:").pop().strip()
            print(osid, dcid,planid)
            def after_get_scriptid(data):
                d = data.json()
                create_one(token,**{
                    "DCID":dcid,
                    "VPSPLANID": planid,
                    "OSID": osid,
                    "label": label,
                    "SCRIPTID":list(d.keys())[0]
                })
                self.write(json.dumps(d))

            await back_request("https://api.vultr.com/v1/startupscript/list", after_get_scriptid, 
                method='get',
                headers={"API-Key": token},
                loop=tloop,
            )
        elif post_args['op'] == 'getpass':
            # h = post_args['ip']
            hh = self.db.query_one(Host, host=post_args['ip'])
            self.write(json.dumps({
                    'data':{
                        'passwd': hh.passwd,
                        'createTime': hh.getTime(),
                        'host': hh.host,
                    }
                }))

        elif post_args['op'] == 'base':
            h = post_args['ip']
            host = self.db.query_one(Host, host=h)
            await self.async_run(host,'enuma_elish', loop=tloop)
        elif post_args['op'] == 'qr':
            h = post_args['ip']
            if os.path.exists(os.path.join(self.settings['ss-saved'], h)):
                async with aiofiles.open(os.path.join(self.settings['ss-saved'], h)) as afp:
                    d = await afp.read()
                    d = json.loads(d)
                    self.settings['L'].info(d)
                    pwd = d['password'] if 'password' in d else None
                    if 'port_password' in d:
                        port = random.choice(list(d['port_password'].keys()))
                        pwd = d['port_password'][port]
                    else:
                        port = d['server_port']
                    method = d['method']
                    
                    code = 'ss://' + b64encode('{method}:{pwd}@{host}:{port}'.format(host=h,pwd=pwd, port=port, method=method).encode('utf8')).decode('utf8')
                    R = '{method}:{pwd}@{host}:{port}'.format(host=h,pwd=pwd, port=port, method=method)
                    self.write(json.dumps({"data": code, 'code':R}))
            else:
                self.write(json.dumps({"data":"ss://"}))
        elif post_args['op'] == 'set-proxy':
            proxy = post_args['proxy']
            if proxy.startswith("socks5://"):
                async with aiofiles.open(self.settings['proxy-config-file.conf'], 'w') as afp:
                    await afp.write(proxy)

        elif post_args['op'] == 'link':
            if_tor = False
            if 'tor' in post_args:
                if_tor = True

            from_ip = post_args['ip']
            use_minute = post_args['use-minute']
            to_ip = post_args['target']
            await self.async_link(from_ip, to_ip, use_minute)

        elif post_args['op'] == 'all_links':
            h = post_args['ip']
            targets = await tloop.run_in_executor(background_task_pocket,self.all_links,h)            
        # for parse json post
            self.write(json.dumps({'routes':targets}))

    def all_links(self, ip):
        path = os.path.join(self.settings['ss-saved'], ip)
        if os.path.exists(path):
            c = Book.ss(path, True)
            routes = Book.checkRoutes(c['server'], int(c['server_port']), c['password'], method=c['method'])
            self.settings['L'].info(routes)
            if b'routes' in routes:
                # print(routes)
                ips = [{'ip':i['server'], 'geo':self.get_ip(i['server'])} for i in json.loads(routes.decode())['routes'] if self.get_ip(i['server']) and i['server'] != ip]
                return ips
        return []



        

    def link_to(self, fip, tip,use_time=600):
        f_co = None
        t_co = None
        for r, ds,fs in os.walk(self.settings['ss-saved']):
            for f in fs:
                if fip in f:
                    with open(os.path.join(r, f)) as fp:
                        f_co = json.load(fp) 
                if tip in f:
                    self.settings['L'].info(f)
                    
                    t_co = Book.ss(os.path.join(r, f))

                    self.settings['L'].info(t_co)
                if f_co and t_co:
                    break
        if t_co and f_co:
            Book.refreshTime(f_co['server'],int(f_co['server_port']),use_time, f_co['password'], method=f_co['method'])
            self.settings['L'].info(Book.linkOther(f_co['server'],int(f_co['server_port']),t_co, f_co['password'], method=f_co['method']))
            return Book.linkOther(f_co['server'],int(f_co['server_port']),t_co, f_co['password'], method=f_co['method'])
        if not t_co:
            return 'no target ss config'
        if not f_co:
            return 'no from ss config'

    async def async_link(self, f_ip, to_ip, use_time=600):
        tloop = tornado.ioloop.IOLoop.current()
        res = await tloop.run_in_executor(background_task_pocket, self.link_to, f_ip, to_ip, use_time)
        if isinstance(res, bytes):
            res = res.decode()
        if not res:
            self.write(json.dumps({
                'res':'link failed',
                'log':'bad'
            }))
        else:
            if 'Ich liebe dich' in res:
                self.write(json.dumps({
                    'res':'link ok',
                    'log':'good'
                }))
            else:
                self.write(json.dumps({
                    'res':res,
                    'log':'bad'
                }))
            

class RegHandler(BaseHandler):
    def prepare(self):
        super(RegHandler, self).prepare()
        self.template = "template/login.html"
    def get(self):
        return self.render(self.template, post_page="/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan")
    
    @tornado.web.asynchronous
    def post(self):
        user = self.get_argument("user")
        passwd = self.get_argument("passwd")
        u = User(user=user, pwd=passwd)
        u.save(self.db)
        self.redirect("/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan")


class LoginHandler(BaseHandler):
    def prepare(self):
        super(LoginHandler, self).prepare()
        self.template = "template/login.html"
    def get(self):
        if not self.db.query_one(User):
            return self.render(self.template, post_page="/reg")
        else:
            return self.render(self.template, post_page="/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan")
    
    @tornado.web.asynchronous
    def post(self):
        user = self.get_argument("user")
        passwd = self.get_argument("passwd")
        u = self.db.query_one(User, user=user)
        if u.pwd == passwd:
            self.set_current_seccure_user_cookie(user,passwd)
            self.redirect("/")
        else:
            self.write("Fu*k U !")
            self.finish()

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan")


class CreateHandler(BaseHandler):
    
    def prepare(self):
        super(CreateHandler, self).prepare()
        self.template = "template/create.html"

    def get(self):
        user, passwd = self.get_current_secure_user()
        if not user or not passwd:
            self.redirect("/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan")

        # L is log function , which include ok , info , err , fail, wrn
        self.L.ok('got')
        return self.render(self.template, post_page="/create")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow 
        post_args = self.get_argument("some_argument")
        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']
        
        # redirect or reply some content
        # self.redirect()  
        self.write("hello world")
        self.finish()
    
