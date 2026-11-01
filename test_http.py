import http.client
import json
from pathlib import Path
import threading
import unittest
import uuid
from http.server import ThreadingHTTPServer
from server import Handler, Store

class HttpTests(unittest.TestCase):
    def setUp(self):
        self.dir=Path(__file__).resolve().parent/'data-tests';self.dir.mkdir(exist_ok=True)
        self.db=self.dir/('http-'+uuid.uuid4().hex+'.sqlite3')
        store=Store(self.db)
        handler=type('TestHandler',(Handler,),{'store':store,'failures':{}})
        self.server=ThreadingHTTPServer(('127.0.0.1',0),handler)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.port=self.server.server_port;self.cookie='';self.csrf=''
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join()
        for suffix in ('','-wal','-shm'):
            p=Path(str(self.db)+suffix);assert p.resolve().parent==self.dir.resolve();p.unlink(missing_ok=True)
    def request(self,path,body=None,extra=None):
        c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=10)
        headers={'Content-Type':'application/json','Cookie':self.cookie,'X-CSRF':self.csrf}
        headers.update(extra or {})
        c.request('POST' if body is not None else 'GET',path,json.dumps(body) if body is not None else None,headers)
        r=c.getresponse();raw=r.read();status=r.status;set_cookie=r.getheader('Set-Cookie');c.close()
        if set_cookie:self.cookie=set_cookie.split(';',1)[0]
        return status,json.loads(raw)
    def test_login_csrf_stock_and_host_boundary(self):
        self.assertEqual(self.request('/api/state')[0],401)
        self.assertEqual(self.request('/api/setup',{'password':'temporary-test-password','demo':True})[0],201)
        self.assertEqual(self.request('/api/login',{'id':'owner','password':'temporary-test-password'})[0],200)
        code,state=self.request('/api/state');self.assertEqual(code,200)
        self.assertEqual(len(state['users']),5)
        self.csrf=state['user']['csrf'];p=state['products'][0]
        chat=self.request('/api/assistant',{'question':'Stok mana yang menipis?'})
        self.assertEqual(chat[0],200)
        self.assertEqual(chat[1]['mode'],'local-rules')
        goal=self.request('/api/assistant',{'question':'Target penjualan kita?'})
        self.assertEqual(goal[0],200)
        self.assertIn('bulan pertama 3×',goal[1]['reply'])
        self.assertIn('bulan ketiga 5×',goal[1]['reply'])
        payload={'operationId':'http-sale','mode':'direct','channel':'Toko langsung','method':'Tunai',
            'tendered':p['price'],'lines':[{'id':p['id'],'qty':1,'price':p['price']}]}
        self.assertEqual(self.request('/api/action/sale',payload,{'X-CSRF':''})[0],403)
        self.assertEqual(self.request('/api/action/sale',payload,{'Origin':'https://untrusted.example'})[0],403)
        one=self.request('/api/action/sale',payload);two=self.request('/api/action/sale',payload)
        self.assertEqual(one[0],200);self.assertEqual(one,two)
        self.assertEqual(self.request('/api/operations/http-sale')[1]['id'],one[1]['id'])
        self.assertEqual(self.request('/api/state',None,{'Host':'attacker.example'})[0],403)
        self.assertEqual(self.request('/api/action/user-password',{'operationId':'host-password','id':'host1','password':'host-test-password'})[0],200)
        self.assertEqual(self.request('/api/logout',{})[0],200)
        self.assertEqual(self.request('/api/login',{'id':'host1','password':'host-test-password'})[0],200)
        _,host=self.request('/api/state');self.csrf=host['user']['csrf']
        self.assertEqual(host['user']['name'],'Feby');self.assertEqual(host['orders'],[])
        self.assertNotIn('cost',host['products'][0])
        self.assertEqual(self.request('/api/assistant',{'question':'Berapa omzet saya?'})[0],403)
        payload['operationId']='host-denied'
        self.assertEqual(self.request('/api/action/sale',payload)[0],403)
        self.assertEqual(self.request('/api/action/connect-bigseller',{'appId':'test','appKey':'test'})[0],403)

if __name__=='__main__':unittest.main()
