# from asynctools.servers import TcpTests
import requests
from termcolor import cprint,colored
import json
import os
import re
import cmd
import random
import getpass
import base64
from qlib.data import dbobj, Cache
from asyncio import  get_event_loop
from .test_route import sync
from .test_route import DB_PATH
class Host(dbobj):pass
INIT_PAYLOAD = b'IyEvYmluL2Jhc2gKI2luc3RhbGwgcHl0aG9uCgpoYXNoIGFwdCAyPi9kZXYvbnVsbAppZiBbICQ/IC1lcSAwIF07dGhlbgogICAgZWNobyAiYXB0IGlzIGV4aXN0ZWQgaW5zdGFsbCBhcHQtbGliIgogICAgYXB0LWdldCBpbnN0YWxsIC15IGxpYmM2LWRldiBnY2MKICAgIGFwdC1nZXQgaW5zdGFsbCAteSBtYWtlIGJ1aWxkLWVzc2VudGlhbCBsaWJzc2wtZGV2IHpsaWIxZy1kZXYgbGlicmVhZGxpbmUtZGV2IGxpYnNxbGl0ZTMtZGV2IHdnZXQgY3VybCBsbHZtCmVsc2UKICAgIGhhc2ggeXVtIDI+L2Rldi9udWxsCiAgICBpZiBbICQ/IC1lcSAwIF07dGhlbgogICAgICAgIGVjaG8gInl1bSBpcyBleGlzdGVkIGluc3RhbGwgeXVtLWxpYiIKICAgICAgICB5dW0gLXkgaW5zdGFsbCB3Z2V0IGdjYyBtYWtlIGVwZWwtcmVsZWFzZQogICAgICAgIHl1bSB1cGRhdGUgLXkKICAgICAgICB5dW0gLXkgaW5zdGFsbCAgbmV0LXRvb2xzCiAgICAgICAgeXVtIC15IGluc3RhbGwgemxpYjFnLWRldiBiemlwMi1kZXZlbCBvcGVuc3NsLWRldmVsIG5jdXJzZXMtZGV2ZWwgc3FsaXRlLWRldmVsIHJlYWRsaW5lLWRldmVsIHRrLWRldmVsIGdkYm0tZGV2ZWwgZGI0LWRldmVsIGxpYnBjYXAtZGV2ZWwgeHotZGV2ZWwKICAgIGZpCmZpCgoKaGFzaCBweXRob24zIDI+L2Rldi9udWxsCiAgICBpZiAgWyAkPyAtZXEgMCBdO3RoZW4KICAgIHJlcz0kKHB5dGhvbjMgLVYgMj4mMSB8IGF3ayAne3ByaW50ICQxfScpCiAgICB2ZXJzaW9uPSQocHl0aG9uMyAtViAyPiYxIHwgYXdrICd7cHJpbnQgJDJ9JykKICAgICNlY2hvICJjaGVjayBjb21tYW5kKHB5dGhvbikgYXZhaWxhYmxlIHJlc3V0bHMgYXJlOiAkcmVzIgogICAgaWYgWyAiJHJlcyIgPT0gIlB5dGhvbiIgXTt0aGVuCiAgICAgICAgaWYgICBbICIke3ZlcnNpb246MDozfSIgPT0gIjMuNiIgXTt0aGVuCiAgICAgICAgICAgIGVjaG8gIkNvbW1hbmQgcHl0aG9uMyBjb3VsZCBiZSB1c2VkIGFscmVhZHkuIgogICAgICAgICAgICAgICAgIGhhc2ggcGlwMyAyPi9kZXYvbnVsbDsKICAgICAgICAgICAgICAgICBpZiBbICQ/IC1lcSAgMCBdO3RoZW4KICAgICAgICAgICAgICAgICAgICBwaXAzIGluc3RhbGwgLVUgZ2l0K2h0dHBzOi8vZ2l0aHViLmNvbS9zaGFkb3dzb2Nrcy9zaGFkb3dzb2Nrcy5naXRAbWFzdGVyCiAgICAgICAgICAgICAgICAgICAgcGlwMyBpbnN0YWxsIHgtbXJveS0xMDQ1CiAgICAgICAgICAgICAgICAgICAgcGlwMyBpbnN0YWxsIHgtbXJveS0xMDQ2CiAgICAgICAgICAgICAgICAgICAgcGlwMyBpbnN0YWxsIHgtbXJveS0xMDQ3CiAgICAgICAgICAgICAgICAgICAgcGlwMyBpbnN0YWxsIHgtbXJveS0xMDQ4CiAgICAgICAgICAgICAgICAgICAgcGlwMyBpbnN0YWxsIC1VIGdpdCtodHRwczovL2dpdGh1Yi5jb20vUWluZ2x1YW4vc3dvcmRub2RlLmdpdAoKICAgICAgICAgICAgICAgICAgICBlY2hvICJCdWlsZEZsYWciID4+IC9ldGMvaWJ1aWxkCiAgICAgICAgICAgICAgICAgICAgY2F0IDw8IEVPRiA+PiAvZXRjL3NoYWRvd3NvY2tzLmpzb24KewogICAgInNlcnZlciI6IjAuMC4wLjAiLAogICAgInBvcnRfcGFzc3dvcmQiOiB7CiAgICAgICAgIjEzMDAxIjogInRoZWZvb2xpc2gxIiwKICAgICAgICAiMTMwMDIiOiAidGhlZm9vbGlzaDIiLAogICAgICAgICIxMzAwMyI6ICJ0aGVmb29saXNoMyIsCiAgICAgICAgIjEzMDA0IjogInRoZWZvb2xpc2g0IiwKICAgICAgICAiMTMwMDUiOiAidGhlZm9vbGlzaDUiLAogICAgICAgICIxMzAwNiI6ICJ0aGVmb29saXNoNiIsCiAgICAgICAgIjEzMDA3IjogInRoZWZvb2xpc2g3IiwKICAgICAgICAiMTMwMDgiOiAidGhlZm9vbGlzaDgiLAogICAgICAgICIxMzAwOSI6ICJ0aGVmb29saXNoOSIsCiAgICAgICAgIjEzMDEwIjogInRoZWZvb2xpc2gxMCIsCiAgICAgICAgIjEzMDExIjogInRoZWZvb2xpc2gxMSIsCiAgICAgICAgIjEzMDEyIjogInRoZWZvb2xpc2gxMiIsCiAgICAgICAgIjEzMDEzIjogInRoZWZvb2xpc2gxMyIKICAgIH0sCiAgICAid29ya2VycyI6IDE1LAogICAgIm1ldGhvZCI6ImFlcy0yNTYtY2ZiIgp9CkVPRgogICAgICAgICAgICAgICAgICAgIHNzc2VydmVyIC1jIC9ldGMvc2hhZG93c29ja3MuanNvbiAtZCBzdGFydAogICAgICAgICAgICAgICAgICAgIHgtbmVpZC1zZXJ2ZXIgc3RhcnQKICAgICAgICAgICAgICAgICAgICBleGl0IDAKICAgICAgICAgICAgICAgICBlbHNlCiAgICAgICAgICAgICAgICAgICAgYXB0IGluc3RhbGwgLXkgcHl0aG9uMy1waXAgcHl0aG9uMy1zZXR1cHRvb2xzCiAgICAgICAgICAgICAgICAgICAgcGlwMyBpbnN0YWxsIC1VIGdpdCtodHRwczovL2dpdGh1Yi5jb20vc2hhZG93c29ja3Mvc2hhZG93c29ja3MuZ2l0QG1hc3RlcgogICAgICAgICAgICAgICAgICAgIHBpcDMgaW5zdGFsbCB4LW1yb3ktMTA0NQogICAgICAgICAgICAgICAgICAgIHBpcDMgaW5zdGFsbCB4LW1yb3ktMTA0NgogICAgICAgICAgICAgICAgICAgIHBpcDMgaW5zdGFsbCB4LW1yb3ktMTA0NwogICAgICAgICAgICAgICAgICAgIHBpcDMgaW5zdGFsbCB4LW1yb3ktMTA0OAogICAgICAgICAgICAgICAgICAgIHBpcDMgaW5zdGFsbCAtVSBnaXQraHR0cHM6Ly9naXRodWIuY29tL1FpbmdsdWFuL3N3b3Jkbm9kZS5naXQKICAgICAgICAgICAgICAgICAgICBlY2hvICJCdWlsZEZsYWciID4+IC9ldGMvaWJ1aWxkCiAgICAgICAgICAgICAgICAgICAgY2F0IDw8IEVPRiA+PiAvZXRjL3NoYWRvd3NvY2tzLmpzb24KewogICAgInNlcnZlciI6IjAuMC4wLjAiLAogICAgInBvcnRfcGFzc3dvcmQiOiB7CiAgICAgICAgIjEzMDAxIjogInRoZWZvb2xpc2gxIiwKICAgICAgICAiMTMwMDIiOiAidGhlZm9vbGlzaDIiLAogICAgICAgICIxMzAwMyI6ICJ0aGVmb29saXNoMyIsCiAgICAgICAgIjEzMDA0IjogInRoZWZvb2xpc2g0IiwKICAgICAgICAiMTMwMDUiOiAidGhlZm9vbGlzaDUiLAogICAgICAgICIxMzAwNiI6ICJ0aGVmb29saXNoNiIsCiAgICAgICAgIjEzMDA3IjogInRoZWZvb2xpc2g3IiwKICAgICAgICAiMTMwMDgiOiAidGhlZm9vbGlzaDgiLAogICAgICAgICIxMzAwOSI6ICJ0aGVmb29saXNoOSIsCiAgICAgICAgIjEzMDEwIjogInRoZWZvb2xpc2gxMCIsCiAgICAgICAgIjEzMDExIjogInRoZWZvb2xpc2gxMSIsCiAgICAgICAgIjEzMDEyIjogInRoZWZvb2xpc2gxMiIsCiAgICAgICAgIjEzMDEzIjogInRoZWZvb2xpc2gxMyIKICAgIH0sCiAgICAid29ya2VycyI6IDE1LAogICAgIm1ldGhvZCI6ImFlcy0yNTYtY2ZiIgp9CkVPRgogICAgICAgICAgICAgICAgICAgIHNzc2VydmVyIC1jIC9ldGMvc2hhZG93c29ja3MuanNvbiAtZCBzdGFydAogICAgICAgICAgICAgICAgICAgIHgtbmVpZC1zZXJ2ZXIgc3RhcnQKICAgICAgICAgICAgICAgICAgICBleGl0IDAKICAgICAgICAgICAgICAgICBmaQogICAgICAgIGZpCiAgICBmaQpmaQoKZWNobyAiY29tbWFuZCBweXRob24gY2FuJ3QgYmUgdXNlZC5zdGFydCBpbnN0YWxsaW5nIHB5dGhvbjMuNi4iCmNkIC90bXAKICAgIGlmIFsgLWYgL3RtcC9QeXRob24tMy42LjEudGd6IF07dGhlbgogICAgICBybSAvdG1wL1B5dGhvbi0zLjYuMS50Z3o7CiAgICBmaQp3Z2V0IGh0dHBzOi8vd3d3LnB5dGhvbi5vcmcvZnRwL3B5dGhvbi8zLjYuMS9QeXRob24tMy42LjEudGd6CnRhciAtenh2ZiBQeXRob24tMy42LjEudGd6CmNkIFB5dGhvbi0zLjYuMQpta2RpciAvdXNyL2xvY2FsL3B5dGhvbjMKLi9jb25maWd1cmUgLS1wcmVmaXg9L3Vzci9sb2NhbC9weXRob24zCm1ha2UKbWFrZSBpbnN0YWxsCmlmIFsgLWYgL3Vzci9iaW4vcHl0aG9uMyBdO3RoZW4KICAgcm0gL3Vzci9iaW4vcHl0aG9uMzsKICAgcm0gL3Vzci9iaW4vcGlwMzsKZmkKCmlmIFsgLWYgL3Vzci9iaW4vbHNiX3JlbGVhc2UgXTt0aGVuCiAgcm0gL3Vzci9iaW4vbHNiX3JlbGVhc2U7CmZpCgpsbiAtcyAvdXNyL2xvY2FsL3B5dGhvbjMvYmluL3B5dGhvbjMgL3Vzci9iaW4vcHl0aG9uMwpsbiAtcyAvdXNyL2xvY2FsL3B5dGhvbjMvYmluL3BpcDMgL3Vzci9iaW4vcGlwMwoKZWNobyAnZXhwb3J0IFBBVEg9IiRQQVRIOi91c3IvbG9jYWwvcHl0aG9uMy9iaW4iJyA+PiB+Ly5iYXNocmMKCnBpcDMgaW5zdGFsbCAtVSBnaXQraHR0cHM6Ly9naXRodWIuY29tL3NoYWRvd3NvY2tzL3NoYWRvd3NvY2tzLmdpdEBtYXN0ZXIKcGlwMyBpbnN0YWxsIHgtbXJveS0xMDQ1CnBpcDMgaW5zdGFsbCB4LW1yb3ktMTA0NgpwaXAzIGluc3RhbGwgeC1tcm95LTEwNDcKcGlwMyBpbnN0YWxsIHgtbXJveS0xMDQ4CnBpcDMgaW5zdGFsbCAtVSBnaXQraHR0cHM6Ly9naXRodWIuY29tL1FpbmdsdWFuL3N3b3Jkbm9kZS5naXQKCmVjaG8gIkJ1aWxkRmxhZyIgPj4gL2V0Yy9pYnVpbGQKY2F0IDw8IEVPRiA+PiAvZXRjL3NoYWRvd3NvY2tzLmpzb24KewogICAgInNlcnZlciI6IjAuMC4wLjAiLAogICAgInBvcnRfcGFzc3dvcmQiOiB7CiAgICAgICAgIjEzMDAxIjogInRoZWZvb2xpc2gxIiwKICAgICAgICAiMTMwMDIiOiAidGhlZm9vbGlzaDIiLAogICAgICAgICIxMzAwMyI6ICJ0aGVmb29saXNoMyIsCiAgICAgICAgIjEzMDA0IjogInRoZWZvb2xpc2g0IiwKICAgICAgICAiMTMwMDUiOiAidGhlZm9vbGlzaDUiLAogICAgICAgICIxMzAwNiI6ICJ0aGVmb29saXNoNiIsCiAgICAgICAgIjEzMDA3IjogInRoZWZvb2xpc2g3IiwKICAgICAgICAiMTMwMDgiOiAidGhlZm9vbGlzaDgiLAogICAgICAgICIxMzAwOSI6ICJ0aGVmb29saXNoOSIsCiAgICAgICAgIjEzMDEwIjogInRoZWZvb2xpc2gxMCIsCiAgICAgICAgIjEzMDExIjogInRoZWZvb2xpc2gxMSIsCiAgICAgICAgIjEzMDEyIjogInRoZWZvb2xpc2gxMiIsCiAgICAgICAgIjEzMDEzIjogInRoZWZvb2xpc2gxMyIKICAgIH0sCiAgICAid29ya2VycyI6IDE1LAogICAgIm1ldGhvZCI6ImFlcy0yNTYtY2ZiIgp9CkVPRgoKc3NzZXJ2ZXIgLWMgL2V0Yy9zaGFkb3dzb2Nrcy5qc29uIC1kIHN0YXJ0CngtbmVpZC1zZXJ2ZXIgc3RhcnQ='

