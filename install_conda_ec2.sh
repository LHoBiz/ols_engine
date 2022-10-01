#!/bin/bash

/miniconda3/bin/conda init
source ~/.bashrc
conda remove --name ols_engine --all -y
conda create -n ols_engine python=3.8 -y
conda activate ols_engine
source ~/.bashrc
conda install gdal poppler tiledb=2.2 -y 
sudo conda install -c conda-forge postgresql -y && conda install -c conda-forge/label/gcc7 postgresql -y && conda install -c conda-forge/label/broken postgresql -y && conda install -c conda-forge/label/cf201901 postgresql -y && conda install -c conda-forge/label/cf202003 postgresql -y
