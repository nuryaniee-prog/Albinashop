"""Albina local workspace. Python standard library only; binds to loopback."""
import argparse
import csv
import hashlib
import hmac
import io
import json
import mimetypes
import secrets
import sqlite3
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from bigseller import verify_and_store

BASE = Path(__file__).resolve().parent
WIB = timezone(timedelta(hours=7))
TEAM = [('owner', 'Owner', 'owner'), ('admin', 'Upi', 'admin'),
        ('host1', 'Feby', 'host'), ('host2', 'Tantri', 'host'), ('host3', 'Bowo', 'host')]

class Problem(Exception):
    def __init__(self, message, status=422):
        super().__init__(message)
        self.status = status

def need(condition, message, status=422):
    if not condition:
        raise Problem(message, status)

def number(value, minimum=0, maximum=10**12):
    need(type(value) is int and minimum <= value <= maximum, 'Angka harus bulat dan berada dalam batas yang valid.')
    return value

def text(value, maximum=200, required=False):
    need(isinstance(value, str), 'Teks tidak valid.')
    value = value.strip()
    need(len(value) <= maximum and (value or not required), 'Teks wajib diisi atau terlalu panjang.')
    return value

def now():
    return datetime.now(timezone.utc).isoformat()

def password_hash(password):
    need(isinstance(password, str) and 10 <= len(password) <= 200, 'Password harus 10–200 karakter.')
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 260000).hex()
    return salt + ':' + digest

def password_ok(password, stored):
    if not stored or not isinstance(password, str) or len(password) > 200:
        return False
    salt, digest = stored.split(':', 1)
    test = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 260000).hex()
    return hmac.compare_digest(test, digest)

