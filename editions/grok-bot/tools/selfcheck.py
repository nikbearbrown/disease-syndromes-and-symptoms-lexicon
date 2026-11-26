"""Pre-submission self-review: show any 9-word run shared between a definition and the bundle's Wikipedia text."""
import sys,json,re
sys.path.insert(0,'/workspace/disease-lexicon-checkout/replication/scripts')
from verify_drafts import ngrams
from common import RUN
B={json.loads(l)['concept_id']:json.loads(l) for l in open(RUN/'work/bundles.base.jsonl')}
for l in open(RUN/'work/drafts.partial.jsonl'):
    r=json.loads(l)
    if sys.argv[1:] and r['_meta']['batch']!=int(sys.argv[1]): continue
    src=set()
    for w in B[r['concept_id']]['wikipedia']: src|=ngrams(w['text'],9)
    hit=ngrams(r['definition']['text'],9)&src
    if hit: print(r['concept_id'],[' '.join(h) for h in list(hit)[:2]])
