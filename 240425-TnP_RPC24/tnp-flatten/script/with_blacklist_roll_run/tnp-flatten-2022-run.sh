#!/bin/bash
COND_PATH=/users/hep/eigen1907/Workspace/Workspace-RPC/data/efficiency

srun python3 tnp-flatten-script.py \
    -i $1 \
    -o $2 \
    -g ${COND_PATH}/geometry/run3.csv \
    -c ${COND_PATH}/cert/Cert_Collisions2022_355100_362760_Golden.json \
    --roll-blacklist-path ${COND_PATH}/blacklist/roll-blacklist-2022.json \
    --run-blacklist-path ${COND_PATH}/blacklist/run-blacklist.json



: << "END"
sbatch tnp-flatten-run.sh \
    /users/hep/eigen1907/store/TnP-NanoAOD/crab_output/SingleMuon/Run2022B-27Jun2023-v1/0000/output_15.root \
    /users/hep/eigen1907/store/TnP-NanoAOD/flatten_output/SingleMuon/Run2022B-27Jun2023-v1/0000/output_15.root
END