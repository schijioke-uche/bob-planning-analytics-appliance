#!/usr/bin/env python3
"""Adapted Patch45 renderer tests against the shipped PAA runtime. Offline only."""
from __future__ import annotations
import argparse
import contextlib
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pty
import re
import select
import shlex
import shutil
import signal
import stat
import struct
import subprocess
import sys
import tempfile
import termios
import time

HERE=Path(__file__).resolve().parent; BUNDLE=HERE.parent
APP=BUNDLE/'use-cases/planning-analytics'
RUNTIME=APP/'.bob/runtime/bob-v2'
BASE={'PAA':{}}
sys.path.insert(0,str(RUNTIME))
import production_display as display
from production_display import RetrievalTextFilter as SearchTextFilter, EventRenderer, DisplayError, tool_metadata, scrub_assistant
RESULTS=[]
KEY='OFFLINE_TEST_KEY_NOT_REAL'

def expect(ok, message):
    if not ok: raise AssertionError(message)

def record(name, fn):
    start=time.monotonic()
    try: fn(); status,error='PASS',''
    except Exception as exc: status,error='FAIL',f'{type(exc).__name__}: {exc}'
    RESULTS.append(dict(name=name,status=status,seconds=round(time.monotonic()-start,3),error=error))
    print(status+': '+name+(' -- '+error if error else ''),flush=True)
    if error: raise AssertionError(error)

def sha(data): return hashlib.sha256(data).hexdigest()

def snapshot(root, ignore45=False):
    answer={}
    for p in sorted(root.rglob('*')):
        rel=str(p.relative_to(root))
        if '__pycache__' in p.parts:continue
        if ignore45 and ('/.bob/patch-backups/BOB2-45/' in '/'+rel or rel.endswith('/.bob/patches-applied/BOB2-45.json') or rel.endswith('/.session.lock')):continue
        if p.is_symlink(): answer[rel]=('SYMLINK:'+os.readlink(p),0)
        elif p.is_file(): answer[rel]=(sha(p.read_bytes()),stat.S_IMODE(p.stat().st_mode))
    return answer

@contextlib.contextmanager
def altered(path,data):
    before=path.read_bytes() if path.exists() else None
    mode=stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o645
    path.write_bytes(data.encode() if isinstance(data,str) else data)
    try:yield
    finally:
        if before is None:path.unlink(missing_ok=True)
        else:path.write_bytes(before);path.chmod(mode)

