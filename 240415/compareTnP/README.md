# SegmentAndTrackOnRPC vs NanoAODTnP in 1 file

### data
```sh
xrdcp -v root://cms-xrd-global.cern.ch//store/data/Run2018A/SingleMuon/AOD/15Feb2022_UL2018-v1/50000/4147D578-E518-9F43-AD4B-820A378631E7.root .
```


### SegmentAndTrackOnRPC
```sh
cmsRun /u/user/sjws5411/Workspace/Efficiency/CMSSW_14_1_0_pre2/src/RPCDPGAnalysis/SegmentAndTrackOnRPC/test/step1_makeTHnSparse/analyzeRPCwithTnP_Z_cfg.py

python3 /u/user/sjws5411/Workspace/Efficiency/CMSSW_14_1_0_pre2/src/RPCDPGAnalysis/SegmentAndTrackOnRPC/test/step2_projection/project_efficiency.py -i hist.root
```


### NanoAODTnP
```sh
cmsRun \
    ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/test/muRPCTnPFlatTableProducer_cfg.py \
    inputFiles=file:///u/user/sjws5411/Workspace/Efficiency/CMSSW_14_1_0_pre2/src/Workspace-RPC/240415/4147D578-E518-9F43-AD4B-820A378631E7.root


python3 ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/scripts/rpc-tnp-flatten-nanoaod.py \
        -i ./output.root \
        -c ./Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON_MuonPhys.txt \
        -g ./run2.csv \
        -o flatten_output.root
```

