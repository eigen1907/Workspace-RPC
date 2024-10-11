#!/bin/bash

cd /afs/cern.ch/user/j/joshin/public/RPCEffTnP/CMSSW_14_1_0/src
cmsenv

ERA=$1
#ERA=Run2022
INPUT_DIR="/eos/user/j/joshin/TnP-Flat-NanoAOD/${ERA}*/*/*"

OUTPUT_FILE="/afs/cern.ch/user/j/joshin/public/Workspace-RPC/Log/NanoAOD-TnP/240923/merge/${ERA}.root"

INPUT_FILES=$(ls ${INPUT_DIR}/*.root)

python3 ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/scripts/rpc-tnp-merge-flat-nanoaod.py \
    -i ${INPUT_FILES} \
    -o ${OUTPUT_FILE}