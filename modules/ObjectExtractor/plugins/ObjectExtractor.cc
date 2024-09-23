// -*- C++ -*-
//
// Package:    TrackPropagator/ObjectExtractor
// Class:      ObjectExtractor
//
/**\class ObjectExtractor ObjectExtractor.cc TrackPropagator/ObjectExtractor/plugins/ObjectExtractor.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Jongwon Shin
//         Created:  Thu, 07 Mar 2024 04:22:23 GMT
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonChamberMatch.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"

#include "Geometry/RPCGeometry/interface/RPCGeometry.h"
#include "Geometry/RPCGeometry/interface/RPCGeomServ.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"
#include <vector>


//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.

class ObjectExtractor : public edm::one::EDAnalyzer<edm::one::SharedResources> 
{
public:
  explicit ObjectExtractor(const edm::ParameterSet&);
  ~ObjectExtractor() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  // ----------member data ---------------------------
  edm::EDGetTokenT<reco::TrackCollection> tracksToken_;  //used to select what tracks to read from configuration file
  edm::EDGetTokenT<reco::MuonCollection> muonsToken_;
  
  TTree* tree;
  
  /*
  std::vector<float> track_pt;
  std::vector<float> track_px;
  std::vector<float> track_py;
  std::vector<float> track_pz;
  std::vector<float> track_eta;
  std::vector<float> track_phi;
  std::vector<float> track_ch;
  */

  std::vector<float> muon_e;
  std::vector<float> muon_pt;
  std::vector<float> muon_px;
  std::vector<float> muon_py;
  std::vector<float> muon_pz;
  std::vector<float> muon_eta;
  std::vector<float> muon_phi;
  std::vector<float> muon_ch;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
ObjectExtractor::ObjectExtractor(const edm::ParameterSet& iConfig): 
  tracksToken_(consumes<reco::TrackCollection>(iConfig.getUntrackedParameter<edm::InputTag>("tracksTag"))),
  muonsToken_(consumes<reco::MuonCollection>(iConfig.getUntrackedParameter<edm::InputTag>("muonsTag")))
{
  edm::Service<TFileService> fs;
  tree = fs->make<TTree>("Events", "Events");

  /*
  tree->Branch("track_pt", &track_pt);
  tree->GetBranch("track_pt")->SetTitle("track_pt");
  tree->Branch("track_px", &track_px);
  tree->GetBranch("track_px")->SetTitle("track_px");
  tree->Branch("track_py", &track_py);
  tree->GetBranch("track_py")->SetTitle("track_py");
  tree->Branch("track_pz", &track_pz);
  tree->GetBranch("track_pz")->SetTitle("track_pz");
  tree->Branch("track_eta", &track_eta);
  tree->GetBranch("track_eta")->SetTitle("track_eta");
  tree->Branch("track_phi", &track_phi);
  tree->GetBranch("track_phi")->SetTitle("track_phi");
  tree->Branch("track_ch", &track_ch);
  tree->GetBranch("track_ch")->SetTitle("track_ch");
  */


  tree->Branch("muon_e", &muon_e);
  tree->GetBranch("muon_e")->SetTitle("muon_e");
  tree->Branch("muon_pt", &muon_pt);
  tree->GetBranch("muon_pt")->SetTitle("muon_pt");
  tree->Branch("muon_px", &muon_px);
  tree->GetBranch("muon_px")->SetTitle("muon_px");
  tree->Branch("muon_py", &muon_py);
  tree->GetBranch("muon_py")->SetTitle("muon_py");
  tree->Branch("muon_pz", &muon_pz);
  tree->GetBranch("muon_pz")->SetTitle("muon_pz");
  tree->Branch("muon_eta", &muon_eta);
  tree->GetBranch("muon_eta")->SetTitle("muon_eta");
  tree->Branch("muon_phi", &muon_phi);
  tree->GetBranch("muon_phi")->SetTitle("muon_phi");
  tree->Branch("muon_ch", &muon_ch);
  tree->GetBranch("muon_ch")->SetTitle("muon_ch");
}

