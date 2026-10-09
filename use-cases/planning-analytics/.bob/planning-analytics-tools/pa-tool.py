#!/usr/bin/env python3
"""Bounded Planning Analytics utilities. Python 3.9+, standard library only.

All commands are local/read-only except scaffold/output files within this appliance
and the explicitly opted-in HTTPS GET metadata probe. No TM1 writes, subprocess
shell, package installation, credential persistence or raw retrieval dumps.
"""
from __future__ import annotations
import argparse
import base64
import csv
from decimal import Decimal, InvalidOperation, localcontext
import json
import math
import os
from pathlib import Path
import re
import shutil
import ssl
import sys
import tempfile
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.bob/runtime/bob-v2'))
from project_permissions import normalize_tree
KB=ROOT/'.bob/planning-analytics-knowledgebase'
TEMPLATES=ROOT/'.bob/planning-analytics-templates'
OFFERINGS={'dedicated-cloud','saas','local','certified-containers','software-hub'}
MAX_INPUT=16*1024*1024
MAX_ROWS=100000
class ToolError(Exception): pass

def safe_file(value: str | Path, limit: int=MAX_INPUT) -> Path:
    path=Path(value).expanduser().absolute()
    current=Path(path.anchor)
    for part in path.parts[1:]:
        current/=part
        if current.is_symlink(): raise ToolError('Symlink input/output paths are not accepted.')
    if not path.is_file(): raise ToolError('Input must be an existing regular file.')
    if path.stat().st_size>limit: raise ToolError('Input exceeds the bounded utility size limit.')
    return path

def read_json(path: str | Path) -> dict:
    try: data=json.loads(safe_file(path).read_text(encoding='utf-8-sig'))
    except (UnicodeError,json.JSONDecodeError,RecursionError): raise ToolError('Invalid UTF-8 JSON input.')
    if not isinstance(data,dict):raise ToolError('Expected a JSON object.')
    return data

def output_file(path: str) -> Path:
    p=Path(path).expanduser()
    if not p.is_absolute():p=ROOT/p
    p=p.absolute()
    if '..' in p.parts:raise ToolError('Output traversal is forbidden.')
    store=ROOT/'bob-planning-analytics-store'
    if not p.is_relative_to(store):raise ToolError('Evidence outputs must be inside bob-planning-analytics-store/.')
    current=ROOT
    for part in p.relative_to(ROOT).parts:
        current/=part
        if current.is_symlink():raise ToolError('Symlink output path rejected.')
    if p.exists():raise ToolError('Refusing to overwrite an existing evidence output.')
    return p

def emit(data: dict, output: str | None=None) -> None:
    # Only aggregate diagnostics and explicitly requested evidence, never raw input records.
    encoded=json.dumps(data,indent=2,allow_nan=False)+'\n'
    if output:
        p=output_file(output);p.parent.mkdir(parents=True,exist_ok=True)
        fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o777)
        with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(encoded)
        p.chmod(0o777)
        normalize_tree(ROOT/'bob-planning-analytics-store')
    print(encoded,end='')

def nonempty(value: Any) -> bool:
    return isinstance(value,str) and bool(value.strip()) and not any(x in value.upper() for x in ('REVIEW_REQUIRED','TODO','REPLACE_ME'))

