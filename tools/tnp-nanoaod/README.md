# RPCDPGAnalysis/NanoAODTnP

## Recipes
### Setup
```sh
cmsrel CMSSW_14_1_0_pre2
cd ./CMSSW_14_1_0_pre2/src
cmsenv
git-cms-merge-topic sourcemaru:rpc-tnp-nanoaod_from-${CMSSW_VERSION}
git clone https://github.com/sourcemaru/RPCDPGAnalysis.git -b tnp-nanoaod
git clone https://github.com/sourcemaru/Workspace-RPC.git
scram b
```

### Test
```sh
cmsRun \
    ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/test/muRPCTnPFlatTableProducer_cfg.py \
    inputFiles=root://cmsdcadisk.fnal.gov//dcache/uscmsdisk/store/data/Run2023D/Muon1/AOD/PromptReco-v2/000/371/225/00000/5f3efe8c-de70-43e0-a8c7-a532844ca6c3.root
```

### CRAB job
```sh
rpc-crab-submit.py \
    -p ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/test/muRPCTnPFlatTableProducer_cfg.py \
    -i ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/data/crab/run3.json \
    -s T3_CH_CERNBOX \
    -u joshin \
    -n TnP_NanoAOD
```