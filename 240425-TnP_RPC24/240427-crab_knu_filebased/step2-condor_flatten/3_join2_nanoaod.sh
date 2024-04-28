#!/bin/bash
cmsenv
for dir in *
do
    if [ -d ${dir} ]
        then hadd run3.root ${dir}/$(basename ${dir}).root
    fi
done
