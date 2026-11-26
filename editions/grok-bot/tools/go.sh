#!/bin/bash
# compile batch $1 (logged), then render view for next batch; back up every 5 batches
cd /workspace/disease-lexicon-grok-run-20261124/tools && python3 compile.py $1 && python3 view.py $(($1+1)) > ../work/views/v$(printf %03d $(($1+1))).txt
if [ $(($1 % 5)) -eq 0 ]; then
  D=/cursor/stores/store-b70b09de-a0d7-4d1b-a3f4-5cf53c567708/disease-lexicon; mkdir -p $D
  tar czf $D/disease-lexicon-grok-run-20261124.tgz -C /workspace disease-lexicon-grok-run-20261124 && echo backup ok
fi
