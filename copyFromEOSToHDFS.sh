#!/bin/bash
echo "Running on $HOSTNAME"
/cvmfs/grid.cern.ch/centos7-ui-4.0.3-1_umd4v3/usr/bin/xrdcp $1 $2
/usr/bin/hdfs dfs -copyFromLocal $2 $3
rm $2