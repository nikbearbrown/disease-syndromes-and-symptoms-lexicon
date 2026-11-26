"""Expand the compact drafting notation in work/dsl/bNNN.txt into full draft entries, check, log attempts.
Usage: compile.py BATCH [--dry]   (BATCH=all to rebuild every compiled batch without logging)"""
import sys, json, re, time, datetime
sys.path.insert(0,'/workspace/disease-lexicon-checkout/replication/scripts')
from check import check
from common import *
bundles,views,raw=load()
byid={b['concept_id']:i for i,b in enumerate(bundles)}
KINDS={'disease','syndrome','symptom','sign'}
ATT=RUN/'work/attempts.jsonl'
def attempts():
    d={}
    if ATT.exists():
        for l in open(ATT):
            r=json.loads(l); d.setdefault(r['concept_id'],[]).append(r)
    return d
def split(s,sep):
    out=[];cur='';depth=0
    for ch in s:
        if ch=='{': depth+=1
        if ch=='}': depth-=1
        if ch==sep and depth==0: out.append(cur.strip()); cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur.strip())
    return [x for x in out if x]
def parse_line(line):
    f=[x.strip() for x in line.split('|')]
    if len(f)!=8: raise ValueError(f'expected 8 fields, got {len(f)}: {line[:80]}')
    return f
def resolve(ptr,b,ent,wpo,text_of=None):
    """shorthand -> full pointer"""
    ch=ent['links']
    if re.match(r'^(wp|wd|wn|ex):',ptr): return ptr
    m=re.match(r'^s(\d+)$',ptr)
    if m:
        sn=snippets(wpo['text']); return f"wp:{wpo['revision_id']}#quote={sn[int(m.group(1))-1]}"
    if ptr.startswith('q:'): return f"wp:{wpo['revision_id']}#quote={ptr[2:]}"
    m=re.match(r'^(P\d+)=(Q\d+)$',ptr)
    if m: return f"wd:{ch['wikidata']['choice']}#{ptr}"
    if ptr=='a': return f"wd:{ch['wikidata']['choice']}#alias={text_of}"
    if ptr.startswith('a:'): return f"wd:{ch['wikidata']['choice']}#alias={ptr[2:]}"
    if ptr=='l': return f"wn:{ch['wordnet']['choice']}#lemma={text_of}"
    if ptr.startswith('l:'): return f"wn:{ch['wordnet']['choice']}#lemma={ptr[2:]}"
    m=re.match(r'^h:(\w+)=(\S+)$',ptr)
    if m: return f"wn:{ch['wordnet']['choice']}#{m.group(1)}={m.group(2)}"
    raise ValueError('bad pointer shorthand '+ptr)
def claim_with_ptrs(s):
    """text{cond}^p1,p2 -> (text,cond,ptrs)"""
    ptrs=[];cond=None
    if '^' in s: s,p=s.rsplit('^',1); ptrs=[x.strip() for x in p.split(',') if x.strip()]
    m=re.match(r'^(.*?)\{(.*)\}\s*$',s)
    if m: s,cond=m.group(1),m.group(2)
    return s.strip(),cond,ptrs
