DATA_DIR=/pnfs/knu.ac.kr/data/cms/store/user/joshin/RPC/TnP-NanoAOD-FileBased
DATE=240427
CONFIG_FILE=config.csv

while IFS="," read -r TYPE PERIOD CERT
do
    bash execute.sh ${TYPE} ${PERIOD} ${CERT} ${DATA_DIR} ${DATE}
done < ${CONFIG_FILE}
