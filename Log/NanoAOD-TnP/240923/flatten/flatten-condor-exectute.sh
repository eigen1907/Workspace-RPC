#!/bin/bash

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --cmssw_base) cmssw_base="$2"; shift ;;
        --lumi_cert) lumi_cert="$2"; shift ;;
        --geometry) geometry="$2"; shift ;;
        --input) input="$2"; shift ;;
        --output) output="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done


cd ${cmssw_base}
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
python3 ${cmssw_base}/src/RPCDPGAnalysis/NanoAODTnP/scripts/rpc-tnp-flatten-nanoaod.py \
     -c ${cmssw_base}/src/RPCDPGAnalysis/NanoAODTnP/data/cert/${lumi_cert} \
     -g ${cmssw_base}/src/RPCDPGAnalysis/NanoAODTnP/data/geometry/${geometry} \
     -i ${input} \
     -o ${output}
