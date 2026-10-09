#!/usr/bin/env python3
"""Repeatable offline PAA checks using temporary copies; never contact IBM.

Python 3.9+, Bash and POSIX PTYs. The optional original archives are NOT required.
Strict fake Bob is a test double, not a model/backend or proof of live tool policy.
"""
from __future__ import annotations
import argparse,contextlib,fcntl,hashlib,importlib.util,json,os,re,shutil,stat,subprocess,sys,tempfile,time,zipfile
from pathlib import Path
from decimal import Decimal
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;PKG=HERE.parent;APP=PKG/'use-cases/planning-analytics'
sys.path.insert(0,str(HERE));import test_inherited_display as inherited
RESULTS=[]
def check(ok,message='Assertion failed'):
 if not ok:raise AssertionError(message)
def record(name,fn):
 start=time.monotonic()
 try:fn();status='PASS';error=''
 except Exception as e:status='FAIL';error=type(e).__name__+': '+str(e)
 RESULTS.append({'name':name,'status':status,'seconds':round(time.monotonic()-start,3),'error':error})
 print(status+': '+name+(' -- '+error if error else ''),flush=True)
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(root):
 return {str(p.relative_to(root)):(sha(p.read_bytes()),stat.S_IMODE(p.stat().st_mode)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.is_symlink()}
def run(args,cwd=None,env=None,rc=0,text='',timeout=40):
 result=subprocess.run([str(x) for x in args],cwd=cwd,env=env,text=True,input=text,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
 check(result.returncode==rc,f'exit {result.returncode}, expected {rc}: '+result.stdout[-1200:]);return result.stdout
@contextlib.contextmanager
def changed(p,content):
 before=p.read_bytes();mode=p.stat().st_mode
 p.write_bytes(content.encode() if isinstance(content,str) else content)
 try:yield
 finally:p.write_bytes(before);p.chmod(stat.S_IMODE(mode))
def expect_error(fn,kind=Exception):
 try:fn()
 except kind:return
 raise AssertionError('Expected rejection')

def utility_tests(work):
 a=work/'utility';shutil.copytree(APP,a);m=module('paa_tool_tests',a/'.bob/planning-analytics-tools/pa-tool.py')
 t=a/'.bob/planning-analytics-templates';profile=json.loads((a/'.bob/planning-analytics-profiles/deployment-profile.example.json').read_text())
 record('Self-check needs neither Bob nor a network',lambda:check(json.loads(run(['bash',a/'paa-self-check.sh'],env={'PATH':os.environ['PATH'],'PYTHONDONTWRITEBYTECODE':'1'}))['status']=='PASS'))
 record('Example deployment profile requires explicit remaining review',lambda:check(m.profile_check(profile)['status']=='REVIEW_REQUIRED'))
 for offering in sorted(m.OFFERINGS):
  record('Distinct offering profile accepted as a workflow: '+offering,lambda offering=offering:check(m.profile_check(dict(profile,offering=offering))['status']!='INVALID'))
 for name,change in [('unknown offering',{'offering':'guess'}),('string production flag',{'production':'false'}),('preview production',{'production':True,'technical_preview':True}),('credentials in profile',{'api_key':'SYNTHETIC_SECRET'}),('absent component map',{'components':None})]:
  record('Reject '+name,lambda change=change:check(m.profile_check(dict(profile,**change))['status']=='INVALID'))
 record('Static configuration remains review-required, not live accepted',lambda:check(m.config_check((t/'tm1s.cfg.example').read_text())['status']=='REVIEW_REQUIRED'))
 for name,text in [('port collision','PortNumber=1234\nHTTPPortNumber=1234\nUseSSL=T'),('invalid port','HTTPPortNumber=70000\nUseSSL=T'),('TLS off','PortNumber=1234\nUseSSL=F'),('duplicate property','PortNumber=1\nPortNumber=2\nUseSSL=T'),('malformed line','bad\nUseSSL=T')]:
  record('Config rejects '+name,lambda text=text:check(m.config_check(text)['status']=='INVALID'))
 def csvfile(name,text):p=work/name;p.write_text(text);return str(p)
 s=str(t/'reconciliation-source.csv');d=str(t/'reconciliation-target.csv')
 record('Decimal reconciliation preserves sample totals and matches rows',lambda:check(m.reconcile(s,d,['Entity','Period'],'Amount','0.01')['source_total']=='300.30'))
 dup=csvfile('dups.csv','Entity,Amount\nA,1.10\nA,2.20\n');single=csvfile('single.csv','Entity,Amount\nA,3.30\n')
 record('Duplicate keys rejected unless aggregate explicitly requested',lambda:expect_error(lambda:m.reconcile(dup,single,['Entity'],'Amount','0.01'),m.ToolError))
 record('Explicit duplicate aggregation retains source row/duplicate accounting',lambda:check(m.reconcile(dup,single,['Entity'],'Amount','0.01',True)['source_duplicate_rows']==1))
 mismatch=csvfile('mismatch.csv','Entity,Amount\nA,3.40\n');missing=csvfile('missing.csv','Entity,Amount\nB,3.30\n')
 record('Mismatch detection is per matched business key',lambda:check(m.reconcile(single,mismatch,['Entity'],'Amount','0.01')['value_mismatches']==1))
 record('Missing keys are not hidden by equal grand totals',lambda:check(m.reconcile(single,missing,['Entity'],'Amount','0.01')['missing_target_keys']==1))
 for name,text in [('duplicate-headers','Entity,Amount,Amount\nA,1,1\n'),('nonfinite','Entity,Amount\nA,NaN\n'),('blank-key','Entity,Amount\n,1\n'),('missing-column','Entity,Other\nA,1\n')]:
  bad=csvfile(name+'.csv',text)
  record('CSV rejects '+name,lambda bad=bad:expect_error(lambda:m.reconcile(bad,single,['Entity'],'Amount','0.01'),m.ToolError))
 record('Extreme decimal exponent is rejected without overflow or raw-data traceback',lambda:expect_error(lambda:m.decimal('1e999999999'),m.ToolError))
 record('Excess decimal precision is rejected rather than silently rounded',lambda:expect_error(lambda:m.decimal('0.'+'1'*39),m.ToolError))
 record('Negative tolerance rejected',lambda:expect_error(lambda:m.reconcile(single,single,['Entity'],'Amount','-1'),m.ToolError))
 def score():
  out=m.evaluate(str(t/'forecast-evaluation.csv'));check(out['observations']==4 and Decimal(out['mae'])==Decimal('7.5'));check(out['mape_excluded_zero_actuals']==1 and out['training_performed'] is False)
 record('Forecast metrics tested on synthetic fixture with explicit zero exclusion',score)
 zeros=csvfile('zeros.csv','period,actual,predicted\nA,0,1\nB,0,2\n')
 record('Zero-denominator WAPE and all-zero MAPE are null',lambda:check(m.evaluate(zeros)['wape_percent'] is None and m.evaluate(zeros)['mape_percent_nonzero_actuals'] is None))
 record('Scaffold writes implementation contract to separate store',lambda:check(m.scaffold('test-model','saas',False)['path']=='bob-planning-analytics-store/test-model'))
 record('Design scaffold remains Markdown-only',lambda:check(m.scaffold('test-design','local',True)['files']==1))
 record('Scaffold refuses overwrite',lambda:expect_error(lambda:m.scaffold('test-model','saas',False),m.ToolError))
 record('Scaffold rejects traversal',lambda:expect_error(lambda:m.scaffold('../escape','saas',False),m.ToolError))
 outside=work/'outside.csv';outside.write_text('Entity,Amount\nA,1\n');link=work/'linked.csv';link.symlink_to(outside)
 record('Symlink data input refused',lambda:expect_error(lambda:m.safe_file(str(link)),m.ToolError))
 record('Evidence outside appliance store refused',lambda:expect_error(lambda:m.output_file(str(work/'evidence.json')),m.ToolError))
 out=a/'bob-planning-analytics-store/evidence.json'
 def emit_once():
  with contextlib.redirect_stdout(__import__('io').StringIO()):m.emit({'status':'PASS'},str(out))
  check(stat.S_IMODE(out.stat().st_mode)==0o777)
 record('Evidence is exclusive-create with requested 0777 mode',emit_once)
 record('Evidence existing file refused',lambda:expect_error(lambda:m.emit({'status':'PASS'},str(out)),m.ToolError))
 # Network never occurs in these negative cases. Patch opener to assert no outbound use.
 base=('https://approved.invalid/api/v1','saas',True,'PA_TM1_AUTHORIZATION',False,'PA_TM1_USER','PA_TM1_PASSWORD',None,5)
 with patch.dict(os.environ,{'PA_TM1_AUTHORIZATION':'Bearer OFFLINE_PA_ONLY','BOB_API_KEY':'OFFLINE_BOB_ONLY'},clear=False):
  for name,args in [('no connect',(base[0],base[1],False,*base[3:])),('HTTP',('http://approved.invalid/api/v1',*base[1:])),('URL credentials',('https://user:password@host/api/v1',*base[1:])),('missing API root',('https://host',*base[1:])),('Bob auth variable',(*base[:3],'BOB_API_KEY',*base[4:])),('SaaS Local Basic',(*base[:3],None,True,*base[5:])),('timeout bounds',(*base[:-1],61))]:
   record('REST rejects '+name+' before network',lambda args=args:expect_error(lambda:m.probe(*args),m.ToolError))
  class Response:
   status=200
   def __init__(self,body):self.body=body
   def __enter__(self):return self
   def __exit__(self,*x):pass
   def read(self,n):return self.body[:n]
  class Opener:
   def __init__(self,body):self.body=body;self.calls=[]
   def open(self,req,timeout):self.calls.append((req,timeout));return Response(self.body)
  opener=Opener(b'<edmx:Edmx xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx" Version="4.0"><edmx:DataServices/></edmx:Edmx>')
  def probeok():
   with patch.object(m.urllib.request,'build_opener',return_value=opener):result=m.probe(*base)
   req,timeout=opener.calls[-1];check(req.get_method()=='GET' and req.full_url.endswith('/api/v1/$metadata') and result['raw_payload_displayed'] is False)
  record('REST mocked metadata uses one GET; no raw response persisted/displayed',probeok)
  for name,body in [('DTD',b'<!DOCTYPE Edmx []><Edmx/>'),('wrong root',b'<html>not metadata</html>'),('oversize',b'x'*(1024*1024+1)),('bad XML',b'<Edmx')]:
   def badprobe(body=body):
    with patch.object(m.urllib.request,'build_opener',return_value=Opener(body)):expect_error(lambda:m.probe(*base),m.ToolError)
   record('REST withholds '+name,badprobe)
  record('Redirects never forward Authorization',lambda:expect_error(lambda:m.NoRedirect().redirect_request(None,None,302,'',{},'https://elsewhere.invalid'),m.ToolError))
  def reused_basic():
   with patch.dict(os.environ,{'PA_TM1_USER':'tester','PA_TM1_PASSWORD':'OFFLINE_BOB_ONLY'}):
    expect_error(lambda:m.probe(base[0],'local',True,None,True,'PA_TM1_USER','PA_TM1_PASSWORD',None,5),m.ToolError)
  record('Local Basic rejects Bob-key reuse before Base64 encoding',reused_basic)
 loopback_tests(work,m)


def loopback_tests(work,m):
 import http.server,ssl,threading
 cert=work/'loopback-cert.pem';key=work/'loopback-key.pem'
 if not shutil.which('openssl'):
  record('Local TLS fixture prerequisites',lambda:check(False,'OpenSSL CLI is required for the offline loopback TLS tests.'));return
 run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-keyout',key,'-out',cert,'-days','1','-subj','/CN=localhost','-addext','subjectAltName=DNS:localhost'],timeout=15)
 calls=[]
 class Handler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
   calls.append({'method':self.command,'path':self.path,'authorization':self.headers.get('Authorization')})
   if self.path.startswith('/redirect/'):
    self.send_response(302);self.send_header('Location','https://outside.invalid/api/v1/$metadata');self.end_headers();return
   self.send_response(200);self.send_header('Content-Type','application/xml');self.end_headers();self.wfile.write(b'<Edmx xmlns="http://docs.oasis-open.org/odata/ns/edmx" Version="4.0"/>')
  def log_message(self,*args):pass
 server=http.server.HTTPServer(('127.0.0.1',0),Handler)
 ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);ctx.load_cert_chain(str(cert),str(key));server.socket=ctx.wrap_socket(server.socket,server_side=True)
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 url='https://localhost:'+str(server.server_port)+'/api/v1'
 try:
  with patch.dict(os.environ,{'PA_TM1_AUTHORIZATION':'Bearer LOOPBACK_TEST_ONLY'}):
   def ok():
    result=m.probe(url,'local',True,'PA_TM1_AUTHORIZATION',False,'PA_TM1_USER','PA_TM1_PASSWORD',str(cert),5)
    check(result['tls_verified'] and result['raw_payload_displayed'] is False and calls[-1]['method']=='GET' and calls[-1]['path']=='/api/v1/$metadata')
   record('Actual local HTTPS metadata exchange verifies configured CA and returns only bounded outcome',ok)
   def untrusted():
    before=len(calls);expect_error(lambda:m.probe(url,'local',True,'PA_TM1_AUTHORIZATION',False,'PA_TM1_USER','PA_TM1_PASSWORD',None,5),m.ToolError);check(len(calls)==before)
   record('Actual local HTTPS refuses an untrusted certificate before application data',untrusted)
   def redirect():
    before=len(calls);expect_error(lambda:m.probe(url.replace('/api/v1','/redirect/api/v1'),'local',True,'PA_TM1_AUTHORIZATION',False,'PA_TM1_USER','PA_TM1_PASSWORD',str(cert),5),m.ToolError);check(len(calls)==before+1)
   record('Actual local HTTPS redirect is not followed to an external endpoint',redirect)
 finally:
  server.shutdown();server.server_close();thread.join(timeout=5)


def runtime_tests(work,target):
 fake=HERE/'fake-bob.py';log=work/'bob-calls.jsonl';home=work/'home';home.mkdir(exist_ok=True)
 env={'PATH':os.environ['PATH'],'HOME':str(home),'TERM':'xterm-256color','PYTHONDONTWRITEBYTECODE':'1','BOB2_BIN':str(fake),'BOB_BIN':str(fake),'BOB_API_KEY':'OFFLINE_TEST_KEY_NOT_REAL','FAKE_BOB_LOG':str(log),'LANG':'C.UTF-8'}
 def calls():return [json.loads(x) for x in log.read_text().splitlines()] if log.exists() else []
 record('Doctor validates PAA CLI and all primary mode rules without inference',lambda:check('PAA' in run(['bash',target/'xLaunchpad.sh','--doctor'],env=env,cwd=target)))
 record('Doctor did not invoke an auth/model probe',lambda:check(not calls()))
 def ui():
  out=inherited.tty_run(['bash',target/'xLaunchpad.sh','--preview'],env,target)
  expected=inherited.tty_run(['bash','-c','source "$1"; bob2_ui_init; bob2_ui_menu','bash',HERE/'expected-menu.sh'],env,target)
  check(out==expected,'ANSI menu bytes differ from expected label-only port')
 record('Production launchpad ANSI menu byte comparison',ui)
 routes=[('--chat','1','code'),('--ask','2','ask'),('--code','3','code'),('--design','4','advance'),('--resume','5','code')]
 for flag,choice,mode in routes:
  def route(flag=flag,choice=choice,mode=mode):
   args=['bash',target/'xLaunchpad.sh',flag]+(['Create a nonproduction planning example; no live actions.'] if flag in ('--ask','--code','--design') else [])
   out=run(args,env=env,cwd=target);latest=[x for x in calls() if not x['probe']][-1]
   check(latest['mode']==mode and latest['code']=='PAA' and latest['menu']==choice and latest['cwd']==str(target))
   check('RAW_' not in out and '[Evidence:' in out)
   check(all(s in out for s in ['Browse documentation libraries (completed)','Search Planning Analytics deployment documentation (completed)','Knowledgebase information retrieval (completed)']))
   if flag=='--resume':check(latest['resume']=='latest-user')
  record('Full launcher route with auth/TLS/retrieval handling: '+flag,route)
 def styles():
  out=inherited.tty_run(['bash',target/'xLaunchpad.sh','--chat'],dict(env,FAKE_NATIVE_UI='1',FAKE_CHAT_READ='1'),target,'yes\n','Approval question:')
  text=out.decode();check('INPUT_RECEIVED:yes' in text and 'RAW_' not in text and '\x1b[36m' in text and '\x1b[31m(auto-approve)' in text)
 record('Native PTY input/approval and cyan/red presentation preserved',styles)
 def auth_fail():
  before=len([x for x in calls() if not x['probe']]);out=run(['bash',target/'xLaunchpad.sh','--ask','no request on failure'],env=dict(env,FAKE_AUTH_FAIL='1'),cwd=target,rc=2)
  check(env['BOB_API_KEY'] not in out and len([x for x in calls() if not x['probe']])==before)
 record('Authentication failure is redacted and prevents task start',auth_fail)
 record('Bob 1.x refused without legacy fallback',lambda:run(['bash',target/'xLaunchpad.sh','--doctor'],env=dict(env,FAKE_BOB_VERSION='1.0.6'),cwd=target,rc=2))
 record('Missing v2 stream-json capability refuses unsafe invocation',lambda:run(['bash',target/'xLaunchpad.sh','--ask','test'],env=dict(env,FAKE_MISSING_FLAG='run:--format'),cwd=target,rc=2))
 record('Unknown mode does not fall back to generic Agent',lambda:run(['bash',target/'xLaunchpad.sh','--chat'],env=dict(env,BOB2_INTERACTIVE_MODE='nonexistent'),cwd=target,rc=2))
 record('Malformed structured output has no raw terminal fallback',lambda:check('RAW_SEARCH_PAYLOAD_MARKER' not in run(['bash',target/'xLaunchpad.sh','--ask','test'],env=dict(env,FAKE_MALFORMED_STREAM='1'),cwd=target,rc=2)))
 def specialist():
  run(['bash',target/'xLaunchpad.sh','--chat'],env=dict(env,BOB2_INTERACTIVE_MODE='tm1-modeler'),cwd=target);check([x for x in calls() if not x['probe']][-1]['mode']=='tm1-modeler')
 record('New TM1 specialist mode is actually routable by native runtime',specialist)
 def tls():
  check(all(not x['tls_disabled'] for x in calls()),'TLS disabled in a subprocess')
  probes=[x for x in calls() if x['probe']];check(probes and all(x['workspace'] and x['workspace']!=str(target) and '--disable-mcp' in x['args'] and '--disable-subagents' in x['args'] for x in probes))
 record('Benchmark auth uses isolated --workspace and disabled probe tools; TLS never disabled',tls)
 def sync():
  run(['bash',target/'xLaunchpad.sh','--doctor'],env=dict(env,FAKE_BOB_VERSION='2.1.0'),cwd=target)
  run(['bash',target/'xLaunchpad.sh','--preview'],env=dict(env,FAKE_BOB_VERSION='2.1.0'),cwd=target)
  check((target/'bob-planning-analytics-v2.1.0.sh').is_file() and not(target/'bob-planning-analytics-v2.0.5.sh').exists())
  root=target.parents[1];run(['bash',root/'patches/PAA/patch-PAA-3.sh','--status'])
 record('Version-synchronized edited launcher accepted with no baseline admission',sync)

