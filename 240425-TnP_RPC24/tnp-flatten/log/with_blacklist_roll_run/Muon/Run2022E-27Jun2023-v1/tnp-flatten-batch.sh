#!/bin/bash
#SBATCH --job-name=flatten_tnp_nanoaod

STORE=/users/hep/eigen1907/store/TnP-NanoAOD
SCRIPT=$1 # tnp-flatten-2022-run.sh
DATA=$2   # SingleMuon/Run2022B-27Jun2023-v1

for INPUT_FILE in $(ls ${STORE}/crab_output/${DATA}/*/output_*.root); do
  OUTPUT_FILE=${STORE}/flatten_output/with_blacklist_roll_run/${DATA}/$(basename $(dirname ${INPUT_FILE}))/$(basename ${INPUT_FILE})
  sbatch ${SCRIPT} ${INPUT_FILE} ${OUTPUT_FILE}
done