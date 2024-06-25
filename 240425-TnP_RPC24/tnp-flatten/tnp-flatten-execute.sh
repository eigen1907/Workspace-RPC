#!/bin/bash
python3 /users/hep/eigen1907/Workspace/Workspace-RPC/240425-TnP_RPC24/tnp-flatten/tnp-flatten-script.py \
    -i /users/hep/eigen1907/store/TnP-NanoAOD/240501-134734/SingleMuon/muRPCTnPFlatTableProducer_cfg__SingleMuon__Run2022B-27Jun2023-v1/240501_044806/0000/output_4.root \
    -c /users/hep/eigen1907/Workspace/Workspace-RPC/240425-TnP_RPC24/tnp-flatten/Cert_Collisions2022_eraB_355100_355769_Golden.json \
    -g /users/hep/eigen1907/Workspace/Workspace-RPC/240425-TnP_RPC24/tnp-flatten/run3.csv \
    -o /users/hep/eigen1907/Workspace/Workspace-RPC/240425-TnP_RPC24/tnp-flatten/flatten_output_1_filter.root \
    --roll-blacklist-path /users/hep/eigen1907/Workspace/Workspace-RPC/240425-TnP_RPC24/tnp-flatten/roll-blacklist-2022.json \
    --run-blacklist-path /users/hep/eigen1907/Workspace/Workspace-RPC/240425-TnP_RPC24/tnp-flatten/run-blacklist.json