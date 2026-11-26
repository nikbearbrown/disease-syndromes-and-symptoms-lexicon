import sys, json
from common import *
bundles,views,raw=load(); LAB=raw['labels']; WD=raw['wikidata']
n=int(sys.argv[1]); lo=(n-1)*BATCH; hi=min(lo+BATCH,len(bundles))
maxs=int(sys.argv[2]) if len(sys.argv)>2 else 4
def L(q): return f"{q}({LAB.get(q,{}).get('label','?')})"
for i in range(lo,hi):
    b,v=bundles[i],views[i]; c=b['concept']
    head=f"#{v['idx']} {b['concept_id']} {c['preferred_name']} [{c['broad_class']}]"
    if v['redirect']: head+=f" REDIRECT->{v['target']}#{v.get('fragment')} sec={v.get('section')} tseed={v.get('target_seed')}"
    print(head)
    k=default_wp(b,v); w=b['wikipedia'][k]
    if v['redirect']: print('  rw:',b['wikipedia'][0]['text'][:150].replace('\n',' '))
    sn=snippets(w['text'])
    print(f"  WP {w['revision_id']} {w['title']}: "+' '.join(f"s{j+1}) {s}" for j,s in enumerate(sn[:maxs])) + (f" (+{len(sn)-maxs})" if len(sn)>maxs else ''))
    if v.get('fragment') and v.get('section'):
        # show section snippets index range
        st=w['text'].split('\n\n',1)[-1]; ss=snippets(st)
        off=len(sn)-len(ss)
        print('  SEC:',' '.join(f"s{off+j+1}) {s}" for j,s in enumerate(ss[:5])))
    for it in b['wikidata']:
        cl='; '.join(f"{p}:"+','.join(L(q) for q in qs[:3]) for p,qs in it['claims'].items() if p in ('P31','P279','P361','P828','P1542','P780','P527'))
        print(f"  WD {it['qid']} '{it['label']}' — {v['wd_desc'].get(it['qid'],'')} | {cl} | al: {'; '.join(it['aliases'][:5])}")
    for s in b['wordnet']:
        print(f"  WN {s['synset']} {s['lemmas']} {s['gloss'][:90]} | hyper {s['relations'].get('hypernym')}")
    if b['neighbors']: print('  NB:',', '.join(f"{x['name']}" for x in b['neighbors']))
