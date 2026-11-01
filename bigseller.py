"""Official BigSeller MCP handshake only; never assumes inventory write access."""
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

URL='https://mcp.bigseller.pro/mcp'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise ValueError('BigSeller mengalihkan alamat. Kredensial tidak diteruskan; verifikasi endpoint resmi.')

def protect(data):
    if os.name!='nt':
        raise ValueError('Penyimpanan key terenkripsi ini membutuhkan Windows DPAPI.')
    class Blob(ctypes.Structure):
        _fields_=[('cbData',wintypes.DWORD),('pbData',ctypes.POINTER(ctypes.c_ubyte))]
    raw=ctypes.create_string_buffer(data)
    source=Blob(len(data),ctypes.cast(raw,ctypes.POINTER(ctypes.c_ubyte)))
    target=Blob()
    crypt=ctypes.windll.crypt32.CryptProtectData
    crypt.argtypes=[ctypes.POINTER(Blob),wintypes.LPCWSTR,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,wintypes.DWORD,ctypes.POINTER(Blob)]
    crypt.restype=wintypes.BOOL
    if not crypt(ctypes.byref(source),'Albina BigSeller',None,None,None,1,ctypes.byref(target)):
        raise ValueError('Windows tidak dapat mengenkripsi key. Tidak ada key yang disimpan.')
    try: return ctypes.string_at(target.pbData,target.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree.argtypes=[ctypes.c_void_p]
        ctypes.windll.kernel32.LocalFree(ctypes.cast(target.pbData,ctypes.c_void_p))

def parse_response(body):
    try: return json.loads(body)
    except json.JSONDecodeError:
        for event in body.split('\n\n'):
            data='\n'.join(line[5:].lstrip() for line in event.splitlines() if line.startswith('data:'))
            if data:
                try:
                    result=json.loads(data)
                    if 'result' in result or 'error' in result: return result
                except json.JSONDecodeError: continue
        raise ValueError('Respons MCP tidak dikenali. Periksa aktivasi layanan dengan BigSeller.')

def verify_and_store(app_id,app_key,directory):
    if not isinstance(app_id,str) or not isinstance(app_key,str) or not 1<=len(app_id)<=300 or not 1<=len(app_key)<=1000:
        raise ValueError('APP ID dan APP KEY wajib diisi dengan nilai yang valid.')
    if any(c in app_id+app_key for c in '\r\n'):
        raise ValueError('Kredensial tidak valid.')
    headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream','app-id':app_id,'app-key':app_key}
    def request(payload,notification=False):
        req=urllib.request.Request(URL,data=json.dumps(payload).encode(),headers=headers,method='POST')
        try:
            with urllib.request.build_opener(NoRedirect).open(req,timeout=15) as response:
                session=response.headers.get('Mcp-Session-Id')
                if session: headers['Mcp-Session-Id']=session
                body=response.read(1000000).decode('utf-8').replace('\r\n','\n')
                if notification: return {}
                value=parse_response(body)
                if 'error' in value: raise ValueError('BigSeller menolak negosiasi MCP. Periksa izin akun dan aktivasi layanan.')
                return value.get('result',{})
        except urllib.error.HTTPError as exc:
            raise ValueError(f'BigSeller mengembalikan HTTP {exc.code}. Periksa APP ID/KEY dan aktivasi layanan.') from None
        except (urllib.error.URLError,TimeoutError):
            raise ValueError('BigSeller belum dapat dijangkau. Koneksi belum dinyatakan berhasil.') from None
    initialized=request({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'AlbinaLocal','version':'0.1'}}})
    if not initialized.get('protocolVersion'): raise ValueError('Negosiasi MCP tidak lengkap.')
    headers['MCP-Protocol-Version']=initialized['protocolVersion']
    request({'jsonrpc':'2.0','method':'notifications/initialized'},True)
    tools=request({'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}})
    if not isinstance(tools.get('tools'),list): raise ValueError('BigSeller belum memberikan daftar kemampuan MCP.')
    encrypted=protect(json.dumps({'appId':app_id,'appKey':app_key}).encode())
    path=Path(directory)/'bigseller-key.dpapi'
    tmp=path.with_suffix('.tmp')
    tmp.write_bytes(encrypted); tmp.replace(path)
    return {'connected':True,'tools':[t['name'] for t in tools['tools'] if isinstance(t.get('name'),str)],
            'message':'MCP terverifikasi dan key tersimpan dengan Windows DPAPI. Tulis stok otomatis belum diaktifkan; perlu adapter dan izin API.'}
