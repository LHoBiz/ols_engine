#!/bin/bash


~/miniconda3/bin/conda init
source ~/.bashrc
conda config --append envs_dirs /usr/share/conda3/envs
conda remove --name ols_engine --all -y
conda create --prefix /usr/share/conda3/envs/ols_engine python=3.8 -y
conda activate ols_engine
conda install -n ols_engine django -y
source ~/.bashrc
django-admin startproject lhobiz
cd lhobiz
python manage.py startapp ols_engine
python manage.py migrate
python manage.py makemigrations ols_engine
python manage.py migrate

python manage.py createsuperuser --noinput

python manage.py test ols_engine

conda install -n ols_engine -c conda-forge gdal
# conda install -n ols_engine tiledb=2.2 -y 
# conda install -n ols_engine -c conda-forge postgresql -y 
# conda install -n ols_engine -c conda-forge/label/gcc7 postgresql -y 
# conda install -n ols_engine -c conda-forge/label/broken postgresql -y 
# conda install -n ols_engine -c conda-forge/label/cf201901 postgresql -y 
# conda install -n ols_engine -c conda-forge/label/cf202003 postgresql -y

