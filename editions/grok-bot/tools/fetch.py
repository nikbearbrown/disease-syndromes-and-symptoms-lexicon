"""Fetch evidence for all seeds: Wikipedia (pinned revision ids), Wikidata, stored raw under work/raw."""
import csv, json, time, sys, re, urllib.request, urllib.parse, concurrent.futures as cf
from pathlib import Path
RUN=Path(__file__).resolve().parents[1]; RAW=RUN/'work/raw'; RAW.mkdir(parents=True,exist_ok=True)
SEEDS=Path('/workspace/disease-lexicon-checkout/data/seeds.tsv')
UA={'User-Agent':'IndependentLexiconResearch/1.0 (github.com/nikbearbrown; private research run)'}
def get(url,params):
    for a in range(6):
        try:
            req=urllib.request.Request(url+'?'+urllib.parse.urlencode(params),headers=UA)
            return json.load(urllib.request.urlopen(req,timeout=60))
        except Exception as e:
            time.sleep(2+3*a); err=e
    raise err
WP='https://en.wikipedia.org/w/api.php'; WD='https://www.wikidata.org/w/api.php'
seeds=list(csv.DictReader(SEEDS.open(encoding='utf8'),delimiter='\t'))
# 1. info for seed pages themselves (no redirect resolving)
info={}
ids=[s['page_id'] for s in seeds]
for i in range(0,len(ids),50):
    r=get(WP,{'action':'query','format':'json','formatversion':2,'pageids':'|'.join(ids[i:i+50]),
              'prop':'info|revisions|pageprops','rvprop':'ids|timestamp|content','rvslots':'main'})
    for p in r['query']['pages']:
        rev=p['revisions'][0]
        info[str(p['pageid'])]={'title':p['title'],'redirect':p.get('redirect',False),'revid':str(rev['revid']),
            'rev_ts':rev['timestamp'],'qid':p.get('pageprops',{}).get('wikibase_item'),
            'wikitext':rev['slots']['main']['content'] if p.get('redirect') else None}
# 2. resolve redirects
for pid,v in info.items():
    if v['redirect']:
        m=re.match(r'\s*#redirect\s*\[\[([^\]|]+)',v['wikitext'],re.I)
        tgt=m.group(1).strip() if m else None
        title,_,frag=(tgt or '').partition('#')
        v['target']=title.replace('_',' ').strip(); v['fragment']=frag.strip() or None
# 3. content pages to fetch extracts for
content={}
for pid,v in info.items():
    if v['redirect']:
        if v.get('target'): content.setdefault(v['target'],None)
    else: content.setdefault(v['title'],None)
def fx(title):
    r=get(WP,{'action':'query','format':'json','formatversion':2,'titles':title,'redirects':1,
              'prop':'extracts|revisions|pageprops','explaintext':1,'exsectionformat':'wiki','rvprop':'ids|timestamp'})
    p=r['query']['pages'][0]
    if p.get('missing'): return title,{'missing':True}
    return title,{'title':p['title'],'revid':str(p['revisions'][0]['revid']),'rev_ts':p['revisions'][0]['timestamp'],
                  'qid':p.get('pageprops',{}).get('wikibase_item'),'text':p.get('extract',''),
                  'redirects':r['query'].get('redirects')}
with cf.ThreadPoolExecutor(4) as ex:
    for n,(t,d) in enumerate(ex.map(fx,list(content))):
        content[t]=d
        if n%100==0: print('extract',n,file=sys.stderr)
# 4. wikidata
qids=set(v['qid'] for v in info.values() if v['qid'])|set(d.get('qid') for d in content.values() if d.get('qid'))
qids.discard(None); qids=sorted(qids); wd={}
for i in range(0,len(qids),50):
    r=get(WD,{'action':'wbgetentities','format':'json','ids':'|'.join(qids[i:i+50]),'props':'labels|aliases|descriptions|claims|info|sitelinks','languages':'en','sitefilter':'enwiki'})
    for q,e in r['entities'].items():
        claims={}
        for pid,sts in e.get('claims',{}).items():
            vals=[s['mainsnak'].get('datavalue',{}).get('value') for s in sts]
            vals=[x['id'] for x in vals if isinstance(x,dict) and x.get('id','').startswith('Q')]
            if vals: claims[pid]=vals
        wd[q]={'qid':q,'label':e.get('labels',{}).get('en',{}).get('value',''),'description':e.get('descriptions',{}).get('en',{}).get('value',''),
               'aliases':[a['value'] for a in e.get('aliases',{}).get('en',[])],'claims':claims,'revision_id':str(e.get('lastrevid')),
               'enwiki':e.get('sitelinks',{}).get('enwiki',{}).get('title')}
# labels for referenced items in key properties
KEYP=['P31','P279','P361','P527','P780','P1542','P828','P1199','P2176','P1995','P737']
ref=sorted({x for e in wd.values() for p in KEYP for x in e['claims'].get(p,[])}-set(wd))
lab={}
for i in range(0,len(ref),50):
    r=get(WD,{'action':'wbgetentities','format':'json','ids':'|'.join(ref[i:i+50]),'props':'labels|sitelinks','languages':'en','sitefilter':'enwiki'})
    for q,e in r['entities'].items():
        lab[q]={'label':e.get('labels',{}).get('en',{}).get('value',''),'enwiki':e.get('sitelinks',{}).get('enwiki',{}).get('title')}
for q,e in wd.items(): lab[q]={'label':e['label'],'enwiki':e['enwiki']}
json.dump({'fetched_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'info':info,'content':content,'wikidata':wd,'labels':lab},
          open(RAW/'raw.json','w'),ensure_ascii=False)
print('done',len(info),len(content),len(wd),len(lab))