def build(line,batch):
    N,ws,df,dp,vs,rs,fl,op=parse_line(line)
    i=int(N)-1; b=bundles[i]; v=views[i]; cid=b['concept_id']
    opts={}
    for o in split(op,'~'):
        k,_,val=o.partition('='); opts[k.strip()]=val.strip()
    flags=split(fl,';')
    oos=ws.startswith('OOS')
    # links
    wpi=default_wp(b,v)
    links={}
    wpo=b['wikipedia'][wpi]
    if opts.get('wp','').startswith('-') or oos:
        links['wikipedia']={'choice':None,'reason':opts.get('wp','-')[2:] or ('Page is out of scope for the lexicon; no terminology sense to link.' if oos else 'Abstained.')}
    else:
        if opts.get('wp'): wpi=int(opts['wp'])-1; wpo=b['wikipedia'][wpi]
        if v['redirect'] and wpi==1:
            r=f"Seed page redirects to '{wpo['title']}'; pinned target revision {wpo['revision_id']} carries the evidence for this sense."
        else: r=f"Pinned revision {wpo['revision_id']} of '{wpo['title']}' describes this concept."
        links['wikipedia']={'choice':wpo['revision_id'],'reason':r}
    cands=[x['qid'] for x in b['wikidata']]
    wdc=opts.get('wd')
    if oos: links['wikidata']={'choice':None,'reason':'Page is out of scope for the lexicon; no terminology sense to link.'}
    elif wdc and wdc.startswith('-'): links['wikidata']={'choice':None,'reason':wdc[2:] or 'Abstained: no candidate item matches this sense.'}
    elif not cands: links['wikidata']={'choice':None,'reason':'No Wikidata candidate in the bundle.'}
    else:
        q=wdc or cands[0]
        lab=next(x['label'] for x in b['wikidata'] if x['qid']==q)
        links['wikidata']={'choice':q,'reason':f"Item {q} ('{lab}') is the item for this page and matches the sense."}
    wnc=opts.get('wn')
    if not b['wordnet']: links['wordnet']={'choice':None,'reason':'No WordNet synset for this name in the bundle.'}
    elif oos or not wnc or wnc.startswith('-'):
        links['wordnet']={'choice':None,'reason':(wnc or '-:')[2:] or ('Page is out of scope.' if oos else 'No WordNet sense in the bundle matches this clinical sense.')}
    else:
        syn=b['wordnet'][int(wnc)-1]['synset']
        links['wordnet']={'choice':syn,'reason':f"Synset {syn} glosses the same concept."}
    ent={'concept_id':cid,'work_sense':'Out of scope' if oos else ws,'links':links}
    if oos:
        ent['definition']={'text':'Out of scope','basis':'model_knowledge','pointers':[]}
        ent['variants']=[];ent['relations']=[]
        reason=ws.split(':',1)[1].strip() if ':' in ws else 'no terminology sense'
        flags=[f'out-of-scope: {reason}']+flags
    else:
        ps=[resolve(p,b,ent,wpo) for p in split(dp,',') if p!='mk']
        ent['definition']={'text':df,'basis':'source' if ps else 'model_knowledge','pointers':ps}
        ent['variants']=[]
        for s in split(vs,';'):
            t,c,ptr=claim_with_ptrs(s); ps=[resolve(p,b,ent,wpo,t) for p in ptr]
            ent['variants'].append({'text':t,'condition':c,'basis':'source' if ps else 'model_knowledge','pointers':ps})
        ent['relations']=[]
        nbn={n['name'].lower():n['id'] for n in b['neighbors']}
        for s in split(rs,';'):
            t,note,ptr=claim_with_ptrs(s); typ,_,lab=t.partition(':'); typ=typ.strip(); lab=lab.strip()
            ps=[resolve(p,b,ent,wpo,lab) for p in ptr]; tid=nbn.get(lab.lower())
            ent['relations'].append({'type':typ,'target_label':lab,'target_id':tid,'proposed_new':tid is None,
                                     'basis':'source' if ps else 'model_knowledge','pointers':ps,'note':note})
    # kind
    kind='unclassified'; kp=[]
    if opts.get('k'):
        kk,_,kps=opts['k'].partition('^'); kind=kk
        assert kind in KINDS, kind
        kp=[resolve(p,b,ent,wpo) for p in split(kps,',')]
        assert kp, 'kind needs a source pointer'
    if kind=='unclassified' and not oos and not any(f.startswith('kind-unclassified') for f in flags):
        flags.append('kind-unclassified: the linked sources do not explicitly class this page as a disease, syndrome, symptom or sign')
    # automatic redirect flags (facts from the bundle)
    if v['redirect']:
        tgt=v['target']+('#'+v['fragment'] if v.get('fragment') else '')
        if v.get('target_seed'):
            nm=[bundles[byid[k]]['concept']['preferred_name'] for k in v['target_seed']]
            if not any(f.startswith('duplicate') or f.startswith('redirect-to-seed-section') for f in flags):
                flags.insert(0,f"duplicate: page redirects to seed '{nm[0]}' ({v['target_seed'][0]})")
        else:
            flags.insert(0,f"redirect-unmapped: page redirects to non-seed page '{tgt}'; mapping left to the maintainer")
        if v.get('fragment') and not v.get('section'):
            flags.insert(1,f"redirect-section-missing: section '{v['fragment']}' is absent from pinned revision {b['wikipedia'][1]['revision_id']} of '{v['target']}'")
    ent['flags']=flags
    ent['_meta']={'model':'Grok Bot','model_string':'unknown','model_version':'unknown',
        'run_mode':'batched: drafted by the agent in batches of 15 seeds within one session (approved deviation from fresh-context-per-seed)',
        'batch':batch,'batch_size':BATCH,'kind':kind,'kind_pointers':kp,'attempts':None}
    return cid,ent,kind
