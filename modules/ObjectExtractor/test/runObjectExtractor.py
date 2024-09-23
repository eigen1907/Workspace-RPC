import FWCore.ParameterSet.Config as cms

process = cms.Process("ObjectExtractor")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("file:20.0_step3.root")
)

process.object_extractor = cms.EDAnalyzer('ObjectExtractor')

process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("output.root"),
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True),
)

process.p = cms.Path(process.object_extractor)
