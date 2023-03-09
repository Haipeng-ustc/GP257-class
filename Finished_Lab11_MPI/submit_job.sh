#!/bin/bash

# This script submits a job to the slurm cluster

# print the initial message
echo "Submitting jobs ..."

for file in *.slurm
do
    sbatch $file
done

# print the final message
echo "All jobs submitted"