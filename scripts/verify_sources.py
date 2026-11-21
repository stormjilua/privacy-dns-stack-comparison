#!/usr/bin/env python3
"""Package source, claim and decision-artifact checks. Network checks are opt-in."""
from pathlib import Path
import argparse,csv,hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def validate(root, online=False):
    errors=[]
    def issue(msg):errors.append(msg)
    def read(rel):
        try:return (root/rel).read_text()
        except (OSError,UnicodeError) as e:issue(f'{rel}: {e}');return ''
    try:data=json.loads(read('assets/projects.json'));ledger=json.loads(read('sources.json'))
    except ValueError as e:return [f'invalid JSON: {e}'],0,0,0,0
    text=read('README.md');rows=data.get('projects',[]);sources=ledger.get('sources',[])
    han=len(re.findall(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]',text))
    if len(text.split())<650:issue('README not substantive (minimum 650 words)')
    if han:issue(f'README CJK count={han}')
    if re.search(r'\b(?:Batch [ABCD]|Char|Primary search intent|Language: English)\b',text):issue('internal production label in README')
    if data.get('language')!='en' or ledger.get('language')!='en':issue('language must be en')
    if len(rows)<8:issue('fewer than 8 distinct projects')
    ids=[r.get('repository') for r in rows];sids=[s.get('repository') for s in sources]
    if len(set(ids))!=len(ids):issue('duplicate project identity')
    if len(set(sids))!=len(sids):issue('duplicate source identity')
    if set(ids)!=set(sids):issue('source/project identity sets differ')
    required=['name','repository','url','category','primary_scope','secondary_capability','deployment_or_storage_model','best_for','limitation_to_verify','license_model','claim_status']
    claims=0;by_id={s.get('repository'):s for s in sources}
    for row in rows:
        rid=row.get('repository','?');s=by_id.get(rid,{})
        for field in required:
            if not row.get(field):issue(f'{rid}: missing {field}')
        if s.get('url')!=row.get('url'):issue(f'{rid}: source URL mismatch')
        for doc in s.get('documents',[]):
            rel=doc.get('path','');path=root/rel
            if not path.is_file():issue(f'{rid}: missing snapshot {rel}');continue
            if hashlib.sha256(path.read_bytes()).hexdigest()!=doc.get('sha256'):issue(f'{rid}: snapshot hash mismatch {rel}')
        if not s.get('claims'):issue(f'{rid}: no located claims')
        for c in s.get('claims',[]):
            claims+=1
            for f in ['claim_id','field','upstream_url','version_or_commit','checked_at','snapshot_path','upstream_excerpt','review_result']:
                if not c.get(f):issue(f'{rid}: claim missing {f}')
            if c.get('field') in row and c.get('statement')!=row[c['field']]:issue(f'{rid}: claim statement/field mismatch: {c.get("field")}')
            path=root/c.get('snapshot_path','__missing__')
            if path.is_file():
                lines=path.read_text().splitlines();a=c.get('line_start',0);b=c.get('line_end',0)
                if not 1<=a<=b<=len(lines):issue(f'{rid}: bad excerpt location')
                elif '\n'.join(lines[a-1:b])!=c.get('upstream_excerpt'):issue(f'{rid}: excerpt/lines mismatch')
            else:issue(f'{rid}: claim snapshot missing')
        if online and row.get('source_kind')=='gitiles':
            try:
                u=s['documents'][0]['upstream_url']
                p=subprocess.run(['curl','-sS','-L','--connect-timeout','4','--max-time','20','-x','http://127.0.0.1:19001','-w','\n%{http_code}',u],capture_output=True,text=True,timeout=30)
                if p.returncode or not p.stdout.endswith('\n200'):issue(f'{rid}: no reachable official Gitiles source')
            except (KeyError,IndexError,subprocess.TimeoutExpired) as e:issue(f'{rid}: network check {e}')
        elif online:
            try:
                p=subprocess.run(['git','-c','http.proxy=http://127.0.0.1:19001','ls-remote','--symref',s['clone_url'],'HEAD'],capture_output=True,text=True,timeout=75)
                if p.returncode or not re.search(r'^[0-9a-f]{40,64}\s+HEAD$',p.stdout,re.M):issue(f'{rid}: no reachable public HEAD')
            except (KeyError,subprocess.TimeoutExpired) as e:issue(f'{rid}: network check {e}')
    artifact=data.get('decision_artifact',{})
    path=root/artifact.get('path','__missing__')
    if not path.is_file():issue('decision artifact missing')
    else:
        if artifact.get('path') not in text:issue('README does not link decision artifact')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=artifact.get('sha256'):issue('decision artifact hash mismatch')
        if len(artifact.get('axes',[]))<3:issue('decision artifact has fewer than three distinct axes')
    acceptance=root/'acceptance.json'
    if acceptance.is_file():
        try:
            cert=json.loads(acceptance.read_text())
            for rel,want in cert.get('sha256',{}).items():
                path=root/rel
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=want:issue('acceptance hash mismatch: '+rel)
        except ValueError:issue('invalid acceptance JSON')
    return errors,len(rows),len(sources),han,claims

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--online',action='store_true');ap.add_argument('--root',type=Path,default=ROOT);args=ap.parse_args()
    errors,n,s,han,claims=validate(args.root,args.online)
    print(f'checked={n} sources={s} claims={claims} language=en cjk={han} errors={len(errors)} network={"online" if args.online else "offline"}')
    for e in errors:print(e)
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
