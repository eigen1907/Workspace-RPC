cmsenv
mkdir Run2023
rpc-tnp-plot-eff-detector.py \
    -i ${CMSSW_BASE}/Workspace-RPC/240425-TnP_RPC24/TnP_Plotting/data/Run2023.root \
    -g ${CMSSW_BASE}/Workspace-RPC/240425-TnP_RPC24/TnP_Plotting/geometry/run3.csv \
    -s 13.6 \
    -y 2022 \
    -o Run2023