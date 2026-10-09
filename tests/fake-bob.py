#!/usr/bin/env python3
"""Strict OFFLINE test double, not IBM Bob and not a backend emulator."""
import json,os,pathlib,re,sys,time
args=sys.argv[1:]
root=pathlib.Path.cwd()
CHAT={'--trust':0,'--mode':1,'--resume':1,'--auto-approve':0,'--instance-id':1,'--team-id':1,'--log-level':1}
RUN={'--mode':1,'--format':1,'--max-turns':1,'--workspace':1,'--trust':0,'--accept-license':0,'--team-id':1,'--log-level':1,'--disable-mcp':0,'--disable-subagents':0}
missing=os.environ.get('FAKE_MISSING_FLAG','')
if args==['--version']:
 print('IBM Bob Shell v'+os.environ.get('FAKE_BOB_VERSION','2.0.5'));sys.exit(0)
if args==['--help']:
 print('Usage: bob <command>\n  --list-tasks [all]\n  --version\nCommands: chat run');sys.exit(0)
if len(args)==2 and args[1]=='--help' and args[0] in ('run','chat'):
 opts=RUN if args[0]=='run' else CHAT
 print('Usage: bob '+args[0]+' --format pretty|json|stream-json')
 for flag,n in opts.items():
  if missing!=args[0]+':'+flag:print('  '+flag+(' <value>' if n else ''))
 sys.exit(0)
if args==['--list-tasks','all']:
 if os.environ.get('FAKE_EMPTY_TASKS')=='1':sys.exit(0)
 records=[{'id':'old-user','title':'Earlier work','workspace':root.as_uri(),'updatedAt':10},
 {'id':'auth-probe','title':'BQCA_AUTH_PROBE: Return exactly BOB_AUTH_OK','workspace':root.as_uri(),'updatedAt':300},
 {'id':'wrong-workspace','title':'Other work','workspace':(root.parent/'elsewhere').as_uri(),'updatedAt':500},
 {'id':'latest-user','title':'Most recent real user request','workspace':root.as_uri(),'updatedAt':100}]
 print('\n'.join(json.dumps(r) for r in records));sys.exit(0)
if not args or args[0] not in ('run','chat'):
 sys.exit('FAKE_BOB_REJECTED: expected run/chat subcommand')
command=args[0];opts=RUN if command=='run' else CHAT;values={};positionals=[]
i=1
while i<len(args):
 arg=args[i]
 if arg.startswith('--'):
  if arg not in opts or missing==command+':'+arg:sys.exit('FAKE_BOB_REJECTED: unknown option '+arg)
  if opts[arg]:
   if i+1>=len(args):sys.exit('FAKE_BOB_REJECTED: missing flag value')
   values[arg]=args[i+1];i+=2
  else:values[arg]=True;i+=1
 else:positionals.append(arg);i+=1
if command=='chat' and positionals:sys.exit('FAKE_BOB_REJECTED: positional chat prompt is unsupported')
if command=='run' and len(positionals)!=1:sys.exit('FAKE_BOB_REJECTED: expected exactly one positional prompt')
probe=bool(positionals and any(positionals[0].startswith(p) for p in ('BOB2_AUTH_PROBE:', 'BQCA_AUTH_PROBE:')))
if command=='run' and not probe and pathlib.Path(values.get('--workspace','')).resolve()!=root:
 sys.exit('FAKE_BOB_REJECTED: mismatched workspace/cwd')
if not probe:
 modes=root/'.bob/custom_modes.yaml'
 if not modes.is_file():sys.exit('FAKE_BOB_REJECTED: missing project modes')
 slugs=re.findall(r'^\s*- slug: ([a-z0-9-]+)\s*$',modes.read_text(),re.M)
 if values.get('--mode') not in slugs:sys.exit('FAKE_BOB_REJECTED: unavailable mode')
entry={'command':command,'args':args,'cwd':str(root),'probe':probe,'mode':values.get('--mode'),
       'resume':values.get('--resume'),'menu':os.environ.get('BOB2_MENU_OPTION'),
       'skill':os.environ.get('BOB2_MENU_SKILL_ID'),'code':os.environ.get('BOB2_APPLIANCE_CODE'),
       'tls_disabled':os.environ.get('NODE_TLS_REJECT_UNAUTHORIZED')=='0',
       'legacy_env':[k for k in ('BOBSHELL_API_KEY','BOB_ENDPOINT','BOB_AUTH_ENDPOINT','BOB_REGION') if k in os.environ],
       'api_key_present':bool(os.environ.get('BOB_API_KEY')),
       'workspace':values.get('--workspace'), 'extra_ca':os.environ.get('NODE_EXTRA_CA_CERTS'),
       'mode_override':os.environ.get('BOB2_CODE_MODE'), 'stdin_isatty':sys.stdin.isatty(), 'stdout_isatty':sys.stdout.isatty(), 'env_loads':os.environ.get('TEST_ENV_LOADS')}