def profile_check(data: dict) -> dict:
    errors=[];reviews=[]
    offering=data.get('offering')
    if offering not in OFFERINGS:errors.append('offering must identify one supported appliance workflow.')
    if type(data.get('production')) is not bool:errors.append('production must be an explicit boolean.')
    for name in ['environment','provider','tm1_version','identity_model']:
        if not nonempty(data.get(name)):reviews.append('Resolve '+name+'.')
    if data.get('tm1_generation') not in ('11','12'):reviews.append('Resolve tm1_generation independently from front-end versions.')
    components=data.get('components')
    if not isinstance(components,dict) or not components:errors.append('components must be a nonempty version map.')
    elif not all(nonempty(k) and nonempty(v) for k,v in components.items()):reviews.append('Resolve all selected component versions.')
    if offering in ('saas','dedicated-cloud'):
        if not nonempty(data.get('region')):reviews.append('Resolve hosted region.')
        if data.get('install_managed_servers') is True:errors.append('Hosted workflows must not install IBM-managed servers.')
    if offering=='software-hub':
        if not nonempty(data.get('software_hub_version')):reviews.append('Resolve Software Hub control-plane/service alignment.')
        for name in ['operators_project','operands_project']:
            if not nonempty(data.get(name)):reviews.append('Resolve '+name+'.')
        if data.get('operators_project') and data.get('operators_project')==data.get('operands_project'):
            reviews.append('Review identical operators/operands projects against the exact supported topology.')
    evidence=data.get('support_evidence',{})
    if not isinstance(evidence,dict):errors.append('support_evidence must be an object.');evidence={}
    for key in ('spcr','conformance','release_notes'):
        if not nonempty(evidence.get(key)):reviews.append('Record applicable '+key+' evidence or an explicit supported non-applicability rationale.')
    if data.get('entitlement_confirmed') is not True:reviews.append('Confirm entitlement.')
    if data.get('production') is True:
        if data.get('technical_preview') is True:errors.append('A technical preview is not accepted for production by this workflow.')
        if data.get('recovery_tested') is not True:reviews.append('Complete an isolated restore and reconciliation test.')
        if not nonempty(data.get('approved_change')):reviews.append('Record explicit production change authorization.')
    # Reject credential-bearing profiles; use protected environment/secret references instead.
    def walk(obj):
        if isinstance(obj,dict):
            for key,value in obj.items():
                if re.search(r'(^|_)(password|api_key|authorization|access_token|secret)(_|$)',str(key),re.I) and value not in ('',None):
                    errors.append('Profile contains a credential-like value; use a secret reference instead.')
                walk(value)
        elif isinstance(obj,list):
            for item in obj:walk(item)
    walk(data)
    return {'operation':'profile-check','status':'INVALID' if errors else 'REVIEW_REQUIRED' if reviews else 'STRUCTURALLY_COMPLETE',
            'errors':sorted(set(errors)),'review_items':sorted(set(reviews)),
            'supported_configuration_certified':False,'live_environment_validated':False}

def config_check(text: str) -> dict:
    config={};duplicates=[];malformed=0
    for raw in text.splitlines():
        line=raw.strip()
        if not line or line.startswith(('#',';')):continue
        if '=' not in line:malformed+=1;continue
        k,v=line.split('=',1);k=k.strip().casefold();v=v.strip()
        if not k:malformed+=1;continue
        if k in config:duplicates.append(k)
        config[k]=v
    errors=[];reviews=[]
    if duplicates:errors.append('Duplicate configuration keys found; resolve precedence explicitly.')
    if malformed:errors.append('Malformed configuration lines found.')
    ports={}
    for name in ['portnumber','httpportnumber']:
        val=config.get(name,'')
        if not val:reviews.append('Missing '+name+'.')
        elif not val.isdecimal() or not 1<=int(val)<=65535:errors.append('Invalid '+name+' port.')
        else:ports[name]=int(val)
    if len(ports)==2 and len(set(ports.values()))==1:errors.append('Native and REST ports collide.')
    if config.get('usessl','').upper() not in ['T','TRUE','1']:
        errors.append('TLS is absent or not enabled in the inspected fragment; do not bypass verification.')
    for name in ('servername','databasedirectory','loggingdirectory'):
        if not config.get(name):reviews.append('Missing '+name+'.')
    reviews.extend(['Verify release-specific identity/certificate settings and trust.','Validate exact SPCR and component conformance separately.'])
    return {'operation':'tm1-config-check','status':'INVALID' if errors else 'REVIEW_REQUIRED',
            'parsed_keys':len(config),'duplicate_key_count':len(set(duplicates)),'errors':errors,'review_items':reviews,
            'raw_values_displayed':False,'scope':'static Local fragment; no service or port was contacted'}

