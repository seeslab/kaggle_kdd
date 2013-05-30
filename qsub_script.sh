#!/bin/bash
# The name of the job, can be whatever makes sense to you
#$ -N kaggle

# The job should be placed into the queue 'all.q'.
#$ -q all.q

# Merge output and standard output
#$ -j y

# The batchsystem should use the current directory as working directory.
# Both files will be placed in the current
# directory. The batchsystem assumes to find the executable in this directory.
#$ -cwd


#$ -t 1-1

# request Bourne shell as shell for job.
#$ -S /bin/bash

export PATH=/opt/python/bin:$PATH
source /opt/python/bin/virtualenvwrapper.sh
export WORKON_HOME=/export/home/shared/virtualenvs
workon kaggle_kdd
fab --list
