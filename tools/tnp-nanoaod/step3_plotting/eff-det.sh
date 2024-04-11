cmsenv

#rm -f {REPO}/test/step3_DrawTnPPlot/EffDetector/Run2022/

REPO=${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP
#TYPE=SingleMuon
#ERA=Run2022B

DATA=/eos/user/j/joshin/RPC_STORE/tnp-nanoaod-flatten/

#rpc-tnp-plot-eff-detector.py \
#    -i ${DATA}${TYPE}__${ERA}.root \
#    -g ${REPO}/data/geometry/run3.csv \
#    -s 13.6 \
#    -y ${ERA:3:8} \
#    -o ${REPO}/test/step3_DrawTnPPlot/EffDetector/${TYPE}__${ERA}/

rpc-tnp-plot-eff-detector.py \
    -i ${DATA}Run2022.root \
    -g ${REPO}/data/geometry/run3.csv \
    -s 13.6 \
    -y Run2022 \
    -o ${REPO}/test/step3_DrawTnPPlot/EffDetector/Run2022_2/