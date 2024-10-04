for f in crab_muRPCTnPFlatTableProducer_cfg*; do
  echo "--------------------------------------------"
  echo "Resubmit -> $f"
  crab resubmit $f --numcores=8 --maxjobruntime=2750 --siteblacklist=T2_US_MIT
done