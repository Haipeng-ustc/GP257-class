# This script tests the mpi4py module for matrix multiplication on a square matrix
#   Note: The number of processes must be a perfect square. The matrix size must be 
#   divisible by the square root of the number of processes.
#
#   Usage: python test_mpi4py.py <matrix size>
#   Example with MPI: mpirun -n 4 python test_mpi4py.py 200
#
#   Author: Haipeng Li
#   Date: 2023-03-03
#   Stanford University


import sys

import numpy as np
from mpi4py import MPI

# Initialize MPI environment
comm = MPI.COMM_WORLD
worker_size = comm.Get_size()
rank = comm.Get_rank()

# Check command line arguments
if rank == 0:
    if len(sys.argv) != 2:
        print("Usage: python test_mpi4py.py <matrix size>")
        MPI.Finalize()
        sys.exit(1)

# Parse command line arguments
N = int(sys.argv[1])

# Define block sizes
size = int(np.sqrt(worker_size))
block_size = int(N // size)

# Setup the data type
dtype = np.float32

if rank == 0:
    # Check that the number of processes is a perfect square
    if int(np.sqrt(worker_size))**2 != worker_size:
        print("Error: the number of processes must be a perfect square")
        MPI.Finalize()
        exit(1)

    # Check that the matrix size is divisible by the square root of the number of processes
    if block_size*size != N:
        print("Error: the matrix size must be divisible by the square root of the number of processes")
        MPI.Finalize()
        exit(1)

    # Print matrix size and number of processes
    print("Size of the matrix :", N, "x", N)
    print("Number of processes:", worker_size)
    print("Size of local block:", block_size, "x", block_size)
    print("\n")

# Initialize local blocks of A and B for matrix multiplication on each process
local_A = np.zeros((block_size, N), dtype=dtype)
local_B = np.zeros((N, block_size), dtype=dtype)

if rank == 0:
    # Set random values for A and B
    A = np.random.rand(N, N).astype(dtype)
    B = np.random.rand(N, N).astype(dtype)

    # Initialize local blocks of A and B for sending to each process
    block_A = np.zeros((block_size, N), dtype=dtype)
    block_B = np.zeros((N, block_size), dtype=dtype)

    # Send blocks of A and B to each process
    for i in range(size):
        for j in range(size):
            proc = i*size+j
            print("Sending block", i, j, "to process", proc)
            block_A = np.ascontiguousarray(A[i*block_size:(i+1)*block_size, :])
            block_B = np.ascontiguousarray(B[:, j*block_size:(j+1)*block_size])
            if proc == 0:
                local_A = block_A
                local_B = block_B
            else:
                comm.Send(block_A, dest=proc, tag=0)
                comm.Send(block_B, dest=proc, tag=1)
else:
    # Receive local blocks of A and B from process 0 and store in local_A and local_B
    comm.Recv(local_A, source=0, tag=0)
    comm.Recv(local_B, source=0, tag=1)

# Compute local C on each process
local_C = np.matmul(local_A, local_B)

# Send local C to process 0 for gathering
if rank != 0:
    comm.Send(local_C, dest=0, tag=2)

# Receive local C from each process on process 0
else:
    C = np.zeros((N, N))
    for i in range(size):
        for j in range(size):
            proc = i*size+j
            if proc == 0:
                C[i*block_size:(i+1)*block_size, 
                  j*block_size:(j+1)*block_size] = local_C
            else:
                comm.Recv(local_C, source=proc, tag=2)
                C[i*block_size:(i+1)*block_size, 
                  j*block_size:(j+1)*block_size] = local_C

# Compare the MPI result with the serial result from np.matmul
if rank == 0:
    print("\nMPI result == Serial result: ", np.allclose(C, np.matmul(A, B)))
    assert np.allclose(C, np.matmul(A, B)), "MPI result != Serial result"
    print("\n")
    
# Stop the MPI and clean up the MPI environment
MPI.Finalize()
