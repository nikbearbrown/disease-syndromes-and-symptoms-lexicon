"""Build bundles.jsonl (one per seed, in TSV order) from work/raw/raw.json, plus work/views.json for drafting."""
import csv, json, re, sys
from pathlib import Path
RUN=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/workspace/venv-clinlex/lib/python3.13/site-packages')
from nltk.corpus import wordnet as wn
raw=json.load(open(RUN/'work/raw/raw.json'))
info,content,WD,LAB=raw['info'],raw['content'],raw['wikidata'],raw['labels']
seeds=list(csv.DictReader(open('/workspace/disease-lexicon-checkout/data/seeds.tsv',encoding='utf8'),delimiter='\t'))
KEYP=['P31','P279','P361','P527','P780','P1542','P828','P1199','P2176','P1995','P737']
CATSLUG={'Category:Diseases and disorders':'diseases-and-disorders','Category:Infectious diseases':'infectious-diseases',
 'Category:Infectious diseases by mode of transmission':'infectious-diseases-by-mode-of-transmission','Category:Symptoms':'symptoms',
 'Category:Syndromes':'syndromes','Category:Medical signs':'medical-signs'}
def lead(t,limit=1400):
    t=t.split('\n== ')[0].split('\n==')[0].strip()
    if len(t)>limit:
        cut=t[:limit]; k=cut.rfind('. ')
        t=cut[:k+1] if k>300 else cut
    return t
def section(t,frag,limit=1200):
    f=frag.replace('_',' ').strip().lower()
    lines=t.split('\n')
    for i,l in enumerate(lines):
        m=re.match(r'^(=+)\s*(.*?)\s*=+\s*$',l)
        if m and m.group(2).lower()==f:
            lvl=len(m.group(1)); out=[l]
            for l2 in lines[i+1:]:
                m2=re.match(r'^(=+)\s*(.*?)\s*=+\s*$',l2)
                if m2 and len(m2.group(1))<=lvl: break
                out.append(l2)
            return 'heading','\n'.join(out).strip()[:limit]
    for l in lines:
        if l.lower().startswith(f) or (f in l.lower() and len(l)<1500 and not l.startswith('=')):
            return 'line',l.strip()[:limit]
    return None,''
title2seed={}
for s in seeds: title2seed.setdefault(s['preferred_name'].lower(),s['concept_id'])
def strip_paren(t): return re.sub(r'\s*\([^)]*\)\s*$','',t).strip()
# resolved page per seed
resolved={}
for s in seeds:
    v=info[s['page_id']]
    if v['redirect']:
        c=content.get(v['target'],{}); resolved[s['concept_id']]=c.get('title')
    else: resolved[s['concept_id']]=content[v['title']]['title']
page2seeds={}
for k,t in resolved.items(): page2seeds.setdefault(t,[]).append(k)
name={s['concept_id']:s['preferred_name'] for s in seeds}
def wnsyn(title):
    out=[]
    for lem in {strip_paren(title).replace(' ','_'),strip_paren(title).lower().replace(' ','_')}:
        for sy in wn.synsets(lem,pos='n'):
            if any(o['synset']==sy.name() for o in out): continue
            rel={}
            for r,fn in [('hypernym',sy.hypernyms),('hyponym',sy.hyponyms),('part_meronym',sy.part_meronyms),('part_holonym',sy.part_holonyms),('member_meronym',sy.member_meronyms),('member_holonym',sy.member_holonyms)]:
                xs=[x.name() for x in fn()][:12]
                if xs: rel[r]=xs
            out.append({'synset':sy.name(),'lemmas':[l.name().replace('_',' ') for l in sy.lemmas()],'gloss':sy.definition(),'relations':rel})
    return out
def wditem(q,extra=None):
    e=WD[q]; d={'qid':q,'label':e['label'],'aliases':e['aliases'],'claims':{p:e['claims'][p] for p in KEYP if p in e['claims']},'revision_id':e['revision_id']}
    return d
bundles=[];views=[]
for idx,s in enumerate(seeds,1):
    cid=s['concept_id']; v=info[s['page_id']]; cats=[c.strip() for c in s['direct_categories'].split('|')]
    wp=[];meta={'idx':idx,'cats':cats,'redirect':v['redirect']}
    qids=[]
    if v['redirect']:
        c=content.get(v['target'],{})
        wp.append({'title':v['title'],'revision_id':v['revid'],'text':v['wikitext'].strip()[:600]})
        txt=lead(c['text'],900); sec=None
        if v.get('fragment'):
            how,st=section(c['text'],v['fragment']); sec=how
            if st: txt=txt+'\n\n'+st
        wp.append({'title':c['title'],'revision_id':c['revid'],'text':txt})
        meta.update(target=c['title'],fragment=v.get('fragment'),section=sec,
                    target_seed=[k for k in page2seeds.get(c['title'],[]) if not info[[x for x in seeds if x['concept_id']==k][0]['page_id']]['redirect']] or None)
        if v['qid']: qids.append(v['qid'])
        if c.get('qid') and c['qid'] not in qids: qids.append(c['qid'])
    else:
        c=content[v['title']]
        wp.append({'title':c['title'],'revision_id':c['revid'],'text':lead(c['text'])})
        if v['qid']: qids.append(v['qid'])
    wdl=[wditem(q) for q in qids if q in WD]
    wnl=wnsyn(s['preferred_name'])
    # neighbors
    nb=[];why={}
    def add(k,r):
        if k!=cid and k not in why: nb.append({'id':k,'name':name[k]}); why[k]=r
    alltext=' '.join(w['text'] for w in wp).lower()
    for t,k in title2seed.items():
        tt=strip_paren(t)
        if len(tt)>=5 and re.search(r'(?<!\w)'+re.escape(tt)+r'(?!\w)',alltext): add(k,'title in excerpt')
    for it in wdl:
        for p in KEYP:
            for q in it['claims'].get(p,[]):
                t=(LAB.get(q,{}) or {}).get('enwiki')
                if t and t.lower() in title2seed: add(title2seed[t.lower()],f'wikidata {p}')
                for k in page2seeds.get(t,[]) if t else []: add(k,f'wikidata {p}')
    for k in page2seeds.get(resolved[cid],[]): add(k,'same resolved page')
    if v['redirect'] and v['target'].lower() in title2seed: add(title2seed[v['target'].lower()],'redirect target')
    nb=nb[:25]
    b={'concept_id':cid,'concept':{'id':cid,'preferred_name':s['preferred_name'],'kind':'unclassified',
        'broad_class':' | '.join(CATSLUG[c] for c in cats),'variants':[],'relations':[]},
       'neighbors':nb,'examples':[],'wikipedia':wp,'wikidata':wdl,'wordnet':wnl}
    bundles.append(b); meta['neighbor_method']={n['id']:why[n['id']] for n in nb}
    meta['wd_desc']={q:WD[q]['description'] for q in qids if q in WD}
    views.append(meta)
with open(RUN/'work/bundles.base.jsonl','w',encoding='utf8') as f:
    for b in bundles: f.write(json.dumps(b,ensure_ascii=False)+'\n')
json.dump(views,open(RUN/'work/views.json','w'),ensure_ascii=False)
print(len(bundles), sum(len(b['wordnet'])>0 for b in bundles),'with wn', sum(len(b['neighbors']) for b in bundles)/len(bundles),'avg nb')