def decimal(value: str, context: str='value') -> Decimal:
    try:d=Decimal(value.strip())
    except (InvalidOperation,AttributeError):raise ToolError('Invalid numeric '+context+'.')
    if not d.is_finite() or d.copy_abs()>Decimal('1E30'):raise ToolError('Nonfinite or out-of-range numeric '+context+'.')
    if len(d.as_tuple().digits)>38 or not -30<=d.as_tuple().exponent<=30:
        raise ToolError('Numeric precision/exponent exceeds the bounded 38-digit, +/-30 exponent contract.')
    return d

def load_csv(path: str, columns: list[str]) -> list[dict]:
    p=safe_file(path)
    if len(columns)!=len(set(columns)):raise ToolError('Requested columns must be distinct.')
    try:
        with p.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f)
            if not reader.fieldnames or len(reader.fieldnames)!=len(set(reader.fieldnames)):
                raise ToolError('CSV needs unique headers.')
            if not set(columns)<=set(reader.fieldnames):raise ToolError('CSV is missing required columns.')
            rows=[]
            for row in reader:
                if len(rows)>=MAX_ROWS:raise ToolError('CSV exceeds the bounded row limit.')
                if None in row or any(row.get(k) is None for k in columns):raise ToolError('Malformed CSV record.')
                rows.append(row)
    except UnicodeError:raise ToolError('CSV must be UTF-8.')
    if not rows:raise ToolError('CSV has no data rows.')
    return rows

def reconcile(source: str,target: str,keys: list[str],value: str,tolerance: str,aggregate: bool=False) -> dict:
    tol=decimal(tolerance,'tolerance')
    if tol<0:raise ToolError('Tolerance must be nonnegative.')
    if not keys or any(not k for k in keys):raise ToolError('Provide at least one nonempty business key.')
    rows_a=load_csv(source,keys+[value]);rows_b=load_csv(target,keys+[value])
    def grouped(rows):
        output={};dups=0
        for row in rows:
            key=tuple(row[k] for k in keys)
            if any(not item.strip() for item in key):raise ToolError('Blank business key.')
            amount=decimal(row[value])
            if key in output:
                dups+=1
                if not aggregate:raise ToolError('Duplicate business key: explicit --aggregate is required; no records were silently merged.')
                output[key]+=amount
            else:output[key]=amount
        return output,dups
    a,da=grouped(rows_a);b,db=grouped(rows_b)
    shared=set(a)&set(b);mismatch=sum(abs(a[k]-b[k])>tol for k in shared)
    missing_target=len(set(a)-set(b));missing_source=len(set(b)-set(a))
    return {'operation':'reconcile','status':'MATCH' if not(mismatch or missing_target or missing_source) else 'MISMATCH',
            'source_rows':len(rows_a),'target_rows':len(rows_b),'source_keys':len(a),'target_keys':len(b),
            'source_duplicate_rows':da,'target_duplicate_rows':db,'explicit_aggregation':aggregate,
            'common_keys':len(shared),'value_mismatches':mismatch,'missing_target_keys':missing_target,'missing_source_keys':missing_source,
            'source_total':str(sum(a.values(),Decimal(0))),'target_total':str(sum(b.values(),Decimal(0))),
            'absolute_tolerance_per_key':str(tol),'raw_records_displayed':False,'live_tm1_validated':False}

