#!/bin/bash
TYPE=with_blacklist_roll
WOKING_DIR=$(pwd)
EXE_ARGS=execute_args.csv
while IFS="," read -r SCRIPT DATA
do
    mkdir -p log/${TYPE}/${DATA}

    cp ./script/${TYPE}/tnp-flatten-script.py log/${TYPE}/${DATA}
    cp ./script/${TYPE}/tnp-flatten-batch.sh log/${TYPE}/${DATA}
    cp ./script/${TYPE}/${SCRIPT} log/${TYPE}/${DATA}
    cd log/${TYPE}/${DATA}
    
    bash ./tnp-flatten-batch.sh ${SCRIPT} ${DATA}

    cd ${WOKING_DIR}
done < ${EXE_ARGS}