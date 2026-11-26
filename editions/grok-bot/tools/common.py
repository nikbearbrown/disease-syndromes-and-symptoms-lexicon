import json, re
from pathlib import Path
RUN=Path(__file__).resolve().parents[1]
BATCH=15
def load():
    bundles=[json.loads(l) for l in open(RUN/'work/bundles.base.jsonl',encoding='utf8')]
    views=json.load(open(RUN/'work/views.json'))
    raw=json.load(open(RUN/'work/raw/raw.json'))
    return bundles,views,raw
def default_wp(b,v):
    return 1 if v['redirect'] else 0
def snippets(text):
    out=[]
    for para in text.split('\n'):
        para=para.strip()
        if not para or para.startswith('='): continue
        for sent in re.split(r'(?<=[.!?;:])\s+',para):
            w=sent.split()
            for i in range(0,len(w),18):
                ch=' '.join(w[i:i+18]).strip()
                if len(ch.split())>=3: out.append(ch)
    return out
