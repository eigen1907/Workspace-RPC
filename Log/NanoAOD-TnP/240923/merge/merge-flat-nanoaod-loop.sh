ERA_LIST=(
    "SingleMuon/Run2022B"
    "SingleMuon/Run2022C" 
    "Muon/Run2022C"
    "Muon/Run2022D"
    "Muon/Run2022E"
    "Muon/Run2022F"
    "Muon/Run2022G" 
    "Muon0/Run2023B"
    "Muon0/Run2023C"
    "Muon0/Run2023D" 
    "Muon0/Run2024B"
    "Muon0/Run2024C"
    "Muon0/Run2024D"
    "Muon0/Run2024E"
    "Muon0/Run2024F"
    "Muon1/Run2023B"
    "Muon1/Run2023C"
    "Muon1/Run2023D" 
    "Muon1/Run2024B"
    "Muon1/Run2024C"
    "Muon1/Run2024D"
    "Muon1/Run2024E"
    "Muon1/Run2024F"
)

#echo ${ERA_LIST[@]}

for ERA in ${ERA_LIST[@]}; do
    echo ${ERA}
    bash merge-flat-nanoaod.sh ${ERA} 
done