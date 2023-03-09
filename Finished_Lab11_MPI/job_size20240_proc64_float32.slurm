#!/bin/bash
#SBATCH --ntasks=64
#SBATCH --ntasks-per-node=16
#SBATCH --partition=serc
#SBATCH --exclusive
#SBATCH --nodes=4
#SBATCH -o job_size20240_proc64_float32.%N.%j.out  # STDOUT
#SBATCH -e job_size20240_proc64_float32.%N.%j.err  # STDERR

#SBATCH --threads-per-core=1
#SBATCH --time=00:30:00

#****************************************************#
# Author:
# Thomas Cullison, Stanford University, 2023
#



##*****************************************##
## size of N for N*N matrix
MATSIZE=20240


##*****************************************##
## Header Info
echo;
echo "Starting sbatch script";
echo "DATE: $(date), NTASKS: $SLURM_NTASKS, NNODES: $SLURM_NNODES";
echo;


##*****************************************##
## SPACK setup (like modules)
# echo ". /home/spack/spack/share/spack/setup-env.sh";
# . /home/spack/spack/share/spack/setup-env.sh;
# echo;
# echo "spack load intel-oneapi-mpi";
# spack load intel-oneapi-mpi;
# echo "which mpiexec";
# which mpiexec;
# echo "spack load python@3.10.8";
# spack load python@3.10.8;
# echo "python --version";
# python --version 2>&1;

## load modules on Sherlock
echo "module load py-mpi4py/3.1.3_py39";
module load py-mpi4py/3.1.3_py39;
echo "python --version";
python --version 2>&1;

##*****************************************##
## MPI
MY_MPI_MATMUL="matmult_mpi_float32.py"
echo;
echo "Running MatMul";
echo;
echo "mpiexec -n $SLURM_NTASKS python $MY_MPI_MATMUL $MATSIZE";
mpiexec -n $SLURM_NTASKS python $MY_MPI_MATMUL $MATSIZE;
echo;


##*****************************************##
## Footer Info
echo;
echo "Done...";
echo "DATE: $(date), NTASKS: $SLURM_NTASKS, NNODES: $SLURM_NNODES";
