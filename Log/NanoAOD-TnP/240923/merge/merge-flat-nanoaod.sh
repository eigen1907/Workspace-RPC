#!/bin/bash

cd /afs/cern.ch/user/j/joshin/public/RPCEffTnP/CMSSW_14_1_0/src
cmsenv

INPUT_DIR="/eos/user/j/joshin/TnP-NanoAOD-flatten/SingleMuon/Run2022B-27Jun2023-v1_muRPCTnPFlatTableProducer_cfg/240923_190829/0000"
OUTPUT_FILE="/afs/cern.ch/user/j/joshin/public/Workspace-RPC/Log/NanoAOD-TnP/240923/merge/Run2022B.root"

INPUT_FILES=$(ls ${INPUT_DIR}/*.root)

python3 ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/scripts/rpc-tnp-merge-flat-nanoaod.py \
    -i ${INPUT_FILES} \
    -o ${OUTPUT_FILE}