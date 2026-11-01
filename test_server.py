import concurrent.futures
import json
from pathlib import Path
import tempfile
import unittest
import uuid
from server import Store, Problem, TEAM
from bigseller import parse_response, protect

class BusinessTests(unittest.TestCase):
    def setUp(self):
        self.testdir=Path(__file__).resolve().parent/'data-tests'
        self.testdir.mkdir(exist_ok=True)
        self.dbpath=self.testdir/('test-'+uuid.uuid4().hex+'.sqlite3')
        self.store=Store(self.dbpath)
        self.store.setup({'password':'test-only-password-123','demo':True})
        self.owner={'id':'owner','role':'owner','name':'Owner'}
        self.admin={'id':'admin','role':'admin','name':'Upi'}
        self.host={'id':'host1','role':'host','name':'Feby'}
        self.products=self.store.state(self.owner)['products']
    def tearDown(self):
        for suffix in ('','-wal','-shm'):
            p=Path(str(self.dbpath)+suffix)
            assert p.resolve().parent==self.testdir.resolve()
            p.unlink(missing_ok=True)
    def action(self,action,payload,user=None):
        return self.store.change(user or self.owner,action,dict(operationId=str(uuid.uuid4()),**payload))
    def sale(self,product=None,qty=1):
        p=product or self.products[0]
        return {'lines':[{'id':p['id'],'qty':qty,'price':p['price'],'discount':0}],
                'mode':'direct','channel':'Toko langsung','method':'Tunai','tendered':p['price']*qty}
    def test_named_team(self):
        self.assertEqual([u[1] for u in TEAM],['Owner','Upi','Feby','Tantri','Bowo'])
        self.assertEqual(sum(u[2]=='host' for u in TEAM),3)
    def test_sale_and_idempotency(self):
        payload=dict(operationId='same-operation',**self.sale(qty=2))
        one=self.store.change(self.owner,'sale',payload)
        self.assertEqual(one,self.store.change(self.owner,'sale',payload))
        state=self.store.state(self.owner)
        self.assertEqual(len(state['orders']),1)
        self.assertEqual(state['products'][0]['stock'],self.products[0]['stock']-2)
        self.assertEqual(len(state['syncTasks']),1)
        payload['customer']='Different body'
        with self.assertRaises(Problem): self.store.change(self.owner,'sale',payload)
    def test_multiline_rollback(self):
        payload=self.sale()
        p=self.products[1]
        payload['lines'].append({'id':p['id'],'qty':999,'price':p['price']})
        with self.assertRaises(Problem): self.action('sale',payload)
        state=self.store.state(self.owner)
        self.assertEqual(state['orders'],[])
        self.assertEqual(state['products'][0]['stock'],self.products[0]['stock'])
    def test_last_unit_concurrency(self):
        p=next(p for p in self.products if p['stock']==1)
        def buy(_):
            try: self.action('sale',self.sale(p)); return True
            except Problem: return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results=list(pool.map(buy,range(6)))
        self.assertEqual(sum(results),1)
        self.assertEqual(next(x for x in self.store.state(self.owner)['products'] if x['id']==p['id'])['stock'],0)
    def test_host_denied_and_costs_hidden(self):
        with self.assertRaises(Problem) as error: self.action('sale',self.sale(),self.host)
        self.assertEqual(error.exception.status,403)
        state=self.store.state(self.host)
        self.assertEqual(state['orders'],[])
        self.assertNotIn('cost',state['products'][0])
        self.assertTrue(all(t['assignee']=='host1' for t in state['tasks']))
    def test_admin_price_control(self):
        payload=self.sale(); payload['lines'][0]['discount']=1
        with self.assertRaises(Problem): self.action('sale',payload,self.admin)
    def test_always_full_payment(self):
        payload=self.sale();payload['tendered']=1
        with self.assertRaises(Problem):self.action('sale',payload)
        payload=self.sale();payload['mode']='reserve'
        with self.assertRaises(Problem):self.action('sale',payload)
        payload=self.sale();payload['method']='QRIS';payload['reference']=''
        with self.assertRaises(Problem):self.action('sale',payload)
    def test_admin_adjust_requires_owner_and_sync(self):
        p=self.products[0]
        r=self.action('adjust',{'id':p['id'],'version':p['version'],'stock':10,'quarantine':0,'reason':'Opname'},self.admin)
        self.assertEqual(self.store.state(self.owner)['products'][0]['stock'],p['stock'])
        self.action('approve',{'id':r['id'],'accept':True})
        state=self.store.state(self.owner)
        self.assertEqual(state['products'][0]['stock'],10)
        self.assertEqual(len(state['syncTasks']),1)
        with self.assertRaises(Problem):self.action('approve',{'id':r['id'],'accept':True})
    def test_return_damaged_and_refund_limits(self):
        p=self.products[0];self.action('sale',self.sale(p,2))
        o=self.store.state(self.owner)['orders'][0]
        self.action('return',{'id':o['id'],'version':o['version'],'product':p['id'],'qty':1,'condition':'Rusak','reason':'Diterima rusak'})
        state=self.store.state(self.owner); o=state['orders'][0]
        fresh=next(x for x in state['products'] if x['id']==p['id'])
        self.assertEqual(fresh['stock'],p['stock']-1)
        self.assertEqual(fresh['quarantine'],1)
        self.assertEqual(o['refundable'],p['price'])
        with self.assertRaises(Problem):self.action('refund',{'id':o['id'],'version':o['version'],'amount':o['total'],'reason':'Refund'})
    def test_campaign_and_expense(self):
        self.action('campaign',{'title':'Campaign A','channel':'Shopee','budget':1000,'cost':100})
        self.action('expense',{'title':'Packing','amount':1000,'category':'Kemasan'})
        state=self.store.state(self.owner)
        self.assertEqual(len(state['campaigns']),1)
        self.assertEqual(len(state['expenses']),1)
    def test_password_and_session(self):
        token=self.store.login('owner','test-only-password-123')
        self.assertEqual(self.store.session(token)['role'],'owner')
        with self.assertRaises(Problem):self.store.login('admin','test-only-password-123')
        self.action('user-password',{'id':'admin','password':'admin-test-pass-123'})
        self.assertEqual(self.store.session(self.store.login('admin','admin-test-pass-123'))['name'],'Upi')
    def test_baseline_and_sync(self):
        self.action('baseline',{'amount':100000,'scope':'Penjualan per 30 hari','start':'2026-11-01'})
        self.action('sale',self.sale())
        state=self.store.state(self.owner)
        self.assertEqual(state['targets'],[{'month':1,'multiple':3},{'month':3,'multiple':5}])
        self.action('sync-confirm',{'id':state['syncTasks'][0]['id'],'evidence':'Nomor dokumen BigSeller contoh'})
        self.assertEqual(self.store.state(self.owner)['syncTasks'][0]['status'],'Diverifikasi manual')
    def test_mcp_parsing(self):
        self.assertEqual(parse_response('data: {"result":{"tools":[]}}\n\n')['result']['tools'],[])
        with self.assertRaises(ValueError):parse_response('not json')

if __name__=='__main__':unittest.main()
