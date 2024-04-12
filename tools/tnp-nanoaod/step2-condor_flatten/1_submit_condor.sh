DATA_DIR=/pnfs/knu.ac.kr/data/cms/store/user/joshin/RPC/TnP-NanoAOD
CONFIG_FILE=config.csv

while IFS="," read -r TYPE PERIOD CERT
do
    bash execute.sh ${TYPE} ${PERIOD} ${CERT} ${DATA_DIR}
done < ${CONFIG_FILE}
