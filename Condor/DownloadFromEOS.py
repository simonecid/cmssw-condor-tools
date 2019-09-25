#!/usr/bin/env python

import os
import tempfile

SourceFile_LocalName_HDFSDestPath = [
  ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/l1tr/gpetrucc/106X/NewInputs104X/240719_oldhgc.done/TTbar_PU200/inputs104X_1.root", "inputs104X_1.root", "CMS_Phase_2/jetMETStudies/TTBar_200_10_0_4_MTD/inputs104X_1.root"],
  ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/l1tr/gpetrucc/106X/NewInputs104X/240719_oldhgc.done/TTbar_PU200/inputs104X_10.root", "inputs104X_10.root", "CMS_Phase_2/jetMETStudies/TTBar_200_10_0_4_MTD/inputs104X_10.root"],
  ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/l1tr/gpetrucc/106X/NewInputs104X/240719_oldhgc.done/TTbar_PU200/inputs104X_97.root", "inputs104X_97.root", "CMS_Phase_2/jetMETStudies/TTBar_200_10_0_4_MTD/inputs104X_97.root"],
  ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/l1tr/gpetrucc/106X/NewInputs104X/240719_oldhgc.done/TTbar_PU200/inputs104X_98.root", "inputs104X_98.root", "CMS_Phase_2/jetMETStudies/TTBar_200_10_0_4_MTD/inputs104X_98.root"],
  ["root://eoscms.cern.ch//eos/cms/store/cmst3/group/l1tr/gpetrucc/106X/NewInputs104X/240719_oldhgc.done/TTbar_PU200/inputs104X_99.root", "inputs104X_99.root", "CMS_Phase_2/jetMETStudies/TTBar_200_10_0_4_MTD/inputs104X_99.root"],
]

for entry in SourceFile_LocalName_HDFSDestPath:

  fd, path = tempfile.mkstemp()

  with os.fdopen(fd, 'w') as tmp: 
    jobDescription =  \
"""Universe = vanilla
job = copyFromEOSToHDFS_{LocalName}
cmd = copyFromEOSToHDFS.sh
args = {SourceFile} {LocalName} {HDFSDestPath}
# Better not to put logs in the same folder, as they are plenty
output = /storage/sb17498/logs/CMSSW/$(job)_$(cluster).$(process).out
error = /storage/sb17498/logs/CMSSW/$(job)_$(cluster).$(process).err
log = /storage/sb17498/logs/CMSSW/$(job)_$(cluster).$(process).log
should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/kreczko/workernode:centos7"
use_x509userproxy = true
getenv=True
request_cpus = 1
request_memory = 2000
request_disk = 3000000
queue 1""".format(SourceFile=entry[0], LocalName=entry[1], HDFSDestPath=entry[2])

    print "Submitting", "copyFromEOSToHDFS_" + entry[1] + ":\n" + jobDescription + "\n-----------------------"
    
    tmp.write(jobDescription)
    tmp.close()
    os.system("condor_submit " + path)