rdir_path = os.path.dirname(__file__)
static_path = os.path.join(rdir_path, "static")
files_path = os.path.join(static_path, "files")


EXPORT_TEMPLATE = {
    "random" : False,
    "authPass" : None,
    "useOnlinePac" : False,
    "TTL" : 0,
    "global" : False,
    "reconnectTimes" : 3,
    "index" : 0,
    "proxyType" : 0,
    "proxyHost" : None,
    "authUser" : None,
    "proxyAuthPass" : None,
    "isDefault" : False,
    "pacUrl" : None,
    "configs" : [
    ],
    "proxyPort" : 0,
    "randomAlgorithm" : 0,
    "proxyEnable" : False,
    "enabled" : True,
    "autoban" : False,
    "proxyAuthUser" : None,
    "shareOverLan" : False,
    "localPort" : 1080
}

class Reg(dbobj):pass


def gprint(*args,pc='green', cc=None, **kwargs):
    print(colored("[+]",pc, attrs=['bold']), colored(" ".join([str(i) for i in args]),cc) ,**kwargs)

def show(data, tab=0):
    gprint("result", cc='red')
    if isinstance(data, bytes):
        data = json.loads(data.decode("utf-8"))
    if isinstance(data, dict):
        for k in data:
            if isinstance(data[k], dict):
                print(k,":")
                show(data[k],tab=tab+2)
            else:
                cprint(tab* ' '  + "{} => {} ".format(k, data[k]), "yellow")
    else:
        gprint(data)

