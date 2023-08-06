# discon
Push python project to pypi and conda server

## Prerequisities

    conda install conda-build anaconda-client
    conda install -c conda-forge bumpversion


## Install

    conda install -c mjirik -c conda-forge discon

### Always upload

    conda config --set anaconda_upload yes

## Required user accounts

### Init PyPI

https://pypi.python.org/pypi

Create `~/.pypirc` with password and login

### Init Anaconda

https://anaconda.org/account/

Login to anaconda:

    anaconda login


## Project directory
You will need `setup.py`,  and `setup.cfg` in your python
project directory. Conda recipe files like `meta.yaml` should be in `conda-recipe` directory.
 
There also may be `bld.bat` and `build.sh` in `conda-recipe` dir. These
files are created if they do not exist.

All files can be generated with `init`.




## Usage

In new project you can generate `.condarc`, `setup.py`, `setup.cfg` and `meta.yml`

    python -m discon init
    
or

    python -m discon init project_name

Create and upload new patch, minor or major version

    python -m discon patch .
    python -m discon minor .
    python -m discon major . -c some_channel
    
You can stay on actual version and just build and upload package

    python -m discon stay .
    
Every particular step can be skipped by parameter. Read help for more info


    python -m discon --skip-upload patch . 


Push your git `master` branch to `stable` branch

    python -m discon stable



# Build

    conda build -c conda-forge .

