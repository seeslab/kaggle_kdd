#!/bin/bash
#
# SGE options
#$ -S /bin/bash
#$ -cwd
# Job array
#$ -t 1-38

/opt/python/bin/python coauthors_diff.py 100 $SGE_TASK_ID
