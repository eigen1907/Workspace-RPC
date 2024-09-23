for f in crab_muRPCTnPFlatTableProducer_cfg*; do
  echo "--------------------------------------------"
  echo "Resubmit -> $f"
  crab resubmit $f --numcores=8 --maxjobruntime=2750 --siteblacklist=T2_FR_IPHC,T2_FR_GRIF,T2_US_MIT
done