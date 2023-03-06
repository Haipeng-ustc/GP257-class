# io-lab



## Getting started


http://zapad.stanford.edu/GP257/io-lab.git


You will need to do this lab on the SLURM cluster. 


Begin by loging in through Chrome Remote Desktop. 

Then request exclusive access to one of the compute nodes with X11 support

srun  --x11 --pty --exclusive  -p cpu  /bin/bash 

Activate the python environment in spack 

spack load python

Next clone the repository for the lab and open up this notebook


git clone http://zapad.stanford.edu/GP257/io-lab.git

cd io

jupyter notebook notebook.ipynb