def dsl_files(): return sorted((RUN/'work/dsl').glob('b*.txt'))
def compile_batch(n):
    out={}
    p=RUN/f'work/dsl/b{n:03d}.txt'
    for line in open(p,encoding='utf8'):
        if not line.strip() or line.startswith('//'): continue
        cid,ent,kind=build(line.rstrip('\n'),n); out[cid]=(ent,kind)
    return out
def main():
    arg=sys.argv[1]; dry='--dry' in sys.argv
    batches=[int(p.stem[1:]) for p in dsl_files()] if arg=='all' else [int(arg)]
    att=attempts(); newlog=[]
    alld={}
    for n in [int(p.stem[1:]) for p in dsl_files()]:
        try: alld.update(compile_batch(n))
        except Exception as e:
            print(f'batch {n} parse error: {e}'); 
            if n in batches: return 1
    if dry:
        from verify_drafts import ngrams
        for n in batches:
            for c,(ent,kind) in compile_batch(n).items():
                src=set()
                for w in bundles[byid[c]]['wikipedia']: src|=ngrams(w['text'],9)
                hit=ngrams(ent['definition']['text'],9)&src
                if hit: print('SELF-REVIEW copy',views[byid[c]]['idx'],[' '.join(h) for h in list(hit)[:2]]); bad=True
        if 'bad' in dir(): sys.exit(3)
        print('dry ok'); return 0
    for n in batches:
        lo=(n-1)*BATCH; hi=min(lo+BATCH,len(bundles))
        exp=[b['concept_id'] for b in bundles[lo:hi]]
        miss=[c for c in exp if c not in alld]
        if miss: print('MISSING in batch',n,miss)
        for c in exp:
            if c not in alld: continue
            ent,kind=alld[c]; b=dict(bundles[byid[c]]); b['concept']=dict(b['concept'],kind=kind)
            errs,warns=check(ent,b)
            prev=att.get(c,[])
            if arg!='all':
                if not prev or (len(prev)==1 and prev[0]['errors'] and True):
                    if not prev or prev[0]['errors']:
                        if len(prev)<2:
                            newlog.append({'concept_id':c,'batch':n,'attempt':len(prev)+1,'errors':errs,'at':datetime.datetime.now().isoformat(timespec='seconds')})
            if errs: print('FAIL',views[byid[c]]['idx'],c,errs)
    with open(ATT,'a') as f:
        for r in newlog: f.write(json.dumps(r)+'\n')
    att=attempts()
    # write partial outputs in seed order
    with open(RUN/'work/drafts.partial.jsonl','w',encoding='utf8') as fd, open(RUN/'work/bundles.partial.jsonl','w',encoding='utf8') as fb:
        for b in bundles:
            c=b['concept_id']
            if c not in alld: continue
            ent,kind=alld[c]; ent['_meta']['attempts']=max(1,len(att.get(c,[])))
            fd.write(json.dumps(ent,ensure_ascii=False)+'\n')
            bb=dict(b); bb['concept']=dict(b['concept'],kind=kind); fb.write(json.dumps(bb,ensure_ascii=False)+'\n')
    done=sorted(int(p.stem[1:]) for p in dsl_files())
    json.dump({'batches_done':done,'records_drafted':len(alld),'updated':datetime.datetime.now().isoformat(timespec='seconds')},open(RUN/'work/progress.json','w'))
    print(f'compiled {len(alld)} records; logged {len(newlog)} attempts')
import sys as _s; _s.exit(main() or 0)
