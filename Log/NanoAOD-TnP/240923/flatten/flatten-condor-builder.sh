#!/bin/bash

CMSSW_BASE=/afs/cern.ch/user/j/joshin/public/RPCEffTnP/CMSSW_14_1_0/src
STORE=/eos/user/j/joshin
OUTPUT_DIR=TnP-NanoAOD
OUTPUT_FLATTEN_DIR=TnP-NanoAOD-flatten
CONFIG_FILE=flatten-condor-config-2022B.json

jq -r '.[] | "\(.primary_dataset),\(.proceed_dataset),\(.cert),\(.geometry)"' "${CONFIG_FILE}" | \
while IFS=',' read -r PRIMARY PROCEED CERT GEOM; do
    CONDOR_DATASET=${PRIMARY}-${PROCEED}
    mkdir ${CONDOR_DATASET}
    touch ${CONDOR_DATASET}/condor.dat 
    for OUTPUT in $(ls ${STORE}/${OUTPUT_DIR}/${PRIMARY}/${PROCEED}*/*/*/*.root); do
        OUTPUT=$(echo ${OUTPUT} | sed "s|/eos/user/j/joshin/||")
        OUTPUT_FLATTEN=$(echo ${OUTPUT} | sed "s|${OUTPUT_DIR}|${OUTPUT_FLATTEN_DIR}|")
        if [ "$OUTPUT" = "$OUTPUT_FLATTEN" ]; then
            echo "OUTPUT and OUTPUT_FLATTEN are the same. Exiting."
            exit 0
        fi
        echo ${OUTPUT} ${OUTPUT_FLATTEN} >> ${CONDOR_DATASET}/condor.dat
    done

    cat > ${CONDOR_DATASET}/condor.sub << EOF
Universe   = vanilla
Executable = flatten-condor-execute.sh
Arguments  = --cmssw_base ${CMSSW_BASE} \
--cert ${CERT} \
--geometry ${GEOM} \
--store ${STORE} \
--output \$(output) \
--output_flatten \$(output_flatten)
Log        = ${CONDOR_DATASET}/process-\$(Process).log
Error      = ${CONDOR_DATASET}/process-\$(Process).err
Queue output, output_flatten from ${CONDOR_DATASET}/condor.dat
EOF
    condor_submit ${CONDOR_DATASET}/condor.sub
done