log=os.environ.get('FAKE_BOB_LOG')
if log:
 with open(log,'a') as f:f.write(json.dumps(entry)+'\n')
if probe:
 if os.environ.get('FAKE_AUTH_FAIL')=='1':
  print('Test authentication refused: '+os.environ.get('BOB_API_KEY',''),file=sys.stderr);sys.exit(13)
 if os.environ.get('FAKE_AUTH_BAD_JSON')=='1':print('not-json');sys.exit(0)
 if os.environ.get('FAKE_AUTH_ALTERNATE_JSON')=='1':print(json.dumps({'result': {'text':'BOB_AUTH_OK'}}));sys.exit(0)
 if os.environ.get('FAKE_AUTH_TIMEOUT')=='1':time.sleep(3)
 print(json.dumps({'status':'success','last_message':'BOB_AUTH_OK','stats':{'task_id':'isolated-probe'}}));sys.exit(0)
# All raw results stay available to this OFFLINE fake agent.
browse = {'indices':[{'name':'docs_45','description':'RAW_BROWSE_PAYLOAD_MARKER'}]}
payload = {'results':[{'query':'Planning Analytics deployment', 'results':[{'id':'DOC-42','score':0.875,'content':'RAW_SEARCH_PAYLOAD_MARKER: use a staging environment.'}]}]}
kb = {'documents':[{'id':'KB-45','metadata':{'source':'RAW_KB_METADATA_MARKER'},'content':'RAW_KB_PAYLOAD_MARKER: validate configuration.'}]}
answer = 'Use a staging environment and validate configuration. [Evidence: DOC-42; KB-45]'
if os.environ.get('FAKE_BOB_EXIT'):
 print('Simulated workload failure',file=sys.stderr);sys.exit(int(os.environ['FAKE_BOB_EXIT']))
headers=['Browse documentation libraries (completed)','Search Planning Analytics deployment documentation (completed)','Knowledgebase information retrieval (completed)']
def pretty(stream=sys.stdout):
 for title,body in zip(headers,[browse,payload,kb]):
  print(' '+title,file=stream,flush=True)
  print(json.dumps(body,indent=2),file=stream,flush=True)
if command=='chat':
 if os.environ.get('FAKE_CHAT_READ')=='1':
  print('Approval question: continue? ',end='',flush=True)
  response=sys.stdin.readline().strip()
  print('INPUT_RECEIVED:'+response,flush=True)
 pretty()
 if os.environ.get('FAKE_NATIVE_UI')=='1':
  config=json.loads((root/'.bob/runtime/bob-v2/appliance.json').read_text())
  name=config['mode_names'][values['--mode']]
  print('\x1b[35m'+'\u2500'*65+'\x1b[39m')
  print(' \x1b[35m\u276f\x1b[39m \u2588 Build Anything, @ for context, / for commands, $ for skills')
  print('\x1b[35m'+'\u2500'*65+'\x1b[39m')
  print(' \x1b[90m'+name+' Mode \x1b[31m(auto-approve)\x1b[39m',flush=True)
 print(answer,flush=True)
 sys.exit(0)
if values.get('--format')!='stream-json':sys.exit('FAKE_BOB_REJECTED: production must use stream-json')
def send(row):print(json.dumps(row),flush=True)
if os.environ.get('FAKE_MALFORMED_STREAM')=='1':
 print('RAW_SEARCH_PAYLOAD_MARKER: not NDJSON');sys.exit(0)
requests=[('browse-1',{'tool_name':'use_mcp_tool','parameters':{'server_name':'ibm_docs','tool_name':'list_documentation_libraries','arguments':{}}}),
 ('search-1',{'tool_name':'use_mcp_tool','parameters':{'server_name':'planning_docs','tool_name':'search','arguments':{'query':'Planning Analytics deployment'}}}),
 ('kb-1',{'tool_name':'read_file','parameters':{'files':[{'path':'.bob/planning-analytics-knowledgebase/verification.md'}]}})]
for ident,event in requests:send(dict(event,type='tool_use',tool_id=ident))
for (ident,_),body in zip(requests,[browse,payload,kb]):
 send({'type':'tool_result','tool_id':ident,'status':'success','output':body if ident!='kb-1' else 'RAW_KB_PAYLOAD_MARKER: validate configuration.'})
if os.environ.get('FAKE_STREAM_STDERR_SEARCH')=='1' or os.environ.get('FAKE_STREAM_STDERR_RETRIEVAL')=='1':pretty(sys.stderr)
assert browse['indices'][0]['name']=='docs_45'
assert payload['results'][0]['results'][0]['content'].endswith('staging environment.')
assert kb['documents'][0]['content'].endswith('validate configuration.')
send({'type':'message','role':'assistant','content':answer})
if os.environ.get('FAKE_NO_FINAL')!='1':send({'type':'result','status':'success','stats':{'task_id':'test-user'},'last_message':answer})