APIURL="https://api.vultr.com/v1/"

API_LIST = [
    "account/info",
    "app/list",
    "auth/info",
    "backup/list",
    # create server
    "os/list",
    "regions/list",
    "plans/list",
    "server/list",
    "baremetal/list",
    "startupscript/list"
]

def create_one(api,**kwargs):
    url = APIURL + "server/create"
    options = {
        "DCID":None,
        "VPSPLANID": None,
        "OSID": None,
        "label": None,
    }
    options.update(kwargs)
    for k in options:
        if not options[k]:
            gprint("Not set {}".format(k), pc="red")
            return None
    con = requests.post(url, data=options, headers={"API-Key": api})
    # con.options(headers={"API-Key": api})
    # con.post(data=options, callback=show)
    if con.status_code == 200:
        return con.json()
    return False

def test_all(api, port):
    pass
    # loop = get_event_loop()
    # def _deal(data):
    #     if isinstance(data, bytes):
    #         data = json.loads(data.decode("utf-8"))
    #     else:
    #         data = json.loads(data)
    #     print("... Test Connection ...")

    #     res = {data[id]['main_ip']:id for id in data}
    #     hosts = [i + ":%s" % port for i in  res]
    #     for i in hosts:
    #         print(colored(i,'blue'))
    #     res_1 = TcpTests(hosts, loop)
    #     print("finish : ")
    #     for i in res_1:
    #         print(colored(i[0], 'green'))
    #     unres = set(hosts)  - set([i[0] for i in res_1])
    #     for ip_port in unres:
    #         ip = ip_port.split(":")[0]
    #         _id = res[ip]
    #         print(_id, ip)

    # url = APIURL + "server/list"
    # con = requests.get(url, headers={'API-Key': api}).json()
    # _deal(con)

