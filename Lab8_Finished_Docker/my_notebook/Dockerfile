# This dockerfile is used to build the Seismic Waveform Inversion Toolbox (SWIT)
# docker image, which is a 2-D acoustic Full-waveform Inversion (FWI) package 
# implemented in Fortran and Python. The package is available at 
# https://github.com/Haipeng-ustc/SWIT-1.0

# Using the Ubuntu image (our OS)
FROM ubuntu:latest

# Install the basic tools on ubuntu for compiling 
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    gfortran \
    wget \
    git \
    vim

# Install OpenMPI (MPI implementation)
RUN apt-get update && apt-get install -y \
    openmpi-bin \
    libopenmpi-dev


# Install the required packages including python3
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Install the required python packages
RUN pip3 install numpy obspy scipy matplotlib multiprocess PySimpleGUI psutil Pillow

# Download the source code and compile the SWIT-1.0 solver
RUN git clone https://github.com/Haipeng-ustc/SWIT-1.0.git && \
    cd SWIT-1.0/fd2dmpi/ && \
    make clean && \
    make


# Add the SWIT-1.0 solver
ENV PATH /SWIT-1.0/bin:$PATH

# Add the Python scripts for SWIT-1.0 to environment variable
ENV PYTHONPATH /SWIT-1.0/toolbox:$PYTHONPATH