class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as c:
            c.executescript('''
              PRAGMA journal_mode=WAL;
              CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,name TEXT NOT NULL,role TEXT NOT NULL,password TEXT);
              CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id TEXT REFERENCES users(id),csrf TEXT,expires REAL);
              CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT);
              CREATE TABLE IF NOT EXISTS products(id TEXT PRIMARY KEY,sku TEXT UNIQUE NOT NULL,name TEXT NOT NULL,variant TEXT,
                stock INTEGER NOT NULL CHECK(stock>=0),reserved INTEGER NOT NULL DEFAULT 0 CHECK(reserved>=0),
                quarantine INTEGER NOT NULL DEFAULT 0 CHECK(quarantine>=0 AND quarantine<=stock),
                price INTEGER NOT NULL CHECK(price>0),cost INTEGER,threshold INTEGER NOT NULL DEFAULT 5,version INTEGER NOT NULL DEFAULT 1);
              CREATE TABLE IF NOT EXISTS orders(id TEXT PRIMARY KEY,created TEXT,actor TEXT REFERENCES users(id),customer TEXT,channel TEXT,
                lines TEXT,total INTEGER,paid INTEGER DEFAULT 0,refunded INTEGER DEFAULT 0,refundable INTEGER DEFAULT 0,
                method TEXT,reference TEXT,tendered INTEGER DEFAULT 0,status TEXT,version INTEGER DEFAULT 1);
              CREATE TABLE IF NOT EXISTS movements(id INTEGER PRIMARY KEY AUTOINCREMENT,created TEXT,actor TEXT,sku TEXT,
                kind TEXT,delta INTEGER,reserved_delta INTEGER DEFAULT 0,reference TEXT,reason TEXT);
              CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,created TEXT,actor TEXT,action TEXT,reference TEXT,details TEXT);
              CREATE TABLE IF NOT EXISTS operations(id TEXT PRIMARY KEY,actor TEXT,hash TEXT,result TEXT);
              CREATE TABLE IF NOT EXISTS approvals(id TEXT PRIMARY KEY,created TEXT,actor TEXT,action TEXT,payload TEXT,status TEXT,decision_by TEXT);
              CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY,title TEXT,assignee TEXT REFERENCES users(id),due TEXT,status TEXT,notes TEXT DEFAULT '');
              CREATE TABLE IF NOT EXISTS live(id TEXT PRIMARY KEY,title TEXT,host TEXT REFERENCES users(id),start TEXT,end TEXT,
                products TEXT,views INTEGER,orders_count INTEGER,revenue INTEGER,status TEXT DEFAULT 'Persiapan');
              CREATE TABLE IF NOT EXISTS campaigns(id TEXT PRIMARY KEY,title TEXT,channel TEXT,budget INTEGER,cost INTEGER,status TEXT);
              CREATE TABLE IF NOT EXISTS expenses(id TEXT PRIMARY KEY,created TEXT,title TEXT,amount INTEGER,category TEXT);
              CREATE TABLE IF NOT EXISTS sync_tasks(id TEXT PRIMARY KEY,created TEXT,action TEXT,reference TEXT,status TEXT,evidence TEXT);
              CREATE INDEX IF NOT EXISTS orders_created ON orders(created);
              CREATE INDEX IF NOT EXISTS movements_sku ON movements(sku,created);
            ''')
            for uid, name, _ in TEAM:
                c.execute('UPDATE users SET name=? WHERE id=?',(name,uid))

    @contextmanager
    def connect(self):
        c = sqlite3.connect(self.path, timeout=10)
        c.row_factory = sqlite3.Row
        c.execute('PRAGMA foreign_keys=ON')
        try:
            with c:
                yield c
        finally:
            c.close()

    def audit(self, c, user, action, ref, details=''):
        c.execute('INSERT INTO audit(created,actor,action,reference,details) VALUES(?,?,?,?,?)',
                  (now(), user['id'], action, ref, details))

    def setting(self, c, key, default=None):
        r = c.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
        return json.loads(r['value']) if r else default

    def set_setting(self, c, key, value):
        c.execute('INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, json.dumps(value)))

    def setup(self, payload):
        hashed = password_hash(payload.get('password'))
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            need(c.execute('SELECT count(*) FROM users').fetchone()[0] == 0, 'Workspace sudah diaktifkan.', 409)
            for uid, name, role in TEAM:
                c.execute('INSERT INTO users VALUES(?,?,?,?)', (uid, name, role, hashed if uid == 'owner' else None))
            demo = payload.get('demo') is True
            self.set_setting(c, 'demo', demo)
            self.set_setting(c, 'baseline', None)
            self.set_setting(c, 'baseline_scope', '')
            self.set_setting(c, 'start_date', '')
            if demo:
                examples = [('ALB-001-M','Kaos Sporty Dewasa','Olive · M',24,85000,55000),
                            ('ALB-002-6','Dress Brukat Anak','Cream · 6 tahun',3,125000,80000),
                            ('ALB-003-S','Kaos Crop Anak','Peach · S',35,55000,34000),
                            ('ALB-004-L','Celana Chinos Dewasa','Sand · L',1,115000,72000),
                            ('ALB-005-8','Setelan Katun Anak','Sage · 8 tahun',18,95000,61000)]
                for sku,name,variant,stock,price,cost in examples:
                    c.execute('INSERT INTO products(id,sku,name,variant,stock,price,cost) VALUES(?,?,?,?,?,?,?)',
                              (str(uuid.uuid4()),sku,name,variant,stock,price,cost))
                    c.execute('INSERT INTO movements(created,actor,sku,kind,delta,reference,reason) VALUES(?,?,?,?,?,?,?)',
                              (now(),'owner',sku,'Saldo contoh',stock,'SETUP','Katalog contoh, bukan hasil opname aktual'))
            for i,(title,uid) in enumerate([('Cocokkan saldo awal dengan fisik gudang','admin'),
                ('Siapkan produk untuk live pertama','host1'),('Tinjau koleksi dewasa','host2'),
                ('Siapkan daftar produk stok lama','host3')]):
                c.execute('INSERT INTO tasks(id,title,assignee,due,status) VALUES(?,?,?,?,?)', (str(i),title,uid,'','Belum mulai'))
            self.audit(c, {'id':'owner'}, 'Workspace dibuat', 'SETUP', 'Tim tetap: 1 owner, 3 host, 1 admin')
        return {'ok': True}

    def public_status(self):
        with self.connect() as c:
            return {'setup': c.execute('SELECT count(*) FROM users').fetchone()[0] == 0}

    def login(self, uid, password):
        with self.connect() as c:
            user = c.execute('SELECT * FROM users WHERE id=?', (uid,)).fetchone()
            need(user is not None and password_ok(password, user['password']), 'Akun atau password tidak sesuai. Akun tim perlu diaktifkan owner.', 401)
            token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(24)
            c.execute('DELETE FROM sessions WHERE expires<?', (time.time(),))
            c.execute('INSERT INTO sessions VALUES(?,?,?,?)', (hashlib.sha256(token.encode()).hexdigest(),uid,csrf,time.time()+43200))
            return token

    def session(self, token):
        with self.connect() as c:
            row = c.execute('SELECT u.id,u.name,u.role,s.csrf FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token=? AND s.expires>?',
                (hashlib.sha256(token.encode()).hexdigest(),time.time())).fetchone()
            need(row is not None, 'Silakan masuk ke workspace.', 401)
            return dict(row)

    def state(self, user):
        with self.connect() as c:
            c.execute('BEGIN')
            rows = lambda table: [dict(r) for r in c.execute('SELECT * FROM '+table)]
            products = rows('products')
            if user['role'] != 'owner':
                for p in products: p.pop('cost', None)
            result={'user':user,'demo':self.setting(c,'demo'), 'products':products,
                'users':[{'id':r['id'],'name':r['name'],'role':r['role'],'active':bool(r['password'])} for r in c.execute('SELECT * FROM users')],
                'baseline':self.setting(c,'baseline'),'baselineScope':self.setting(c,'baseline_scope',''),
                'startDate':self.setting(c,'start_date',''),'targets':[{'month':1,'multiple':3},{'month':3,'multiple':5}]}
            result['bigseller']=self.setting(c,'bigseller',{'connected':False}) if user['role']=='owner' else {'connected':False}
            result['tasks']=[t for t in rows('tasks') if user['role']!='host' or t['assignee']==user['id']]
            result['live']=[l for l in rows('live') if user['role']!='host' or l['host']==user['id']]
            result['campaigns']=rows('campaigns') if user['role']!='host' else []
            result['orders']=[]
            result['movements']=[]
            result['audit']=[]
            result['approvals']=[]
            result['expenses']=[]
            result['syncTasks']=[]
            if user['role']!='host':
                for o in c.execute('SELECT * FROM orders ORDER BY created DESC LIMIT 500'):
                    item=dict(o); item['lines']=json.loads(item['lines'])
                    if user['role']!='owner':
                        for line in item['lines']: line.pop('cost',None)
                    result['orders'].append(item)
                result['movements']=[dict(r) for r in c.execute('SELECT * FROM movements ORDER BY id DESC LIMIT 200')]
                result['approvals']=rows('approvals')
                result['syncTasks']=rows('sync_tasks')
                result['audit']=[dict(r) for r in c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 100')]
                if user['role']=='owner': result['expenses']=rows('expenses')
            return result

    def movement(self,c,user,p,kind,delta,reserved_delta,ref,reason=''):
        c.execute('INSERT INTO movements(created,actor,sku,kind,delta,reserved_delta,reference,reason) VALUES(?,?,?,?,?,?,?,?)',
                  (now(),user['id'],p['sku'],kind,delta,reserved_delta,ref,reason))

    def change(self, user, action, payload):
        operation = text(payload.get('operationId',''), 100, True)
        digest=hashlib.sha256(json.dumps({'action':action,'payload':payload},sort_keys=True).encode()).hexdigest()
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            current=c.execute('SELECT id,name,role FROM users WHERE id=?',(user['id'],)).fetchone()
            need(current is not None,'Akun tidak tersedia.',401)
            user=dict(current)
            old=c.execute('SELECT * FROM operations WHERE id=?',(operation,)).fetchone()
            if old:
                need(old['actor']==user['id'] and old['hash']==digest,'Identitas operasi sudah dipakai untuk data berbeda.',409)
                return json.loads(old['result'])
            result=self.command(c,user,action,payload)
            if action in ('sale','receive','adjust','return') and not result.get('message','').startswith('Pengajuan'):
                c.execute('INSERT INTO sync_tasks VALUES(?,?,?,?,?,?)',(str(uuid.uuid4()),now(),action,result.get('id',''),'Menunggu',''))
            c.execute('INSERT INTO operations VALUES(?,?,?,?)',(operation,user['id'],digest,json.dumps(result)))
            self.audit(c,user,action,result.get('id',''),result.get('message',''))
            return result

    def command(self,c,user,action,b):
        owner=user['role']=='owner'
        operational=user['role'] in ('owner','admin')
        uid=user['id']
        if action=='task-status':
            task=c.execute('SELECT * FROM tasks WHERE id=?',(b.get('id'),)).fetchone()
            need(task is not None,'Tugas tidak ditemukan.',404)
            need(operational or task['assignee']==uid,'Tidak memiliki akses ke tugas ini.',403)
            status=b.get('status'); need(status in ('Belum mulai','Dikerjakan','Terhambat','Selesai'),'Status tidak valid.')
            c.execute('UPDATE tasks SET status=?,notes=? WHERE id=?',(status,text(b.get('notes',''),500),task['id']))
            return {'id':task['id'],'message':'Status tugas diperbarui.'}
        if action=='live-result':
            l=c.execute('SELECT * FROM live WHERE id=?',(b.get('id'),)).fetchone()
            need(l is not None,'Sesi tidak ditemukan.',404)
            need(operational or l['host']==uid,'Tidak memiliki akses sesi ini.',403)
            c.execute('UPDATE live SET views=?,orders_count=?,revenue=?,status=? WHERE id=?',
                (number(b.get('views')),number(b.get('orders_count')),number(b.get('revenue')),'Selesai',l['id']))
            return {'id':l['id'],'message':'Hasil sesi manual dicatat.'}
        need(operational,'Tindakan hanya tersedia bagi owner/admin.',403)
        if action=='approve':
            need(owner,'Persetujuan hanya oleh owner.',403)
            req=c.execute('SELECT * FROM approvals WHERE id=?',(b.get('id'),)).fetchone()
            need(req is not None and req['status']=='Menunggu','Pengajuan sudah diproses atau tidak ditemukan.',409)
            if b.get('accept') is True:
                inner=json.loads(req['payload'])
                result=self.command(c,user,req['action'],inner)
                if req['action'] in ('adjust','return'):
                    c.execute('INSERT INTO sync_tasks VALUES(?,?,?,?,?,?)',(str(uuid.uuid4()),now(),req['action'],result.get('id',''),'Menunggu',''))
                state='Disetujui'
                self.audit(c,user,'Setujui '+req['action'],req['id'],f"Pengaju: {req['actor']}")
            else: result={}; state='Ditolak'
            c.execute('UPDATE approvals SET status=?,decision_by=? WHERE id=?',(state,uid,req['id']))
            return {'id':req['id'],'message':'Pengajuan '+state.lower()+'.','result':result}
        if action in ('cancel','return','adjust','refund') and not owner:
            text(b.get('reason',''),500,True)
            ref=str(uuid.uuid4())
            c.execute('INSERT INTO approvals VALUES(?,?,?,?,?,?,?)',(ref,now(),uid,action,json.dumps(b),'Menunggu',None))
            return {'id':ref,'message':'Pengajuan menunggu persetujuan owner. Stok belum berubah.'}
        if action=='sale':
            lines=b.get('lines')
            need(isinstance(lines,list) and 1<=len(lines)<=20,'Keranjang harus berisi 1–20 SKU.')
            need(b.get('channel') in ('Toko langsung','WhatsApp','Reseller'),'Channel tidak valid.')
            need(b.get('mode')=='direct','POS offline hanya menerima pembayaran lunas dan penyerahan langsung.')
            parsed=[]; seen=set(); total=0
            for line in lines:
                p=c.execute('SELECT * FROM products WHERE id=?',(line.get('id'),)).fetchone()
                need(p is not None,'Produk tidak ditemukan.')
                need(p['id'] not in seen,'SKU duplikat; gabungkan jumlahnya.')
                seen.add(p['id']); q=number(line.get('qty'),1,100000)
                price=number(line.get('price'),1); discount=number(line.get('discount',0),0,price*q)
                need(owner or (price==p['price'] and discount==0),'Harga khusus/diskon hanya dapat dikonfirmasi owner.',403)
                if price!=p['price'] or discount:
                    text(b.get('reason',''),500,True)
                avail=p['stock']-p['reserved']-p['quarantine']
                need(q<=avail,f"Stok {p['name']} · {p['variant']} tidak cukup. Tersedia {avail} pcs.",409)
                net=number(q*price-discount)
                total+=net
                parsed.append({'id':p['id'],'sku':p['sku'],'name':p['name'],'variant':p['variant'],'qty':q,
                               'price':price,'discount':discount,'net':net,'cost':p['cost'],'returned':0})
            number(total,1)
            direct=b['mode']=='direct'
            tendered,method,reference=(self.payment(b,total) if direct else (0,'',''))
            ref='OFF-'+uuid.uuid4().hex[:12].upper()
            for line in parsed:
                q=line['qty']; p=c.execute('SELECT * FROM products WHERE id=?',(line['id'],)).fetchone()
                c.execute('UPDATE products SET stock=stock-?,reserved=reserved+?,version=version+1 WHERE id=?',
                          (q if direct else 0,0 if direct else q,p['id']))
                self.movement(c,user,p,'Penjualan langsung' if direct else 'Reservasi',-q if direct else 0,0 if direct else q,ref)
            c.execute('INSERT INTO orders(id,created,actor,customer,channel,lines,total,paid,method,reference,tendered,status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                      (ref,now(),uid,text(b.get('customer',''),100),b['channel'],json.dumps(parsed),total,total if direct else 0,
                       method,reference,tendered,'Diserahkan' if direct else 'Dipesan'))
            return {'id':ref,'message':'Penjualan tersimpan.' if direct else 'Pesanan dan reservasi tersimpan.'}
        if action in ('pay','fulfill','cancel','return','refund'):
            o=c.execute('SELECT * FROM orders WHERE id=?',(b.get('id'),)).fetchone()
            need(o is not None,'Order tidak ditemukan.',404)
            need(o['version']==b.get('version'),'Order telah berubah. Muat ulang sebelum melanjutkan.',409)
            lines=json.loads(o['lines'])
            if action=='pay':
                need(o['status']=='Dipesan' and o['paid']==0,'Order sudah dibayar atau tidak dapat dibayar.',409)
                tendered,method,reference=self.payment(b,o['total'])
                c.execute('UPDATE orders SET paid=total,method=?,reference=?,tendered=?,version=version+1 WHERE id=?',
                          (method,reference,tendered,o['id']))
            elif action=='fulfill':
                need(o['status']=='Dipesan' and o['paid']==o['total'],'Order harus dipesan dan lunas sebelum diserahkan.',409)
                for line in lines:
                    p=c.execute('SELECT * FROM products WHERE id=?',(line['id'],)).fetchone(); q=line['qty']
                    need(p['reserved']>=q and p['stock']-p['quarantine']>=q,'Stok fisik/reservasi tidak cukup. Periksa gudang.',409)
                    c.execute('UPDATE products SET stock=stock-?,reserved=reserved-?,version=version+1 WHERE id=?',(q,q,p['id']))
                    self.movement(c,user,p,'Penyerahan',-q,-q,o['id'])
                c.execute("UPDATE orders SET status='Diserahkan',version=version+1 WHERE id=?",(o['id'],))
            elif action=='cancel':
                text(b.get('reason',''),500,True)
                need(o['status']=='Dipesan','Hanya order yang belum diserahkan dapat dibatalkan.',409)
                for line in lines:
                    p=c.execute('SELECT * FROM products WHERE id=?',(line['id'],)).fetchone(); q=line['qty']
                    need(p['reserved']>=q,'Reservasi tidak cocok.',409)
                    c.execute('UPDATE products SET reserved=reserved-?,version=version+1 WHERE id=?',(q,p['id']))
                    self.movement(c,user,p,'Pembatalan',0,-q,o['id'],b['reason'])
                c.execute("UPDATE orders SET status='Dibatalkan',refundable=paid,version=version+1 WHERE id=?",(o['id'],))
            elif action=='return':
                text(b.get('reason',''),500,True)
                need(o['status']=='Diserahkan','Barang belum diserahkan.',409)
                line=next((l for l in lines if l['id']==b.get('product')),None)
                need(line is not None,'Baris order tidak ditemukan.')
                q=number(b.get('qty'),1)
                need(q<=line['qty']-line['returned'],'Jumlah retur melebihi sisa yang dapat dikembalikan.',409)
                condition=b.get('condition'); need(condition in ('Layak jual','Rusak'),'Kondisi tidak valid.')
                p=c.execute('SELECT * FROM products WHERE id=?',(line['id'],)).fetchone()
                # Deterministic rupiah allocation: remainders go to earliest returned units.
                unit,remainder=divmod(line['net'],line['qty'])
                start=line['returned']; value=q*unit+max(0,min(q,remainder-start))
                line['returned']+=q
                c.execute('UPDATE products SET stock=stock+?,quarantine=quarantine+?,version=version+1 WHERE id=?',
                          (q,q if condition=='Rusak' else 0,p['id']))
                self.movement(c,user,p,'Retur '+condition,q,0,o['id'],b['reason'])
                c.execute('UPDATE orders SET lines=?,refundable=refundable+?,version=version+1 WHERE id=?',(json.dumps(lines),value,o['id']))
            elif action=='refund':
                text(b.get('reason',''),500,True)
                amount=number(b.get('amount'),1)
                need(amount<=o['refundable']-o['refunded'] and amount<=o['paid']-o['refunded'],'Nilai refund melebihi hak yang tersisa.',409)
                c.execute('UPDATE orders SET refunded=refunded+?,version=version+1 WHERE id=?',(amount,o['id']))
            return {'id':o['id'],'message':'Order diperbarui.'}
        if action in ('receive','adjust'):
            p=c.execute('SELECT * FROM products WHERE id=?',(b.get('id'),)).fetchone()
            need(p is not None,'Produk tidak ditemukan.',404)
            reason=text(b.get('reason',''),500,True)
            need(p['version']==b.get('version'),'Saldo sudah berubah. Muat ulang untuk koreksi.',409)
            if action=='receive':
                delta=number(b.get('qty'),1,100000); stock=p['stock']+delta; quarantine=p['quarantine']
            else:
                stock=number(b.get('stock'),0,100000); quarantine=number(b.get('quarantine'),0,stock); delta=stock-p['stock']
            c.execute('UPDATE products SET stock=?,quarantine=?,version=version+1 WHERE id=?',(stock,quarantine,p['id']))
            self.movement(c,user,p,'Barang masuk' if action=='receive' else 'Koreksi opname',delta,0,p['id'],reason)
            return {'id':p['id'],'message':'Mutasi stok dicatat.'}
        if action=='product':
            sku=text(b.get('sku',''),60,True).upper()
            name=text(b.get('name',''),150,True); variant=text(b.get('variant',''),100)
            stock=number(b.get('stock',0),0,100000); price=number(b.get('price'),1)
            cost=number(b['cost']) if owner and b.get('cost') is not None else None
            ref=str(uuid.uuid4())
            c.execute('INSERT INTO products(id,sku,name,variant,stock,price,cost) VALUES(?,?,?,?,?,?,?)',(ref,sku,name,variant,stock,price,cost))
            self.movement(c,user,{'sku':sku},'Saldo awal',stock,0,ref,'Produk baru; pastikan hasil hitung fisik')
            return {'id':ref,'message':'Produk dan saldo awal tersimpan.'}
        if action=='task':
            ref=str(uuid.uuid4()); assignee=b.get('assignee')
            need(c.execute('SELECT id FROM users WHERE id=?',(assignee,)).fetchone() is not None,'PIC tidak valid.')
            c.execute('INSERT INTO tasks(id,title,assignee,due,status) VALUES(?,?,?,?,?)',
                      (ref,text(b.get('title',''),180,True),assignee,text(b.get('due',''),30),'Belum mulai'))
            return {'id':ref,'message':'Tugas ditambahkan.'}
        if action=='live':
            host=c.execute("SELECT id FROM users WHERE id=? AND role='host'",(b.get('host'),)).fetchone()
            need(host is not None,'Pilih salah satu dari tiga host.')
            start=text(b.get('start',''),40,True); end=text(b.get('end',''),40,True)
            try:
                begin=datetime.fromisoformat(start); finish=datetime.fromisoformat(end)
                need(begin.tzinfo is not None and finish>begin,'Waktu sesi tidak valid.')
            except (ValueError,TypeError): raise Problem('Waktu sesi tidak valid.')
            ref=str(uuid.uuid4())
            c.execute('INSERT INTO live(id,title,host,start,end,products) VALUES(?,?,?,?,?,?)',
                (ref,text(b.get('title',''),150,True),host['id'],start,end,text(b.get('products',''),500)))
            return {'id':ref,'message':'Jadwal live ditambahkan.'}
        need(owner,'Fitur ini hanya tersedia bagi owner.',403)
        if action=='sync-confirm':
            evidence=text(b.get('evidence',''),500,True)
            r=c.execute('SELECT * FROM sync_tasks WHERE id=?',(b.get('id'),)).fetchone()
            need(r is not None and r['status']=='Menunggu','Catatan sudah diproses atau tidak ditemukan.',409)
            c.execute("UPDATE sync_tasks SET status='Diverifikasi manual',evidence=? WHERE id=?",(evidence,r['id']))
            return {'id':r['id'],'message':'Verifikasi manual BigSeller dicatat; bukan konfirmasi API.'}
        if action=='user-password':
            target=text(b.get('id',''),30,True)
            need(c.execute('SELECT id FROM users WHERE id=?',(target,)).fetchone() is not None,'Akun tidak ditemukan.')
            hashed=password_hash(b.get('password'))
            c.execute('UPDATE users SET password=? WHERE id=?',(hashed,target))
            c.execute('DELETE FROM sessions WHERE user_id=?',(target,))
            return {'id':target,'message':'Password akun diperbarui. Sesi akun tersebut diakhiri.'}
        if action=='baseline':
            amount=number(b.get('amount'),1)
            scope=text(b.get('scope',''),200,True); start=text(b.get('start',''),10,True)
            try: datetime.strptime(start,'%Y-%m-%d')
            except ValueError: raise Problem('Tanggal mulai tidak valid.')
            self.set_setting(c,'baseline',amount); self.set_setting(c,'baseline_scope',scope); self.set_setting(c,'start_date',start)
            return {'id':'baseline','message':'Baseline tersimpan; target tetap bulan 1: 3× dan bulan 3: 5×.'}
        if action=='campaign':
            ref=str(uuid.uuid4())
            c.execute('INSERT INTO campaigns VALUES(?,?,?,?,?,?)',(ref,text(b.get('title',''),150,True),
                text(b.get('channel',''),80,True),number(b.get('budget')),number(b.get('cost')), 'Draft'))
            return {'id':ref,'message':'Campaign dan biaya manual tersimpan.'}
        if action=='expense':
            ref=str(uuid.uuid4())
            c.execute('INSERT INTO expenses VALUES(?,?,?,?,?)',(ref,now(),text(b.get('title',''),150,True),number(b.get('amount'),1),text(b.get('category',''),80,True)))
            return {'id':ref,'message':'Pengeluaran dicatat.'}
        raise Problem('Tindakan tidak dikenal.',404)

    def payment(self,b,total):
        method=b.get('method')
        need(method in ('Tunai','Transfer bank','QRIS'),'Pilih metode pembayaran.')
        tender=number(b.get('tendered'),total)
        reference=text(b.get('reference',''),150,method!='Tunai')
        need(method=='Tunai' or tender==total,'Pembayaran non-tunai harus tepat sesuai total.')
        return tender,method,reference

class Handler(BaseHTTPRequestHandler):
    store = None
    failures = {}
    def log_message(self, fmt, *args):
        pass  # Do not log credentials, cookies or request bodies.

    def send(self,status,data,extra=None):
        raw=json.dumps(data,ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        for key,value in (extra or {}).items(): self.send_header(key,value)
        self.end_headers(); self.wfile.write(raw)

    def host_check(self):
        host=self.headers.get('Host','')
        allowed={f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}
        need(host in allowed,'Host tidak diizinkan.',403)
        origin=self.headers.get('Origin')
        need(not origin or origin in {'http://'+h for h in allowed},'Origin tidak diizinkan.',403)

    def token(self):
        cookie=SimpleCookie()
        try: cookie.load(self.headers.get('Cookie',''))
        except Exception: return ''
        return cookie['albina_session'].value if 'albina_session' in cookie else ''

    def do_GET(self):
        try:
            self.host_check(); path=urlparse(self.path).path
            if path=='/api/status': return self.send(200,self.store.public_status())
            if path=='/api/state': return self.send(200,self.store.state(self.store.session(self.token())))
            if path.startswith('/api/operations/'):
                user=self.store.session(self.token())
                with self.store.connect() as c:
                    op=c.execute('SELECT * FROM operations WHERE id=?',(path.removeprefix('/api/operations/'),)).fetchone()
                    need(op is not None,'Operasi belum ditemukan. Jangan membuat transaksi baru sebelum memeriksa riwayat.',404)
                    need(op['actor']==user['id'] or user['role']=='owner','Tidak memiliki akses.',403)
                    return self.send(200,json.loads(op['result']))
            if path.startswith('/api/'): raise Problem('Endpoint tidak ditemukan.',404)
            files={'/':'index.html','/app.js':'app.js','/style.css':'style.css','/assets/brand-board.png':'assets/brand-board.png','/assets/albina-shop-logo-hd.jpg':'assets/albina-shop-logo-hd.jpg'}
            need(path in files,'File tidak ditemukan.',404)
            p=BASE/'public'/files[path]; raw=p.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type',(mimetypes.guess_type(p.name)[0] or 'text/plain')+'; charset=utf-8')
            self.send_header('Content-Length',str(len(raw)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            self.end_headers(); self.wfile.write(raw)
        except Problem as e: self.send(e.status,{'error':str(e)})

    def do_POST(self):
        try:
            self.host_check()
            need(self.headers.get('Content-Type','').split(';')[0]=='application/json','Gunakan JSON.',415)
            length=int(self.headers.get('Content-Length','0')); need(0<length<=100000,'Payload tidak valid atau terlalu besar.',413)
            b=json.loads(self.rfile.read(length)); need(isinstance(b,dict),'Payload harus object.')
            path=urlparse(self.path).path
            if path=='/api/setup': return self.send(201,self.store.setup(b))
            if path=='/api/login':
                key=self.client_address[0]; cutoff=time.time()-300
                attempts=[t for t in self.failures.get(key,[]) if t>cutoff]
                need(len(attempts)<10,'Terlalu banyak percobaan masuk. Tunggu 5 menit.',429)
                try: token=self.store.login(b.get('id'),b.get('password'))
                except Problem:
                    self.failures[key]=attempts+[time.time()]; raise
                self.failures.pop(key,None)
                return self.send(200,{'ok':True},{'Set-Cookie':f'albina_session={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=43200'})
            user=self.store.session(self.token())
            need(hmac.compare_digest(self.headers.get('X-CSRF',''),user['csrf']),'Sesi form tidak valid. Muat ulang.',403)
            if path=='/api/assistant':
                question=text(b.get('question',''),500,True).lower()
                state=self.store.state(user)
                low=[p for p in state['products'] if p['stock']-p['reserved']-p['quarantine']<=p['threshold']]
                footer='\n\nSumber: database lokal saat ini. BigSeller belum menjadi sumber data live. Mode ini berbasis aturan, bukan model AI generatif.'
                if any(k in question for k in ('target','okr','tujuan')):
                    reply='Target tetap: bulan pertama 3× baseline dan bulan ketiga 5× baseline yang sama. Ini bukan 15× atau total kumulatif tiga bulan. Progres aktual perlu baseline dan data channel yang tervalidasi.'
                elif any(k in question for k in ('stok','barang','produk','sku')):
                    matches=[p for p in state['products'] if p['sku'].lower() in question or p['name'].lower() in question]
                    items=matches or low
                    reply=(f'{len(items)} SKU '+('yang cocok:' if matches else 'perlu perhatian:')+'\n'+'\n'.join(f"• {p['name']} · {p['variant']}: {p['stock']-p['quarantine']-p['reserved']} pcs tersedia lokal." for p in items[:10])) if items else 'Tidak ada SKU lokal di bawah ambang peringatan. Tetap cocokkan dengan stok BigSeller dan fisik.'
                elif any(k in question for k in ('omzet','omset','penjualan','transaksi','uang','laba','hpp','margin')):
                    need(user['role']!='host','Laporan keuangan bisnis tidak tersedia untuk akun host.',403)
                    amount=sum(o['paid'] for o in state['orders']); count=len(state['orders'])
                    nominal=f'{amount:,}'.replace(',','.')
                    reply=f'Pada maksimal 500 transaksi offline lokal terbaru, terdapat {count} transaksi, dengan pembayaran tercatat Rp{nominal}.\nIni bukan omzet seluruh channel, dana cair marketplace, atau laba bersih.'
                elif any(k in question for k in ('tim','host','tugas','live')):
                    unfinished=[t for t in state['tasks'] if t['status']!='Selesai']
                    reply='Tim Albina: Owner, Admin Upi, Host Feby, Host Tantri, Host Bowo. Total 5 orang, 3 host.\n'+f'{len(unfinished)} tugas belum selesai dalam cakupan akses akun ini.\n'+'\n'.join('• '+t['title'] for t in unfinished[:6])
                elif any(k in question for k in ('bigseller','sinkron','koneksi')):
                    pending=[t for t in state['syncTasks'] if t['status']=='Menunggu']
                    reply=f'{len(pending)} mutasi lokal menunggu pembaruan/verifikasi BigSeller dalam cakupan akun ini. Login web BigSeller tidak mengaktifkan API. APP ID dan APP KEY resmi diperlukan; MCP tidak otomatis memberi izin mengubah stok.'
                else:
                    reply='Saya bisa membantu memeriksa stok menipis, penjualan offline lokal, tugas tim, target 3×/5×, dan status BigSeller. Coba: “Stok mana yang menipis?” atau “Apa tugas saya?”'
                return self.send(200,{'reply':reply+footer,'mode':'local-rules','asOf':now()})
            if path=='/api/action/connect-bigseller':
                need(user['role']=='owner','Koneksi hanya dapat dikonfigurasi owner.',403)
                try: status=verify_and_store(b.get('appId'),b.get('appKey'),self.store.path.parent)
                except ValueError as e: raise Problem(str(e))
                status['verifiedAt']=now()
                with self.store.connect() as c:
                    self.store.set_setting(c,'bigseller',status)
                    self.store.audit(c,user,'Verifikasi MCP BigSeller','BIGSELLER','Daftar kemampuan diterima; tidak menulis stok.')
                return self.send(200,{'message':status['message']})
            if path=='/api/logout':
                with self.store.connect() as c: c.execute('DELETE FROM sessions WHERE token=?',(hashlib.sha256(self.token().encode()).hexdigest(),))
                return self.send(200,{'ok':True},{'Set-Cookie':'albina_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0'})
            need(path.startswith('/api/action/'),'Endpoint tidak ditemukan.',404)
            self.send(200,self.store.change(user,path.removeprefix('/api/action/'),b))
        except Problem as e: self.send(e.status,{'error':str(e)})
        except (ValueError,TypeError,KeyError,AttributeError): self.send(400,{'error':'Data permintaan tidak valid.'})
        except sqlite3.IntegrityError: self.send(409,{'error':'Data sudah ada atau perubahan melanggar aturan. Muat ulang dan periksa.'})
        except sqlite3.OperationalError: self.send(503,{'error':'Database sedang sibuk. Periksa hasil transaksi sebelum mencoba ulang.'})
        except Exception:
            self.send(500,{'error':'Penyimpanan belum dapat dipastikan. Periksa hasil transaksi sebelum mengulang.'})

def serve(db,port):
    Handler.store=Store(db)
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    print(f'Albina local: http://127.0.0.1:{port}',flush=True)
    print('Database lokal siap. Tekan Ctrl+C untuk menghentikan server.',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=4180)
    parser.add_argument('--db',default=str(BASE/'data/albina.sqlite3'))
    args=parser.parse_args()
    serve(args.db,args.port)
