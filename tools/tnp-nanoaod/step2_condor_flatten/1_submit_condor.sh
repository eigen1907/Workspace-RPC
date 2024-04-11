DATA_DIR=/eos/user/j/joshin/RPC/TnP-NanoAOD
CONFIG_FILE=./config.csv

while IFS="," read -r TYPE PERIOD CERT
do
    ./makeCondor.sh ${TYPE} ${PERIOD} ${CERT} ${DATA_DIR}
done < ${CONFIG_FILE}