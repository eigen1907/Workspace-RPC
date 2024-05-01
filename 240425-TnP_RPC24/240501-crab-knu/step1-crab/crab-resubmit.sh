for f in crab_muRPCTnPFlatTableProducer_cfg*; do
  echo "--------------------------------------------"
  echo "Resubmit -> $f"
  crab resubmit $f --numcores 8 --maxjobruntime=2000
done