def evaluate(path: str) -> dict:
    rows=load_csv(path,['period','actual','predicted'])
    periods=[r['period'] for r in rows]
    if any(not x.strip() for x in periods) or len(periods)!=len(set(periods)):raise ToolError('Forecast periods must be unique and nonempty.')
    a=[decimal(r['actual']) for r in rows];p=[decimal(r['predicted']) for r in rows]
    errors=[pred-actual for actual,pred in zip(a,p)];n=Decimal(len(a));denom=sum(map(abs,a),Decimal(0))
    nonzero=[abs(err/act)*100 for act,err in zip(a,errors) if act!=0]
    with localcontext() as ctx:
        ctx.prec=80
        mae=sum(map(abs,errors),Decimal(0))/n
        rmse=(sum((x*x for x in errors),Decimal(0))/n).sqrt()
        bias=sum(errors,Decimal(0))/n
        wape=sum(map(abs,errors),Decimal(0))/denom*100 if denom else None
        mape=sum(nonzero,Decimal(0))/len(nonzero) if nonzero else None
    return {'operation':'forecast-evaluate','status':'SCORED','observations':len(a),'mae':str(mae),'rmse':str(rmse),
            'mean_error_predicted_minus_actual':str(bias),'wape_percent':str(wape) if wape is not None else None,
            'mape_percent_nonzero_actuals':str(mape) if mape is not None else None,'mape_excluded_zero_actuals':len(a)-len(nonzero),
            'zero_total_actual_policy':'WAPE null when sum(abs(actual)) = 0','training_performed':False,
            'forecast_quality_certified':False,'note':'Scoring provided pairs only; caller must establish holdout integrity and applicability.'}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise ToolError('Redirect refused to protect authorization and endpoint scope.')

def probe(service_root: str,offering: str,connect: bool,header_env: str | None,
          local_basic: bool,username_env: str,password_env: str,ca_file: str | None,timeout: int) -> dict:
    if not connect:raise ToolError('Network access requires explicit --connect; no request was sent.')
    if offering not in OFFERINGS:raise ToolError('Select an explicit offering.')
    if not 1<=timeout<=60:raise ToolError('Timeout must be between 1 and 60 seconds.')
    if any(ord(x)<33 for x in service_root):raise ToolError('Service root must be a valid URL without whitespace/control characters.')
    try:u=urllib.parse.urlsplit(service_root);port=u.port
    except ValueError:raise ToolError('Invalid service root URL.')
    if u.scheme!='https' or not u.hostname or u.username or u.password or u.query or u.fragment:
        raise ToolError('Use an explicit HTTPS service root without credentials, query or fragment.')
    if not u.path.rstrip('/').endswith('/api/v1'):
        raise ToolError('Supply the verified TM1 REST service root ending in /api/v1; paths are not inferred.')
    for name in filter(None,[header_env,username_env if local_basic else None,password_env if local_basic else None]):
        if not re.fullmatch(r'PA_[A-Z0-9_]+',name):raise ToolError('Use a dedicated PA_ credential environment variable, never a Bob key.')
    authorization=''
    if local_basic:
        if offering!='local' or header_env:raise ToolError('Explicit Local Basic is local-only and mutually exclusive with an authorization-header variable.')
        user=os.environ.get(username_env,'');password=os.environ.get(password_env,'')
        if not user or not password or ':' in user:raise ToolError('Local credentials are absent or invalid.')
        bob_key=os.environ.get('BOB_API_KEY','')
        if bob_key and (bob_key in user or bob_key in password):raise ToolError('Bob credentials must not be reused for TM1.')
        authorization='Basic '+base64.b64encode((user+':'+password).encode()).decode()
    elif header_env:authorization=os.environ.get(header_env,'')
    else:raise ToolError('Provide a dedicated verified Authorization environment variable or explicit approved Local Basic.')
    if not authorization or len(authorization)>16384 or any(ord(x)<32 or ord(x)==127 for x in authorization):raise ToolError('Authorization is absent or contains control characters.')
    if os.environ.get('BOB_API_KEY') and os.environ['BOB_API_KEY'] in authorization:
        raise ToolError('Bob credentials must not be reused for TM1.')
    cafile=str(safe_file(ca_file)) if ca_file else None
    ctx=ssl.create_default_context(cafile=cafile)
    opener=urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx),NoRedirect())
    url=service_root.rstrip('/')+'/$metadata'
    req=urllib.request.Request(url,method='GET',headers={'Authorization':authorization,'Accept':'application/xml','User-Agent':'PAA-readonly-metadata-probe/1.0'})
    try:
        with opener.open(req,timeout=timeout) as response:
            if response.status!=200:raise ToolError('Metadata probe returned a non-success status.')
            body=response.read(1024*1024+1)
        if len(body)>1024*1024:raise ToolError('Metadata response exceeded 1 MiB; not displayed or persisted.')
        if b'<!DOCTYPE' in body.upper() or b'<!ENTITY' in body.upper():raise ToolError('Unsafe XML declaration in metadata; not displayed.')
        root=ET.fromstring(body)
        if root.tag.split('}')[-1]!='Edmx':raise ToolError('Response is not recognized OData metadata; not displayed.')
    except urllib.error.HTTPError as exc:
        raise ToolError('Metadata probe returned HTTP '+str(exc.code)+'; response body withheld.')
    except (urllib.error.URLError,TimeoutError,ssl.SSLError,OSError):raise ToolError('Metadata probe failed at TLS/network/timeout layer; credentials and raw diagnostics withheld.')
    except ET.ParseError:raise ToolError('Metadata response is not valid XML; raw payload withheld.')
    return {'operation':'rest-probe','status':'METADATA_RECEIVED','http_method':'GET','http_status':200,'tls_verified':True,
            'raw_payload_displayed':False,'raw_payload_persisted':False,'database_writes_performed':False,
            'note':'Metadata connectivity is not proof of cube permissions, product support or complete service readiness.'}

