#!/bin/bash

cd /home/ec2-user
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh -b

# conda env export > environment.yml
git clone https://github.com/LHoBiz/ols_engine.git
git fetch
git checkout aws-linux
# sudo chown -R ec2-user /home/ec2-user/*
# sudo rm /home/ec2-user/ols_engine/v0.2/ -rf

/miniconda3/bin/conda init
source ~/.bashrc
conda create -n ols_engine python=3.8 -y
conda activate ols_engine
source ~/.bashrc
conda install gdal poppler tiledb=2.2 -y 
conda install -c conda-forge postgresql -y && conda install -c conda-forge/label/gcc7 postgresql -y && conda install -c conda-forge/label/broken postgresql -y && conda install -c conda-forge/label/cf201901 postgresql -y && conda install -c conda-forge/label/cf202003 postgresql -y
