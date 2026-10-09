#!/usr/bin/env python3
"""New full-release regressions. All fixtures are offline; no IBM calls."""
from __future__ import annotations
import argparse,contextlib,hashlib,importlib.util,io,json,os,re,shutil,stat,subprocess,sys,tempfile,time,zipfile
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;PKG=HERE.parent;APP=PKG/'use-cases/planning-analytics'
sys.path.insert(0,str(HERE))
import test_domains_runtime as previous
import test_inherited_display as inherited
RESULTS=[]

def check(value,msg='Assertion failed'):
    if not value:raise AssertionError(msg)

def record(name,fn):
    start=time.monotonic()
    try:fn();result='PASS';error=''
    except Exception as exc:result='FAIL';error=f'{type(exc).__name__}: {exc}'
    RESULTS.append(dict(name=name,status=result,seconds=round(time.monotonic()-start,3),error=error))
    print(result+': '+name+(' -- '+error if error else ''),flush=True)

def run(args,cwd=None,env=None,rc=0):
    value=subprocess.run([str(a) for a in args],cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
    check(value.returncode==rc,f'Unexpected exit {value.returncode}: {value.stdout[-1500:]}');return value.stdout

def bytes_snapshot(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts}

def all_777(root):
    return all(stat.S_IMODE(p.lstat().st_mode)==0o777 for p in [root,*root.rglob('*')] if not p.is_symlink() and (p.is_file() or p.is_dir()))

def copy_package(to):
    shutil.copytree(PKG,to,ignore=shutil.ignore_patterns('__pycache__'))
    for p in to.rglob('*'):
        if p.is_file() and p.suffix in ('.sh','.py'):p.chmod(0o755)
    return to

def content_tests():
    config=json.loads((APP/'.bob/runtime/bob-v2/appliance.json').read_text())
    modes=(APP/'.bob/custom_modes.yaml').read_text()
    record('Full release has 20 unique canonical modes and Planning Analytics labels',lambda:check(len(config['mode_slugs'])==20 and len(set(config['mode_slugs']))==20 and re.findall(r'^- slug: (.+)$',modes,re.M)==config['mode_slugs'] and all(n.startswith('IBM Bob Planning Analytics ') and n.endswith(' Appliance') for n in config['mode_names'].values())))
    for slug in config['mode_slugs']:
        def one(slug=slug):
            rules=list((APP/config['rule_sources'][slug]).glob('*.md'))
            check(len(rules)>=2)
            check(all('BOB2-DOCUMENTATION-DISCOVERY-POLICY.md' in p.read_text() and 'PAA-MAINTENANCE-POLICY.md' in p.read_text() for p in rules))
        record('Mode/rule routing and policy linkage: '+slug,one)
    for p in sorted((APP/'.bob/skills').glob('*/SKILL.md')):
        record('Skill identity, retrieval and editable maintenance: '+p.parent.name,lambda p=p:check('BOB2-DOCUMENTATION-DISCOVERY-POLICY.md' in p.read_text() and 'PAA-MAINTENANCE-POLICY.md' in p.read_text() and p.read_text().startswith('---\n')))
    record('No old mandatory receipt or local launcher hash field shipped',lambda:check(not list((APP/'.bob/patches-applied').glob('PAA-*.json')) and 'launcher_sha256' not in config))
    record('All active maintenance/runtime/utility sources lack hash-comparison admission',lambda:check(all('hashlib' not in p.read_text() and 'Managed file differs' not in p.read_text() for p in [PKG/'patches/PAA/install.py',APP/'.bob/runtime/bob-v2/runtime.py',APP/'.bob/planning-analytics-tools/pa-tool.py'])))
    record('Active configuration, not just its example, enables cyan',lambda:check('BOB2_UI_ACCENT=cyan' in (APP/'.bob/bob-v2.env').read_text()))
    record('Original .env contains no credentials',lambda:check(all(not line.strip() or line.lstrip().startswith('#') for line in (APP/'.env').read_text().splitlines())))
    record('No old patch chain required by maintenance',lambda:check('patch-PAA-1' not in (PKG/'maintenance.sh').read_text() and 'patch-PAA-2' not in (PKG/'maintenance.sh').read_text()))


def installation_tests(work):
    repo=copy_package(work/'repository with spaces');target=repo/'use-cases/planning-analytics';controller=repo/'patches/PAA/patch-PAA-3.sh'
    def preflight():
        before=bytes_snapshot(repo);result=json.loads(run(['bash',repo/'maintenance.sh','--check'],cwd=Path('/tmp')))
        check(result['status']=='READY' and result['local_baseline_checks'] is False and before==bytes_snapshot(repo))
    record('Fresh extracted package preflight succeeds without installation receipt',preflight)
    record('Actual bundled maintenance.sh runs from an unrelated CWD',lambda:check(json.loads(run(['bash',repo/'maintenance.sh'],cwd=Path('/tmp')))['status']=='MAINTAINED'))
    record('Recursive 0777 includes all current files and dot directories',lambda:check(all_777(repo/'use-cases')))
    def edited():
        changes={'.env.example':b'# operator additions\r\nBOB_TEAM_ID=EXAMPLE_ONLY\r\n','.env':b'# local secret placeholder\nBOB_API_KEY=OFFLINE_LOCAL_TEST\n','AGENTS.md':b'# operator-custom instructions\n','.bob/rules-code/local-team.md':b'# local team rules\n','.bob/planning-analytics-knowledgebase/guide/15-model-design-dimensions-cubes-and-drivers.md':b'# locally revised guidance\n'}
        for name,data in changes.items():p=target/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        for action in ('--check','--apply','--status'):
            output=run(['bash',repo/'maintenance.sh',action]);check('baseline:' not in output.lower() and 'warning' not in output.lower())
            check(all((target/name).read_bytes()==data for name,data in changes.items()))
    record('Exact .env.example edit plus CRLF, .env and rule edits never block maintenance',edited)
    def old_receipts():
        base=target/'.bob/patches-applied';base.mkdir(exist_ok=True)
        for name in ('PAA-1.json','PAA-2.json','PAA-BASELINE.json'):(base/name).write_text('not JSON\n')
        before={p.name:p.read_bytes() for p in base.iterdir()}
        for action in ('--check','--apply','--status'):run(['bash',controller,action])
        check(before=={p.name:p.read_bytes() for p in base.iterdir()})
    record('Absent/stale/malformed historical receipts are not parsed as gates',old_receipts)
    def repeat():
        before=bytes_snapshot(target)
        for _ in range(3):run(['bash',repo/'maintenance.sh'])
        check(before==bytes_snapshot(target))
    record('Repeated maintenance preserves every local file byte',repeat)
    def new_files():
        d=target/'bob-planning-analytics-store/new hidden/.data';d.mkdir(parents=True)
        (d/'mine.txt').write_text('preserve');(d/'mine.txt').chmod(0o400);d.chmod(0o700)
        run(['bash',repo/'maintenance.sh']);check(all_777(repo/'use-cases') and (d/'mine.txt').read_text()=='preserve')
    record('Later-created work and hidden files normalize to 0777',new_files)
    def symlinks():
        outside=work/'outside';outside.mkdir();secret=outside/'file';secret.write_text('outside unchanged');secret.chmod(0o600)
        link=target/'outside-link';link.symlink_to(outside,target_is_directory=True)
        run(['bash',repo/'maintenance.sh']);check(secret.read_text()=='outside unchanged' and stat.S_IMODE(secret.stat().st_mode)==0o600)
    record('Recursive maintenance does not follow links outside the selected tree',symlinks)
    def siblings():
        for name in ('ansible','openshift','software-hub','terraform','websphere','watsonx-orchestrate','qse-vulnerable-code'):
            sibling=repo/'use-cases'/name;sibling.mkdir(exist_ok=True);(sibling/'team.txt').write_text(name);(sibling/'team.txt').chmod(0o640)
        before=bytes_snapshot(repo/'use-cases');run(['bash',repo/'maintenance.sh'])
        check(before==bytes_snapshot(repo/'use-cases') and all_777(repo/'use-cases'))
    record('Seven sibling contents preserved while selected tree permissions become 0777',siblings)
    def receiptless_payloadless():
        z=repo/'patches/PAA/payload/planning-analytics.zip';data=z.read_bytes();z.unlink()
        try:
            for action in ('--check','--apply','--status'):run(['bash',repo/'maintenance.sh',action])
        finally:z.write_bytes(data)
    record('Existing-target maintenance needs neither payload nor baseline records',receiptless_payloadless)
    def modes_differ():
        (target/'.env.example').chmod(0o456)
        for action in ('--check','--status'):run(['bash',controller,action])
        run(['bash',controller,'--apply']);check(stat.S_IMODE((target/'.env.example').stat().st_mode)==0o777)
    record('No exact-permission admission test; apply normalizes arbitrary existing modes',modes_differ)
    # New-target path installation from the complete patch control subtree.
    fresh=work/'empty repository';fresh.mkdir();shutil.copytree(PKG/'patches',fresh/'patches');ctl=fresh/'patches/PAA/patch-PAA-3.sh';new=fresh/'use-cases/planning-analytics'
    record('Fresh repository installation needs no old seven-appliance layout or receipts',lambda:check(json.loads(run(['bash',ctl,'--apply']))['status']=='INSTALLED' and new.is_dir()))
    record('Freshly installed content matches delivered file bytes (test only, not a gate)',lambda:check(bytes_snapshot(new)==bytes_snapshot(APP)))
    record('Freshly installed tree is entirely 0777',lambda:check(all_777(fresh/'use-cases')))
    def singular():
        other=work/'singular';other.mkdir();(other/'use-case').mkdir();run(['bash',ctl,'--root',other,'--apply']);check((other/'use-case/planning-analytics/xLaunchpad.sh').is_file() and not (other/'use-cases').exists())
    record('Singular use-case directory spelling supported',singular)
    def no_bob():
        env={'PATH':os.environ['PATH'],'TERM':'xterm-256color','PYTHONDONTWRITEBYTECODE':'1','BOB_BIN':'missing-bob-xyz','BOB2_BIN':'missing-bob-xyz'}
        check('Planning Analytics' in run(['bash',fresh/'use-cases/planning-analytics/xLaunchpad.sh','--preview'],env=env))
    record('Preview requires no Bob, API key, installed receipt or network',no_bob)
    def local_launcher():
        launcher=next(new.glob('bob-planning-analytics-v*.sh'));before=launcher.read_bytes()+b'\n# approved local comment\n';launcher.write_bytes(before)
        env={'PATH':os.environ['PATH'],'HOME':str(work),'TERM':'xterm-256color','BOB2_BIN':str(HERE/'fake-bob.py'),'PYTHONDONTWRITEBYTECODE':'1','FAKE_BOB_VERSION':'2.0.7'}
        run(['bash',new/'bob-filename-version-sync.sh'],env=env)
        launchers=list(new.glob('bob-planning-analytics-v*.sh'));check(len(launchers)==1 and launchers[0].read_bytes()==before)
    record('Edited versioned launcher is retained during version synchronization',local_launcher)
    def edited_guide():
        p=new/'.bob/planning-analytics-knowledgebase/guide/15-model-design-dimensions-cubes-and-drivers.md';p.write_text(p.read_text()+'\nOperator additions.\n')
        check(json.loads(run(['bash',new/'paa-self-check.sh']))['status']=='PASS')
    record('Self-check permits edited knowledgebase sections; no hash baseline',edited_guide)
    def rollback():
        before=bytes_snapshot(target);result=json.loads(run(['bash',controller,'--rollback']));saved=Path(result['archive']);check(saved.is_dir() and bytes_snapshot(saved)==before and not target.exists())
    record('Explicit rollback archives locally edited project without receipt/hash admission',rollback)
    def staged_failure():
        import importlib.util
        spec=importlib.util.spec_from_file_location('new_installer_test',PKG/'patches/PAA/install.py')
        engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
        other=work/'write-failure';other.mkdir()
        real=engine.fill_missing
        def fail(dest,members):
            (dest/'first.txt').write_text('partial fixture')
            raise OSError('injected I/O failure')
        with patch.object(engine,'fill_missing',side_effect=fail):
            try:engine.main(['--root',str(other),'--apply'])
            except OSError:pass
            else:raise AssertionError('Expected injected failure')
        check(not (other/'use-cases/planning-analytics').exists() and not list((other/'use-cases').glob('.paa-install-*')))
    record('Injected fresh-install write failure publishes no partial appliance',staged_failure)
    def nonroot():
        if os.geteuid()!=0:
            # The full suite already uses the current unprivileged account.
            return
        import pwd
        account=pwd.getpwnam('nobody')
        other=work/'unprivileged';other.mkdir();shutil.copytree(PKG/'patches',other/'patches')
        shutil.copytree(APP,other/'use-cases/planning-analytics')
        work.chmod(0o755)
        for item in [other,*other.rglob('*')]:
            os.chown(item,account.pw_uid,account.pw_gid)
            item.chmod(0o755 if item.is_dir() else 0o644)
        local=other/'use-cases/planning-analytics/.env.example'
        local.write_text('# unprivileged local template edit\n');local.chmod(0)
        def identity():
            os.setgroups([]);os.setgid(account.pw_gid);os.setuid(account.pw_uid)
        out=subprocess.run([sys.executable,str(other/'patches/PAA/install.py'),'--apply'],preexec_fn=identity,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=40)
        check(out.returncode==0,out.stdout+out.stderr)
        check(all_777(other/'use-cases') and local.read_text()=='# unprivileged local template edit\n')
    record('Unprivileged owner repairs a 0000 local template without a baseline or mode gate',nonroot)
    # Keep runtime tests on a clean real installed package, not the intentionally edited one.
    return new


def extra_style_tests(work):
    runtime=APP/'.bob/runtime/bob-v2';sys.path.insert(0,str(runtime))
    from terminal_style import NativeCyanAccent,SgrState,clean
    from production_display import RetrievalTextFilter
    config=json.loads((runtime/'appliance.json').read_text())
    def uncolored():
        line='\u2500'*60+'\n';prompt=' \u276f \u2588 Build Anything, @ for context, / for commands, $ for skills\n'
        text=line+prompt+line
        f=RetrievalTextFilter(NativeCyanAccent(config,True));out=f.feed(text)+f.finish()
        check(clean(out)==text and out.count('\x1b[36m')>=3)
    record('Native uncolored input frame gains cyan only after context recognition',uncolored)
    def diagnostic():
        env=dict(os.environ,TERM='xterm-256color',PYTHONDONTWRITEBYTECODE='1');env.pop('NO_COLOR',None)
        out=inherited.tty_run(['bash',PKG/'paa-ui-check.sh'],env,PKG).decode()
        check('\x1b[36m' in out and '\x1b[31m(auto-approve)' in out and 'HIDDEN_DEMO_BODY' not in out)
        for s in ('Browse documentation libraries (completed)','Search Planning Analytics documentation (completed)','Knowledgebase information retrieval (completed)'):check(s in clean(out))
    record('Shipped no-backend ANSI diagnostic shows cyan/red with no raw result body',diagnostic)
    def no_terminfo():
        env=dict(os.environ,TERM='paa-unknown-terminal',PYTHONDONTWRITEBYTECODE='1');env.pop('NO_COLOR',None)
        out=inherited.tty_run(['bash',APP/'xLaunchpad.sh','--preview'],env,APP).decode();check('\x1b[36m' in out and 'Planning Analytics' in out)
    record('Original menu retains ANSI fallback when terminfo is unavailable',no_terminfo)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report',default=str(PKG/'audit/offline-test-results.json'));args=parser.parse_args()
    fatal=''
    try:
        inherited.unit_tests();inherited.style_discovery_tests();RESULTS.extend(inherited.RESULTS)
        content_tests()
        with tempfile.TemporaryDirectory(prefix='paa-v3-tests-') as temp:
            work=Path(temp)
            previous.utility_tests(work)
            target=installation_tests(work)
            previous.runtime_tests(work,target)
            extra_style_tests(work)
        RESULTS.extend(previous.RESULTS)
    except Exception as exc:
        fatal=f'{type(exc).__name__}: {exc}'
        for result in inherited.RESULTS+previous.RESULTS:
            if result not in RESULTS:RESULTS.append(result)
        record('Suite completed',lambda:check(False,fatal))
    data=dict(release='PAA-3.0.0',complete=not fatal,passed=sum(r['status']=='PASS' for r in RESULTS),failed=sum(r['status']=='FAIL' for r in RESULTS),fatal_error=fatal,scope='Offline and loopback-only; strict fake Bob and synthetic PTY traces; not live IBM acceptance',tests=RESULTS)
    p=Path(args.report);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='tests'},indent=2))
    return 1 if fatal or data['failed'] else 0
if __name__=='__main__':sys.exit(main())
