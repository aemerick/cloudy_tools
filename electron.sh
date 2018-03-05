#!/bin/bash

#
# Code this to just loop through ALL files
#

for num in {1..26..1}
do

    fname1="hm_2011_sh_run"$num".physical"

    grep -B 1 'Physical' $fname1 | grep -v 'Physical' > temp.dat; grep -v '\--' temp.dat > temp2.dat

    sed -i "1s/^/PhyC_depth     Te      n_H    n_e    Htot    accel   fillfac\n/" temp2.dat

    fname2="hm_2011_sh_run"$num".electron"

    mv 'temp2.dat' $fname2
    rm temp.dat

done