ObjectExtractor::~ObjectExtractor() 
{
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
  //
  // please remove this method altogether if it would be left empty
}


// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void ObjectExtractor::fillDescriptions(edm::ConfigurationDescriptions& descriptions) 
{
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters

  edm::ParameterSetDescription desc;
  desc.addUntracked<edm::InputTag>("tracksTag", edm::InputTag("generalTracks"));
  desc.addUntracked<edm::InputTag>("muonsTag", edm::InputTag("muons"));
  //desc.setUnknown();
  descriptions.add("objectExtractorDefault", desc);
}


//
// member functions
//

// ------------ method called for each event  ------------
void ObjectExtractor::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) 
{
  using namespace edm;
  using namespace std;

  /*
  track_pt.clear();
  track_px.clear();
  track_py.clear();
  track_pz.clear();
  track_eta.clear();
  track_phi.clear();
  track_ch.clear();
  */

  muon_e.clear();
  muon_pt.clear();
  muon_px.clear();
  muon_py.clear();
  muon_pz.clear();
  muon_eta.clear();
  muon_phi.clear();
  muon_ch.clear();

  /*
  for (const auto& track : iEvent.get(tracksToken_)) 
  {
    track_pt.push_back(track.pt());
    track_px.push_back(track.px());
    track_py.push_back(track.py());
    track_pz.push_back(track.pz());
    track_eta.push_back(track.eta());
    track_phi.push_back(track.phi());
    track_ch.push_back(track.charge());
  }
  */

  for (const auto& muon: iEvent.get(muonsToken_))
  {
    muon_e.push_back(muon.energy());
    muon_pt.push_back(muon.pt());
    muon_px.push_back(muon.px());
    muon_py.push_back(muon.py());
    muon_pz.push_back(muon.pz());
    muon_eta.push_back(muon.eta());
    muon_phi.push_back(muon.phi());
    muon_ch.push_back(muon.charge());

    const auto muonInnerTrack = muon.innerTrack();
    const auto muonOuterTrack = muon.outerTrack();
    //const auto muonGlobalTrack = muon.globalTrack();
    const auto muonChamberMatches = muon.matches();

    cout << "isGlobalMuon: " << muon.isGlobalMuon() << endl;

    cout << "innerTrack's outerPosition: " << muonInnerTrack->outerPosition()
         << " / innerTrack's outerMomentum: " << muonInnerTrack->outerMomentum() << endl;

    cout << "outerTrack's innerPosition: " << muonOuterTrack->innerPosition()
         << " / outerTrack's innerMomentum: " << muonOuterTrack->innerMomentum() << endl;
 

    for (const auto& match: muonChamberMatches)
    {
      cout << "station: " << match.station()
           << ", muonSubdetId: " << match.detector()      
           << ", rawDetId: " << match.id.rawId() << endl; 

      //RPCDetId rpcDetId = static_cast<RPCDetId>(match.id.rawId());
      if ( match.detector() == MuonSubdetId::RPC )
      {
        RPCDetId rpcDetId = RPCDetId(match.id.rawId());
        string rollName = RPCGeomServ(rpcDetId).name();
        cout << rollName << endl;
      }

      //if ( match.detector() == MuonSubdetId::RPC )
      //{
      //  DetId matchedId = match.id;
      //  string detName = RPCGeomServ(matchedId*);
      //  cout << detName << endl; 
      //  //cout << RPCGeomServ(match.id&).name() << endl;
      //}
    }
  }

  tree->Fill();
  return;
}

// ------------ method called once each job just before starting event loop  ------------
void ObjectExtractor::beginJob() 
{
  // please remove this method if not needed
}

// ------------ method called once each job just after ending the event loop  ------------
void ObjectExtractor::endJob() 
{
  // please remove this method if not needed
}

//define this as a plug-in
DEFINE_FWK_MODULE(ObjectExtractor);
