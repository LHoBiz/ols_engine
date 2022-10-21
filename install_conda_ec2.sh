#!/bin/bash

cd /usr/share
sudo wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sudo sh ./Miniconda3-latest-Linux-x86_64.sh -b

~/miniconda3/bin/conda init
source ~/.bashrc
conda config --append envs_dirs /usr/share/conda3/envs
conda remove --name ols_engine --all -y
conda create --prefix /usr/share/conda3/envs/ols_engine python=3.8 -y
conda activate ols_engine
source ~/.bashrc
conda install -n ols_engine gdal poppler tiledb=2.2 -y 
conda install -n ols_engine -c conda-forge postgresql -y 
conda install -n ols_engine -c conda-forge/label/gcc7 postgresql -y 
conda install -n ols_engine -c conda-forge/label/broken postgresql -y 
conda install -n ols_engine -c conda-forge/label/cf201901 postgresql -y 
conda install -n ols_engine -c conda-forge/label/cf202003 postgresql -y
