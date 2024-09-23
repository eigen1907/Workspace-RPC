# RPC Geometry Fix

### Working meeting on iRPC Geometry in CMSSW
https://indico.cern.ch/event/1399804/

### xml file check(rpcf)
```sh
cmsrel CMSSW_14_1_0_pre2
cd CMSSW_14_1_0_pre2/src
cmsenv
git cms-addpkg Geometry/MuonCommonData
git cms-addpkg Geometry/CMSCommonData
git cms-addpkg Configuration/Geometry

${CMSSW_BASE}/src/Geometry/CMSCommonData/data/dd4hep/cmsExtendedGeometry2024.xml
${CMSSW_BASE}/src/Geometry/MuonCommonData/data/rpcf/2024/v1/rpcf.xml
```