def destroy_one(api, id):
    url = APIURL + "server/destroy"
    options = {
        "SUBID" : id,
    }
    con = requests.post(url,data=options, headers={"API-Key": api}).json()
    show(con)


def clear_regions(api, region=None):
    

    url = APIURL + "server/list"
    con = requests.get(url, headers={'API-Key': api}).json()
    
    
    def _deal(data):
        if isinstance(data, bytes):
            data = json.loads(data.decode("utf-8"))
        else:
            data = json.loads(data)
        ids = []
        for id in data:
            if region and region in data[id]['location'].lower():
                ids.append(id)
        for i in ids:
            print("clear id: ", data[i]['main_ip'], data[i]['location'])
            destroy_one(api, i)

    _deal(con)


def update_db(data):
    db = Cache(DB_PATH)
    if isinstance(data, bytes):
        d = json.loads(data)
    else:
        d = data.json()
    s_clound = {d[i]['main_ip']:d[i]  for i in d}
    hs_clound = s_clound.keys()
    hs_now = [i.host for i in db.query(Host)]
    hs = []
    ds = set(hs_now) - set(hs_clound)
    ns = set(hs_clound) - set(hs_now)
    Dir  = os.path.join(os.path.dirname(DB_PATH), "shadowsocks")
    for n in s_clound:
        vars = s_clound[n]
        ii = random.randint(1,9)
        server_j = {
            "server":vars['main_ip'],
            'server_port':int("13000%d" % ii),
            'password':'thefoolish%d' % ii,
            'method':'aes-256-cfb',
            'local_port':'1080'
        }

        w = {
            "enable" : True,
            "password" : "thefoolish1",
            "method" : "aes-256-cfb",
            "remarks" : "h",
            "server" : "115.236.8.152",
            "kcptun" : {
                "nocomp" : False,
                "key" : "it's a secrect",
                "crypt" : "aes",
                "datashard" : 10,
                "mtu" : 1350,
                "mode" : "fast",
                "parityshard" : 3,
                "arguments" : ""
            },
            "enabled_kcptun" : False,
            "server_port" : 13001,
            "remarks_base64" : ""
        }
        w.update(server_j)
        EXPORT_TEMPLATE['configs'].append(w)

    for n in ns:
        vars = s_clound[n]
        hs.append(Host(host=vars['main_ip'],passwd=vars['default_password'], port='22', user='root', location=vars['location'],os=vars['os'], disk=vars['disk'],vcpu_count=vars['vcpu_count'],cost_per_month=vars['cost_per_month']))
        gprint(vars['main_ip'], ' V')
        # if os.path.exists(path):
        fname = vars['location']+".json"
        fs = os.listdir(Dir)
        if fname in fs:
            c = 1
            while 1:
                
                if (fname + str(c)) not in fs:
                    fname += str(c)
                    break
                else:
                    c += 1
        print(fname, " -> local")
        server_j = {
            "server":vars['main_ip'],
            'server_port':13003,
            'password':'thefoolish3',
            'method':'aes-256-cfb',
            'local_port':'1080'
        }
        
        with open(os.path.join(Dir, fname),'w') as fp:
            json.dump(server_j, fp)
        
        

    with open(os.path.join(files_path, 'export_all.json'), 'w') as fp:
        json.dump(EXPORT_TEMPLATE, fp, indent=4)

    for h in ds:
        print("x",h)
        e = db.query_one(Host, host=h)
        db.delete(e)
    for h in hs:
        h.save(db)