def scaffold(name: str,offering: str,design_only: bool) -> dict:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) or len(name)>60:raise ToolError('Use a lowercase hyphenated project name of at most 60 characters.')
    base=ROOT/('bob-planning-analytics-designs' if design_only else 'bob-planning-analytics-store')
    if base.is_symlink():raise ToolError('Artifact directory symlink rejected.')
    base.mkdir(parents=True,exist_ok=True);target=base/name
    if target.exists() or target.is_symlink():raise ToolError('Project already exists; no files were overwritten.')
    staging=Path(tempfile.mkdtemp(prefix='.paa-scaffold-',dir=base))
    try:
        overview=f'# {name} - Planning Analytics {offering}\n\nThis is a scoped starting artifact, not a deployed planning service.\nResolve exact SKU, TM1 and component builds, identity, source/load contracts, support evidence, business acceptance and rollback. No live action is authorized by this scaffold.\n'
        (staging/'DESIGN.md' if design_only else staging/'README.md').write_text(overview)
        if not design_only:
            for source in ('source-contract.json','model-specification.json','acceptance-plan.md','ti-process-contract.md','upgrade-cutover.md'):
                shutil.copyfile(TEMPLATES/source,staging/source)
            profile=read_json(ROOT/'.bob/planning-analytics-profiles/deployment-profile.example.json');profile['offering']=offering
            (staging/'deployment-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
        for file in staging.iterdir():file.chmod(0o777)
        # Renaming onto an existing nonempty directory fails rather than merges it.
        if target.exists():raise ToolError('Concurrent project creation detected.')
        staging.chmod(0o777)
        staging.rename(target)
        normalize_tree(base)
    finally:
        if staging.exists():shutil.rmtree(staging)
    return {'operation':'scaffold','status':'CREATED','path':str(target.relative_to(ROOT)),'files':len(list(target.iterdir())),
            'offering':offering,'design_only':design_only,'live_deployment_performed':False}

def self_check() -> dict:
    issues=[]
    config=read_json(ROOT/'.bob/runtime/bob-v2/appliance.json')
    slugs=re.findall(r'^- slug: ([a-z0-9-]+)$',(ROOT/'.bob/custom_modes.yaml').read_text(),re.M)
    if config.get('code')!='PAA':issues.append('Wrong appliance identity.')
    if len(slugs)!=len(set(slugs)) or set(slugs)!=set(config.get('mode_slugs',[])):issues.append('Mode registry mismatch.')
    for s in slugs:
        p=ROOT/'.bob'/('rules-'+s)
        if not p.is_dir() or not list(p.glob('*.md')):issues.append('Missing mode rule binding.')
        if not config.get('mode_names',{}).get(s,'').startswith('IBM Bob Planning Analytics '):issues.append('Wrong mode display identity.')
    guide=read_json(KB/'index.json');refs=read_json(KB/'references.json')['references']
    original=KB/'sources/IBM_Planning_Analytics_Comprehensive_Guide.docx'
    if not original.is_file():issues.append('Original guide is missing.')
    for s in guide['guide_sections']:
        p=KB/s['path']
        if not p.is_file():issues.append('A guide section is missing.')
    # Reference counts and provenance hashes are informational, not admission gates.
    skills=list((ROOT/'.bob/skills').glob('*/SKILL.md'))
    for p in skills:
        text=p.read_text()
        if not text.startswith('---\n') or 'description:' not in text or 'name:' not in text:issues.append('Malformed skill frontmatter.')
        if 'BOB2-DOCUMENTATION-DISCOVERY-POLICY.md' not in text:issues.append('Skill lacks retrieval policy binding.')
    return {'operation':'self-check','status':'PASS' if not issues else 'FAIL','modes':len(slugs),'skills':len(skills),
            'guide_sections':len(guide['guide_sections']),'original_reference_urls':len(refs),'issues':sorted(set(issues)),
            'bob_or_backend_contacted':False,'product_support_certified':False}

def main(argv: list[str] | None=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='action',required=True)
    s=sub.add_parser('profile-check');s.add_argument('file');s.add_argument('--output')
    s=sub.add_parser('tm1-config-check');s.add_argument('file');s.add_argument('--output')
    s=sub.add_parser('reconcile');s.add_argument('source');s.add_argument('target');s.add_argument('--keys',required=True,help='comma-separated key columns');s.add_argument('--value',default='Amount');s.add_argument('--tolerance',default='0.01');s.add_argument('--aggregate',action='store_true');s.add_argument('--output')
    s=sub.add_parser('forecast-evaluate');s.add_argument('file');s.add_argument('--output')
    s=sub.add_parser('rest-probe');s.add_argument('--service-root',required=True);s.add_argument('--offering',choices=sorted(OFFERINGS),required=True);s.add_argument('--connect',action='store_true');s.add_argument('--authorization-env');s.add_argument('--local-basic-approved',action='store_true');s.add_argument('--username-env',default='PA_TM1_USER');s.add_argument('--password-env',default='PA_TM1_PASSWORD');s.add_argument('--ca-file');s.add_argument('--timeout',type=int,default=10);s.add_argument('--output')
    s=sub.add_parser('scaffold');s.add_argument('name');s.add_argument('--offering',choices=sorted(OFFERINGS),required=True);s.add_argument('--design-only',action='store_true')
    sub.add_parser('self-check')
    a=p.parse_args(argv)
    if a.action=='profile-check':data=profile_check(read_json(a.file))
    elif a.action=='tm1-config-check':data=config_check(safe_file(a.file).read_text(encoding='utf-8-sig'))
    elif a.action=='reconcile':
        with localcontext() as context:
            context.prec=80
            data=reconcile(a.source,a.target,[x.strip() for x in a.keys.split(',')],a.value,a.tolerance,a.aggregate)
    elif a.action=='forecast-evaluate':
        with localcontext() as context:
            context.prec=80
            data=evaluate(a.file)
    elif a.action=='rest-probe':data=probe(a.service_root,a.offering,a.connect,a.authorization_env,a.local_basic_approved,a.username_env,a.password_env,a.ca_file,a.timeout)
    elif a.action=='scaffold':data=scaffold(a.name,a.offering,a.design_only)
    else:data=self_check()
    emit(data,getattr(a,'output',None))
    return 1 if data['status'] in ('INVALID','MISMATCH','FAIL') else 3 if data['status']=='REVIEW_REQUIRED' else 0

if __name__=='__main__':
    try:sys.exit(main())
    except (ToolError,OSError,UnicodeError,InvalidOperation) as exc:
        # ToolError messages are deliberately bounded and do not interpolate input values.
        message=str(exc) if isinstance(exc,ToolError) else 'Local input or filesystem operation failed; no raw data/credentials displayed.'
        print(json.dumps({'status':'ERROR','message':message}),file=sys.stderr);sys.exit(2)
