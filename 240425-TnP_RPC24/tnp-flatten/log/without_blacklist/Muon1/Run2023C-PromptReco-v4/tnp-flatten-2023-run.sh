#!/bin/bash
COND_PATH=/users/hep/eigen1907/Workspace/Workspace-RPC/data/efficiency

srun python3 tnp-flatten-script.py \
    -i $1 \
    -o $2 \
    -g ${COND_PATH}/geometry/run3.csv \
    -c ${COND_PATH}/cert/Cert_Collisions2023_366442_370790_Golden.json \
    #--roll-blacklist-path ${COND_PATH}/blacklist/roll-blacklist-2023.json \
    #--run-blacklist-path ${COND_PATH}/blacklist/run-blacklist.json