def invoke(args, env, cwd, rc=0, text='', timeout=50):
    p=subprocess.run([str(a) for a in args],cwd=str(cwd),env=env,text=True,input=text,
                     stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    expect(p.returncode==rc,f'Expected exit {rc}, got {p.returncode}: {p.stdout[-4000:]}')
    return p.stdout

def tty_run(args,env,cwd,text='',wait_for='',timeout=30):
    master,slave=pty.openpty()
    original=termios.tcgetattr(slave)
    attrs=list(original);attrs[3]&=~termios.ECHO;termios.tcsetattr(slave,termios.TCSANOW,attrs)
    fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',50,200,0,0))
    proc=subprocess.Popen([str(a) for a in args],env=env,cwd=str(cwd),stdin=slave,stdout=slave,stderr=slave)
    result=bytearray();deadline=time.monotonic()+timeout;sent=False
    try:
        if text and not wait_for:os.write(master,text.encode());sent=True
        while time.monotonic()<deadline:
            ready,_,_=select.select([master],[],[],0.05)
            if ready:
                try:data=os.read(master,65536)
                except OSError:break
                if not data:break
                result.extend(data)
                if text and not sent and wait_for.encode() in result:os.write(master,text.encode());sent=True
            elif proc.poll() is not None:break
        try:rc=proc.wait(timeout=max(.1,deadline-time.monotonic()))
        except subprocess.TimeoutExpired:proc.kill();proc.wait();raise AssertionError('PTY timed out')
        expect(rc==0,f'PTY exit {rc}: {result[-2000:]!r}')
        after=termios.tcgetattr(slave)
        expect(after==attrs,'Terminal attributes were not restored')
        return bytes(result).replace(b'\r\n',b'\n')
    finally:
        if proc.poll() is None:proc.kill();proc.wait()
        os.close(master);os.close(slave)

def filter_text(text,chunk=7,idle=False):
    f=SearchTextFilter();parts=[]
    for i in range(0,len(text),chunk):
        parts.append(f.feed(text[i:i+chunk]))
        if idle:parts.append(f.idle())
    parts.append(f.finish())
    return ''.join(parts),f

def unit_tests():
    for fixture,label in [('browse-output-fixture.txt','Browse documentation libraries'),('search-output-fixture.txt','Search IBM Watsonx documentation')]:
        sample=(HERE/fixture).read_text()
        for chunk in (1,2,7,83,8192):
            for idle in (False,True):
                def actual(sample=sample,label=label,chunk=chunk,idle=idle):
                    out,f=filter_text(sample+'\nFinal recommendation stays visible.\n',chunk,idle)
                    expect(out.splitlines()[0].strip()==label+' (completed)' and out.splitlines()[-1]=='Final recommendation stays visible.',repr(out))
                    expect(f.omitted==1,'Expected one suppressed payload')
                record(f'uploaded {fixture}: chunks {chunk}, idle {idle}',actual)
    def mixed():
        text=''
        for label,payload in [('Browse documentation libraries',{'indices':[{'name':'LEAK','description':'LEAK'}]}),('Search exact phrase documentation',{'results':[{'query':'LEAK','score':1}]}),('Knowledgebase information retrieval',{'documents':[{'content':'LEAK','metadata':{}}]})]:
            text+='\x1b[36m '+label+' (completed)\x1b[0m\n```json\n'+json.dumps(payload,indent=2)+'\n```\n'
        text+='An actionable answer. [Evidence: 45]\n'
        out,f=filter_text(text,1,True)
        expect('LEAK' not in out and f.omitted==3 and '[Evidence: 45]' in out,repr(out))
        expect(out.count('(completed)')==3,'Missing/duplicate statuses')
    record('all three operations; ANSI/chunked/fenced bodies hidden; answer retained',mixed)
    def quotes():
        p={'indices':[{'description':'braces " { [ ] } escaped \\ " and Unicode \u03b1'}]}
        out,_=filter_text('Browse documentation libraries (completed) '+json.dumps(p)+'\nNEXT\n',1,True)
        expect(out=='Browse documentation libraries (completed)\nNEXT\n',repr(out))
    record('inline Browse JSON with quotes/braces/escapes is fully suppressed',quotes)
    def normal():
        text='Plan\nRun oc get pods\n{"items": [{"metadata":{"name":"demo"}}]}\nApproval? '
        out,_=filter_text(text,1,True);expect(out==text,repr(out))
    record('normal output, deployment JSON and non-newline approval prompts retained',normal)
    def final_json():
        text='Browse documentation libraries (completed)\n{"indices":[]}\n{"apiVersion":"v1","kind":"ConfigMap","data":{"value":"ANSWER"}}\n'
        out,_=filter_text(text,3,True)
        expect('"apiVersion"' in out and 'ANSWER' in out and 'indices' not in out,repr(out))
    record('final requested JSON artifact after retrieval is not swallowed',final_json)
    for label in ('Browse documentation libraries','Search phrase documentation','Knowledgebase information retrieval'):
        for status in ('failed','cancelled','completed'):
            def truthful(label=label,status=status):
                out,_=filter_text(label+' ('+status+')\n[{"content":"RAW_LEAK"}]\nNext\n',2,True)
                expect(out==label+' ('+status+')\nNext\n',repr(out))
            record(label+': native '+status+' is truthful and payload-free',truthful)
    def progress():
        out,_=filter_text('Browse documentation libraries (running)\n{"indices":[]}\nBrowse documentation libraries (completed)\n{"indices":[]}\n',1)
        expect(out=='Browse documentation libraries (running)\nBrowse documentation libraries (completed)\n',repr(out))
    record('running retrieval does not produce a fabricated completion',progress)
    def unframed():
        for payload in [{'indices':[{'description':'LEAK'}]}, {'results':[{'score':1,'content':'LEAK'}]}, {'documents':[{'content':'LEAK','metadata':{}}]}]:
            out,_=filter_text('Before\n'+json.dumps(payload)+'\nAfter\n',2,True)
            expect('LEAK' not in out and 'Before' in out and 'After' in out,repr(out))
            expect('(completed)' not in out,'Unframed result should not invent a status')
    record('unframed Browse/Search/KB envelopes withheld without fabricated success',unframed)
    def wrapper():
        obj={'content':[{'type':'text','text':json.dumps({'indices':[{'description':'LEAK'}]})}]}
        out,_=filter_text(json.dumps(obj)+'\nFinal\n',1,True)
        expect(out=='Final\n',repr(out))
    record('MCP text-content wrapper of Browse indices is suppressed',wrapper)
    def echoes():
        for raw in [{'indices':[{'name':'LEAK','description':'LEAK'}]},{'results':[{'score':1,'content':'LEAK'}]},{'documents':[{'content':'LEAK','metadata':{}}]}]:
            text='Before\n'+json.dumps(raw)+'\nAfter [citation]\n'
            out=scrub_assistant(text)
            expect('LEAK' not in out and 'Before' in out and 'After [citation]' in out,repr(out))
        expect('LEAK' not in scrub_assistant('{"indices": [{"description": "LEAK'), 'Malformed envelope echoed')
    record('assistant echoes of all three raw schemas are suppressed; prose/citations retained',echoes)
    def partial():
        f=SearchTextFilter();out=f.feed('Browse documentation libraries (completed)\n{"indices":[{"description":"LEAK')
        expect('LEAK' not in out,'Partial body leaked')
        try:f.finish()
        except DisplayError:return
        raise AssertionError('Unclosed raw payload accepted')
    record('truncated payload fails closed without printing its body',partial)
    def limit():
        old=display.MAX_RECORD;display.MAX_RECORD=100
        try:
            f=SearchTextFilter();out=f.feed('Knowledgebase information retrieval (completed)\n')
            try:f.feed('{"content":"'+'A'*300)
            except DisplayError:
                expect('A'*10 not in out,'Oversized raw payload leaked');return
            raise AssertionError('Display limit not enforced')
        finally:display.MAX_RECORD=old
    record('display buffer limit has no raw-output fallback',limit)
    identities=[
      ({'tool_name':'browseDocumentationLibraries'},'Browse documentation libraries'),
      ({'tool_name':'list_indices'},'Browse documentation libraries'),
      ({'tool_name':'getDocumentationLibraries'},'Browse documentation libraries'),
      ({'tool_name':'use_mcp_tool','parameters':{'server_name':'ibm_docs','tool_name':'browse'}},'Browse documentation libraries'),
      ({'tool_name':'use_mcp_tool','parameters':json.dumps({'server_name':'ibm_docs','tool_name':'list_indices','arguments':'{}'})},'Browse documentation libraries'),
      ({'tool_name':'arbitrary','display_name':'Browse documentation libraries'},'Browse documentation libraries'),
      ({'tool_name':'use_mcp_tool','parameters':{'server_name':'watsonx_docs','tool_name':'search','arguments':json.dumps({'query':'watsonx deployment'})}},'Search watsonx deployment documentation'),
      ({'tool_name':'search','parameters':{'queries':[{'query':'alpha'},{'query':'beta'}]}},'Search alpha; beta documentation'),
      ({'tool_name':'searchIBMwatsonxDocumentation'},'Search IBM Watsonx documentation'),
      ({'tool_name':'search_knowledgebase'},'Knowledgebase information retrieval'),
      ({'tool_name':'retrieveKnowledgeBase'},'Knowledgebase information retrieval'),
      ({'tool_name':'kb_lookup'},'Knowledgebase information retrieval'),
      ({'tool_name':'read_file','parameters':{'path':'.bob/software-hub-knowledgebase/file.md'}},'Knowledgebase information retrieval'),
      ({'tool_name':'read_file','parameters':{'files':[{'path':'.bob/websphere-knowledgebase/file.md'}]}},'Knowledgebase information retrieval'),
      ({'tool_name':'use_mcp_tool','parameters':{'server_name':'knowledgebase','tool_name':'get','arguments':{'uri':'kb://example'}}},'Knowledgebase information retrieval'),
      ({'tool_name':'read_resource','parameters':{'uri':'knowledgebase://source'}},'Knowledgebase information retrieval'),
      ({'tool_name':'execute_command','parameters':{'command':'cat .bob/software-hub-knowledgebase/file.md'}},'Knowledgebase information retrieval'),
      ({'tool_name':'use_mcp_tool','parameters':{'server_name':'ibm_docs','tool_name':'show_sections'}},'Knowledgebase information retrieval')]
    for i,(event,label) in enumerate(identities):
        record('tool identity/argument classification '+str(i+1),lambda event=event,label=label:expect(tool_metadata(event,{})==(True,label),repr(tool_metadata(event,{}))))
    def non_retrieval():
        for event in [{'tool_name':'execute_command','parameters':{'command':'oc get pods'}},{'tool_name':'read_file','parameters':{'path':'src/main.py'}},{'tool_name':'write_to_file','parameters':{'path':'deployment.yaml','content':'search documentation'}}]:
            expect(not tool_metadata(event,{})[0],repr(event))
    record('unrelated command/file-write operations not classified from content alone',non_retrieval)
    def sanitized():
        event={'tool_name':'search','parameters':{'query':'\x1b[31mhello\nworld\r\tapi_key=SECRET'}}
        yes,label=tool_metadata(event,{})
        expect(yes and '\x1b' not in label and '\n' not in label and 'SECRET' not in label,label)
    record('query labels strip terminal controls, collapse whitespace and redact assignments',sanitized)
    def parallel():
        outs=[];errs=[];r=EventRenderer({}, {},outs.append,errs.append)
        rows=[{'type':'tool_use','tool_id':'b','tool_name':'list_indices'},
              {'type':'tool_use','tool_id':'s','tool_name':'search','parameters':{'query':'specific phrase'}},
              {'type':'tool_use','tool_id':'k','tool_name':'kb_lookup'},
              {'type':'tool_result','tool_id':'k','status':'success','output':'RAW_KB'},
              {'type':'tool_result','tool_id':'b','status':'success','output':{'indices':['RAW_BROWSE']}},
              {'type':'tool_result','tool_id':'s','status':'success','output':'RAW_SEARCH'},
              {'type':'message','role':'assistant','content':'Final answer [citation].'},
              {'type':'result','status':'success','last_message':'Final answer [citation].'}]
        before=json.dumps(rows,sort_keys=True)
        for row in rows:r.event(row)
        out=''.join(outs)
        expect(out=='Knowledgebase information retrieval (completed)\nBrowse documentation libraries (completed)\nSearch specific phrase documentation (completed)\nFinal answer [citation].\n',repr(out))
        expect(json.dumps(rows,sort_keys=True)==before,'Renderer mutated input result/context')
    record('interleaved tool IDs preserve all result objects and emit correct statuses',parallel)
    for tool in ('list_indices','search','kb_lookup'):
        def failure(tool=tool):
            out=[];r=EventRenderer({}, {},out.append,out.append)
            r.event({'type':'tool_use','tool_id':'x','tool_name':tool})
            r.event({'type':'tool_result','tool_id':'x','status':'error','output':'RAW_OUTPUT','error':'RAW_ERROR'})
            expect('(failed)' in ''.join(out) and 'RAW' not in ''.join(out) and '(completed)' not in ''.join(out),repr(out))
        record(tool+': structured failures show no raw error/result body',failure)
    def nested_failure():
        out=[];r=EventRenderer({}, {},out.append,out.append)
        r.event({'type':'tool_use','tool_id':'x','tool_name':'list_indices'})
        r.event({'type':'tool_result','tool_id':'x','status':'success','output':{'isError':True,'text':'RAW_FAIL'}})
        expect(''.join(out)=='Browse documentation libraries (failed)\n',repr(out))
    record('MCP isError flag overrides apparent transport success',nested_failure)
    def cancellation():
        out=[];r=EventRenderer({}, {},out.append,out.append)
        r.event({'type':'tool_use','tool_id':'x','tool_name':'kb_lookup'})
        r.event({'type':'tool_result','tool_id':'x','status':'cancelled','output':'RAW'})
        expect(''.join(out)=='Knowledgebase information retrieval (cancelled)\n',repr(out))
    record('structured knowledgebase cancellation is not mislabeled completed',cancellation)
    def unknown_status():
        out=[];r=EventRenderer({}, {},out.append,out.append)
        r.event({'type':'tool_use','tool_id':'x','tool_name':'list_indices'})
        r.event({'type':'tool_result','tool_id':'x','output':'RAW'})
        expect('(completed)' not in ''.join(out) and 'status unrecognized' in ''.join(out),repr(out))
    record('missing operation status cannot be claimed completed',unknown_status)
    def duplicate():
        out=[];r=EventRenderer({}, {},out.append,out.append)
        for ident in ['a','b']:
            r.event({'type':'tool_use','tool_id':ident,'tool_name':'list_indices'})
            event={'type':'tool_result','tool_id':ident,'status':'success','output':'RAW'}
            r.event(event);r.event(event)
        r.event({'type':'message','role':'assistant','content':'Browse documentation libraries (completed)\nAnswer'})
        expect(''.join(out).count('(completed)')==2 and 'Answer' in ''.join(out),repr(out))
    record('each real call keeps its status; duplicate events/model status echoes suppressed',duplicate)
    def unknown():
        out=[];r=EventRenderer({}, {},out.append,out.append)
        r.event({'type':'tool_result','tool_id':'missing','status':'success','output':'RAW_UNKNOWN'})
        r.event({'type':'future_event','output':'RAW_UNKNOWN'})
        expect(not out and r.unknown==2,'Unknown raw fallback')
    record('unpaired/unknown events never dump raw data',unknown)
    def command():
        out=[];r=EventRenderer({}, {'BOB_API_KEY':KEY},out.append,out.append)
        r.event({'type':'tool_use','tool_id':'e','tool_name':'execute_command'})
        r.event({'type':'tool_result','tool_id':'e','status':'success','output':'deployment.apps/demo configured'})
        r.event({'type':'error','message':'Authentication failed '+KEY})
        expect('configured' in ''.join(out) and 'Authentication failed' in ''.join(out) and KEY not in ''.join(out),repr(out))
    record('meaningful command results/errors retained; credentials redacted',command)
    def recovered():
        out=[];r=EventRenderer({}, {},out.append,out.append)
        r.event({'type':'tool_use','tool_id':'k','tool_name':'kb_lookup'})
        r.event({'type':'tool_result','tool_id':'k','status':'failed','output':'RAW'})
        r.event({'type':'result','status':'success','last_message':'Recovered using another source.'})
        expect(r.final_success and '(failed)' in ''.join(out) and 'Recovered' in ''.join(out),repr(out))
    record('a recovered retrieval failure does not override final task status',recovered)

    def terminated():
        master,slave=pty.openpty();original=termios.tcgetattr(slave)
        script=("import sys; from pathlib import Path; sys.path.insert(0,"+repr(str(RUNTIME))+"); "
                "from production_display import chat_terminal; import os; "
                "sys.exit(chat_terminal([sys.executable, '-u', '-c', \"import time; print('READY_FOR_TERMINATION', flush=True); time.sleep(60)\"], Path.cwd(),dict(os.environ)))")
        proc=subprocess.Popen([sys.executable,'-c',script],stdin=slave,stdout=slave,stderr=slave)
        output=bytearray();deadline=time.monotonic()+10
        try:
            while b'READY_FOR_TERMINATION' not in output and time.monotonic()<deadline:
                if select.select([master],[],[],.1)[0]:output.extend(os.read(master,65536))
                if proc.poll() is not None:break
            expect(b'READY_FOR_TERMINATION' in output,repr(output))
            os.kill(proc.pid,signal.SIGTERM)
            expect(proc.wait(timeout=8)==143,'SIGTERM exit status changed')
            expect(termios.tcgetattr(slave)==original,'SIGTERM left terminal in raw mode')
        finally:
            if proc.poll() is None:proc.kill();proc.wait()
            os.close(master);os.close(slave)
    record('SIGTERM cleans child session and restores terminal attributes',terminated)
    def opaque():
        for body in ({'indices':[]},json.dumps({'indices':[]}),{'content':[{'type':'text','text':json.dumps({'indices':[{'name':'docs_sample','description':'RAW'}]})}]}):
            out=[];r=EventRenderer({}, {},out.append,out.append)
            r.event({'type':'tool_use','tool_id':'o','tool_name':'opaque_adapter'})
            r.event({'type':'tool_result','tool_id':'o','status':'success','output':body})
            expect(''.join(out)=='Browse documentation libraries (completed)\n',repr(out))
    record('opaque wrapper with recognized Browse envelope produces status, never raw metadata',opaque)
    def array():
        out,_=filter_text('[{"name":"docs_sample","description":"RAW_LIBRARY"}]\nDone\n',1,True)
        expect(out=='Done\n',repr(out))
    record('bare documentation-library record array also suppressed',array)


def style_discovery_tests():
    from terminal_style import SgrState, NativeCyanAccent, accent_enabled, clean
    def endstate(value):
        st=SgrState();st.apply(value);return st.values
    def styled_filter(value,chunk=1,config=None,cyan=False):
        f=SearchTextFilter(NativeCyanAccent(config,cyan));out=[]
        for i in range(0,len(value),chunk):
            out.append(f.feed(value[i:i+chunk]));out.append(f.idle())
        out.append(f.finish());return ''.join(out)
    for label in ('Browse documentation libraries','Search Cloud Pak For Data documentation','Knowledgebase information retrieval'):
        for status in ('completed','failed','cancelled','executing...'):
            def preserve(label=label,status=status):
                header='  \x1b[1;36m'+label+'\x1b[39m \x1b[90m('+status+')\x1b[0m\n'
                raw=header+'{\"indices\": [{\"description\": \"RAW_COLOR_LEAK\"}]}\n'
                expect(styled_filter(raw)==header,repr(styled_filter(raw)))
            record('native ANSI/prefix/indentation preserved: '+label+' '+status,preserve)
    def canonical():
        text=' \x1b[32m+ \x1b[1;36mBrowse documentation\x1b[39m \x1b[90m(success)\x1b[0m\n{\"indices\": []}\n'
        result=styled_filter(text)
        expect(result==' \x1b[32m+ \x1b[1;36mBrowse documentation libraries\x1b[39m \x1b[90m(completed)\x1b[0m\n',repr(result))
    record('canonical text normalization preserves icon and separate field colors',canonical)
    def inline():
        text='  \x1b[36mSearch alpha documentation \x1b[90m(completed)\x1b[0m {\"results\": [{\"content\": \"RAW_LEAK\"}]}\n'
        result=styled_filter(text)
        expect('RAW_LEAK' not in result and '\x1b[36mSearch' in result and '\x1b[90m(completed)' in result,repr(result))
    record('inline payload suppression retains styled header',inline)
    def reset():
        source='\x1b[36mBrowse documentation libraries (completed)\n{\"indices\": []}\x1b[0m\nNormal answer\n'
        result=styled_filter(source)
        expect('indices' not in result and endstate(result)==endstate(source),repr(result))
        prefix=result.split('Normal answer')[0]
        expect(not endstate(prefix),'Hidden payload reset was lost and color bled into the answer')
    record('SGR reset after hidden payload preserved without color bleed',reset)
    def hidden_style():
        source='\x1b[38;2;0;180;180mBrowse documentation libraries (completed)\n{\"indices\": [\x1b[39m]}\nNext\n'
        result=styled_filter(source)
        expect(endstate(source)==endstate(result) and 'indices' not in result,repr(result))
    record('RGB/indexed foreground state reconciled across hidden body',hidden_style)
    def answers():
        text='\x1b[1;35mA colorful answer\x1b[0m [citation]\n'
        expect(scrub_assistant(text)==text,'Assistant color stripped')
        raw=text+'{\"indices\": [{\"description\": \"RAW_LEAK\"}]}\n'+text
        out=scrub_assistant(raw)
        expect('RAW_LEAK' not in out and out.count(text)==2,repr(out))
    record('assistant ANSI formatting and citations survive envelope scrubber',answers)
    def ordinary():
        raw='\x1b[?25l\x1b[2K\r\x1b[35mPlan\x1b[0m\n\x1b]8;;https://example.invalid\x07Link\x1b]8;;\x07\nApproval? '
        expect(styled_filter(raw)==raw,'Ordinary ANSI/cursor/OSC/approval bytes changed')
    record('unrelated cursor controls, hyperlinks, colored answers and prompt bytes retained',ordinary)
    for code,base in BASE.items():
        config=json.loads((HERE/'config'/(code+'.json')).read_text())
        for slug,name in config['mode_names'].items():
            def footer(name=name,slug=slug,config=config):
                raw='  \x1b[90m'+name+' Mode \x1b[31m(auto-approve)\x1b[39m - 10k tokens\n'
                out=styled_filter(raw,config=config,cyan=True)
                expect(clean(out)==clean(raw),'Footer text renamed')
                start=out.index(name);end=start+len(name)
                expect(endstate(out[:start]).get('fg')=='36','Mode title not cyan')
                approve=out.index('(auto-approve)')
                expect(endstate(out[:approve]).get('fg')=='31','Auto-approve warning recolored')
                expect(endstate(out)==endstate(raw),'Footer end SGR changed')
            record(code+' '+slug+': cyan mode title; red warning and text retained',footer)
    def inputbox():
        rule='\x1b[35m'+'\u2500'*70+'\x1b[39m\n'
        prompt=' \x1b[35m\u276f\x1b[39m \u2588 Build Anything, @ for context, / for commands, $ for skills\n'
        raw=rule+prompt+rule
        out=styled_filter(raw,cyan=True)
        expect(clean(out)==clean(raw) and '\x1b[36m' in out,'Input box text changed or missing cyan')
        for token in ('\u2500','\u276f'):
            expect(endstate(out[:out.index(token)]).get('fg')=='36','Input accent not cyan')
    record('sample-shaped native input borders and chevron restored to cyan',inputbox)
    def optout():
        raw='\x1b[35m'+'\u2500'*40+'\x1b[0m\n'
        expect(styled_filter(raw,cyan=False)==raw,'native opt-out changes colors')
        for env,tty in (({'TERM':'xterm','NO_COLOR':'1'},True),({'TERM':'dumb'},True),({'TERM':'xterm','BOB2_UI_ACCENT':'native'},True),({'TERM':'xterm'},False)):
            expect(not accent_enabled(env,tty),'No-color/native/nonterminal override ignored')
        expect(accent_enabled({'TERM':'xterm'},True),'Default terminal cyan not enabled')
    record('native/no-color/nonterminal presentation overrides honored',optout)
    def codeblock():
        raw='```text\n\x1b[35m'+'\u2500'*70+'\x1b[0m\n```\n'
        expect(styled_filter(raw,cyan=True)==raw,'Code-block art recolored')
    record('cyan accent skips fenced code output',codeblock)
    def unrelated_rule():
        raw='\x1b[35m'+'\u2500'*70+'\x1b[39m\nThis is an answer separator, not the input box.\n'
        expect(styled_filter(raw,cyan=True)==raw,'An unrelated horizontal answer rule was recolored')
    record('unconfirmed horizontal answer rule remains byte-for-byte native',unrelated_rule)

    def discovery_policy():
        policy=(APP/'.bob/BOB2-DOCUMENTATION-DISCOVERY-POLICY.md').read_text()
        for text in ('BEFORE','before'):
            pass
        for token in ('parameter schema','FIRST','not automatically','ONCE','product','version','not an MCP proxy'):
            expect(token in policy,'Missing discovery policy contract: '+token)
        for value in ('ibm-software-hub','docs_cloud_pak_for_data'):
            expect(value in policy,'Incident trace absent')
    record('discovery policy forbids guessed mapping and defines bounded recovery',discovery_policy)
