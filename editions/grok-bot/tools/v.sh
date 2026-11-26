#!/bin/bash
cd /workspace/disease-lexicon-grok-run-20261124/tools && python3 view.py $1 > ../work/views/v$(printf %03d $1).txt
