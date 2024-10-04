#!/bin/bash

#/eos/user/j/joshin/TnP-NanoAOD/Muon/Run2022C-27Jun2023-v1_muRPCTnPFlatTableProducer_cfg/240923_190846/0000
DATA_DIR=/eos/user/j/joshin/TnP-NanoAOD/
CONFIG_FILE=flatten-condor-config.csv

while IFS="," read -r TYPE PERIOD CERT
do
    bash execute.sh ${TYPE} ${PERIOD} ${CERT} ${DATA_DIR}
done < ${CONFIG_FILE}
