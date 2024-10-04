#!/bin/bash

CMSSW_BASE=/afs/cern.ch/user/j/joshin/public/RPCEffTnP/CMSSW_14_1_0/src

INPUT_DIR=/eos/user/j/joshin/TnP-NanoAOD
OUTPUT_DIR=/eos/user/j/joshin/TnP-NanoAOD-flatten

CONFIG_FILE=flatten-condor-config.json
jq -r '.[] | "\(.primary_dataset),\(.proceed_dataset),\(.lumi_cert),\(.geometry)"' "${CONFIG_FILE}" | \
while IFS=',' read -r PRIMARY PROCEED CERT GEOM; do
    CONDOR_DATASET=${PRIMARY}-${PROCEED}
    touch ${CONDOR_DATASET}.dat
    for OUTPUT in $(ls ${INPUT_DIR}/${PRIMARY}/${PROCEED}*/*/*/*.root); do
        OUTPUT_FLATTEN=$(echo ${OUTPUT} | sed "s|${INPUT_DIR}|${OUTPUT_DIR}|")
        echo ${OUTPUT} ${OUTPUT_FLATTEN} >> ${CONDOR_DATASET}.dat
    done

    cat > ${CONDOR_DATASET}.sub << EOF
Universe   = vanilla
Executable = flatten-condor-executer.sh
Arguments  = --cmssw_base ${CMSSW_BASE} \
--lumi_cert ${CERT} \
--geometry ${GEOM} \
--input \$(output) \
--output \$(output_flatten)
Log        = ${CONDOR_DATASET}.log
Error      = ${CONDOR_DATASET}.err
Queue output, output_flatten from ${CONDOR_DATASET}.dat
EOF
    condor_submit ${CONDOR_DATASET}.sub
done
