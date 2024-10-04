import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from Configuration.StandardSequences.Eras import eras
from Configuration.AlCa.GlobalTag import GlobalTag

options = VarParsing('analysis')
options.parseArguments()

process = cms.Process('RPCTnP', eras.Run3)
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('DPGAnalysis.MuonTools.muRPCTnPFlatTableProducer_cfi')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = autoCond['run3_data']

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        '/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/319e19de-d5f8-41e5-b3da-241451966576.root',
        '/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/31b3403b-dc79-45e6-8542-e3803b53ee2c.root',
        '/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/31c4a3c5-cb9e-47d7-a0bc-aaae59e58f19.root',
        '/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/31c9cf3c-0f2c-416e-9c87-8db1f18677b2.root',
        '/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/322d287f-dda6-47c4-8ec6-34fd70b3a425.root',
        '/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/32a0da3b-4217-463c-9b49-70cd52e79d21.root',
        #'/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/32fbc97a-d2c1-4ba7-8551-92e3ff525101.root',
        '/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/33c08dda-3c9e-4564-9ecd-d15fd2111a74.root',
        '/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/3468d499-653f-4c10-8399-7f64fdf10597.root',
        '/store/data/Run2024C/Muon1/AOD/PromptReco-v1/000/379/866/00000/3501a271-c7b2-4a1e-8e10-e46fd55fc7b7.root'
    ),
    secondaryFileNames = cms.untracked.vstring(),
    inputCommands=cms.untracked.vstring(
        'keep *',
        ### For 2022, 2023 Data
        'drop TotemFEDInfos_totemT2Digis_TotemT2_RECO',
        'drop TotemT2DigiedmNewDetSetVector_totemT2Digis_TotemT2_RECO',
        'drop TotemVFATStatusedmDetSetVector_totemT2Digis_TotemT2_RECO',
        ### For 2024 Data
        'drop floatBXVector_gtStage2Digis_CICADAScore_RECO',
    )
)

process.muRPCTnPFlatTableProducer.tagMuonTriggerMatchingPaths = [
    "HLT_IsoMu24",
    "HLT_IsoMu27",
    "HLT_IsoMu30",
    "HLT_Mu50",
    "HLT_Mu55"
]
process.rpcTnPPath = cms.Path(process.muRPCTnPFlatTableProducer)

process.load('PhysicsTools.NanoAOD.NanoAODEDMEventContent_cff')
outputCommands = process.NANOAODEventContent.outputCommands
outputCommands.extend([
    'keep nanoaodFlatTable_*_*_*',
    #'drop edmTriggerResults_*_*_*',
])
process.out = cms.OutputModule('NanoAODOutputModule',
    fileName = cms.untracked.string('Run2024C_Muon1.root'),
    outputCommands = outputCommands,
    SelectEvents = cms.untracked.PSet(
        SelectEvents=cms.vstring('rpcTnPPath')
    )
)

process.end = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.rpcTnPPath,
    process.end
)
