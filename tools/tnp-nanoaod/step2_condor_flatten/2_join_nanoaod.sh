#!/bin/bash
cmsenv
for dir in ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/test/step2_FlattenTnPNanoAOD/*
do
    if [ -d ${dir} ]
    then
        hadd /eos/user/j/joshin/RPC_STORE/tnp-nanoaod-flatten/$(basename ${dir}).root ${dir}/result/*.root
    fi
done