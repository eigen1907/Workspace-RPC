cmsenv

for dir in ../240412/step2-condor_flatten/*
do
    if [ -d ${dir} ]
        then mv ${dir}/$(basename ${dir}).root data/
    fi
done