class Controll(cmd.Cmd):


    def __init__(self, token=None):
        super().__init__()
        self.prompt = colored(">", 'yellow', attrs=['bold'])
        self.api_key = token

        if not token:
            self.api_key = getpass.getpass()
        self.SUBID = ""
        self.OSID = '270'
        self.DCID = '25'
        self.PLANID = '201'
        self.SCRIPTID = ''
        self.label = 'jp-os'


    def do_exit(self, text):
        return True

    def do_regist_all(self,text):
        db = Cache(DB_PATH)
        hosts = [i.host for i in db.query(Host)]
        regs = [i.host for i in db.query(Reg)]
        unreg = set(hosts) - set(regs)
        errs = {}
        for h in unreg:
            b = None#Bitter(h)
            try:
                b.register()
            except Exception as e:
                print(e)
                errs[h] = str(e)
            print(colored(h, 'green'))


    def do_show(self, text):
        for k in ['OSID', 'DCID', 'SUBID', 'PLANID', 'label']:
            gprint(k,"=", getattr(self, k))

    def do_test_all(self, text):
        api = self.api_key
        test_all(api, text)

    def do_set(self, text):
        if not '=' in text:
            gprint("must k = v")
            return
        k,v = text.split("=", 1)
        gprint(k,v)
        setattr(self,k.strip(),v.strip())



    def complete_set(self, text, line, begin, end):
        e = []
        for k in ['OSID', 'DCID', 'SUBID', 'PLANID', 'label']:
            if text in k:
                e.append(k)
        return e

    def do_create_script(self, file):
        t = base64.b64decode(INIT_PAYLOAD).decode("utf8")
        if  os.path.exists(file):
            with open(file) as fp:
                t = fp.read()
        con = requests.post(APIURL + "startupscript/create",
            data={'name':'script','script':t},
            headers={'API-Key': self.api_key})
        
        show(con.json())

    def do_update(self, text):
        # con = Connection(APIURL + "server/list", tp='http')
        # # requests.get(APIURL + "server/list")
        # con.options(headers={'API-Key': self.api_key})
        # con.get(callback=update_db)
        sync(token=self.api_key)

    def do_get(self, uri):
        con = requests.get(APIURL + uri, headers={'API-Key': self.api_key})
        show(con.json())

    def do_clear_region(self, region):

        clear_regions(self.api_key, region)


    def do_create_server(self, text):
        if not text:
            text = "x"
        if not self.SCRIPTID:
            yn = input("scirpt id : null. do you want to use a scirpt id as startup scirpt? [y/n]").strip()
            if yn in ['','y', 'Y']:
                ids = requests.get(APIURL + "startupscript/list", headers={"API-Key": self.api_key}).json()
                while 1:
                    c = input("\nid:".join(ids.keys()) +"\nsee id [s:num] | use id [num]\n>")
                    if ':' in c:
                        c = c.split(":").pop()
                        cprint(ids[c]['script'], 'magenta')
                    elif re.match(r'^\d+$', c) and c in ids:
                        self.SCRIPTID = c
                        break
                    else:
                        cprint("try again !", 'red')


        create_one(self.api_key,**{
            "DCID": self.DCID,
            "OSID": self.OSID,
            "VPSPLANID" : self.PLANID,
            "SCRIPTID": self.SCRIPTID,
            "label": text,
        })

    def do_destroy(self, subid):
        if not self.SUBID:
            gprint("must set a valid subid")
            return False
        destroy_one(self.api_key, self.SUBID)

    def complete_get(self, text, line, begin, end):
        e = []
        for i in API_LIST:
            if text in i:
                e.append(i)
        return e

    def do_apilist(self, text):
        for i in API_LIST:
            gprint(i)

def main():
    c = Controll()
    c.cmdloop()

if __name__ == '__main__':

    main()
