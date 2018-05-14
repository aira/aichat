#!/bin/bash
# This script is meant to be called by the "install" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.
#
# This script is taken from Scikit-Learn (http://scikit-learn.org/)
#
# THIS SCRIPT IS SUPPOSED TO BE AN EXAMPLE. MODIFY IT ACCORDING TO YOUR NEEDS!
echo "Running travis_install.sh from working dir PWD=$PWD"
export PROJECT_NAME="aichat"
echo "PROJECT_NAME=$PROJECT_NAME"
export CENV_NAME=$PROJECT_NAME"_cenv"
# export DISTRIB="conda"
echo "CENV_NAME=$CENV_NAME"
export REQUIREMENTS_PATH="requirements-base.txt"
echo "REQUIREMENTS_PATH=$REQUIREMENTS_PATH"
DOWNLOAD_DIR=${DOWNLOAD_DIR:-$HOME/Downloads}
mkdir -p $DOWNLOAD_DIR
echo "DOWNLOAD_DIR=$DOWNLOAD_DIR"

if [ $# -eq 1 ] ; then
    export HOST_OS=$1  # linux or darwin
else
	export HOST_OS=$OSTYPE  # linux or darwin17
fi

set -e

echo "HOST_OS=$HOST_OS"

export UNVERSIONED_OS=${HOST_OS::6}
if [ $UNVERSIONED_OS == "darwin" ] ; then
    # since we're not on travis we need to set the BUILD_DIR
    export BUILD_DIR=$HOME/build
    mkdir -p $HOME/build

    export HOST_OS=$UNVERSIONED_OS  # linux or darwin
else
    # we're on travis so we need to exit with an error code on any error
    export UNVERSIONED_OS="linux"
	export HOST_OS=$UNVERSIONED_OS  # linux or darwin
fi

echo "UNVERSIONED_OS=$UNVERSIONED_OS"

if [ $UNVERSIONED_OS == "darwin" ] ; then
    brew install python3 portaudio swig
elif [ $UNVERSIONED_OS == "linux" ] ; then
	echo "not installing anything, assuming that travis already installed python3, pyaudio, swig, etc..."
 # sudo apt-get -qq -y update
 #    sudo apt-get install -y build-essential apt-utils gfortran git python3 python3-dev python3-setuptools python3-virtualenv python3-pip wget
 #    sudo apt-get build-dep -y python-pyaudio 
 #    sudo apt-get build-dep -y python3-pyaudio
 #    sudo apt-get install python-pyaudio python3-pyaudio
    # apt-get install -y nginx supervisor sqlite3 
fi

if [[ "$DISTRIB" == "conda" ]] ; then
    # Deactivate the travis-provided virtual environment and setup a conda-based environment instead
    deactivate || echo "no virtualenv has been activated yet (NOT running on a travis container)"


    # Use the anaconda3 installer

    if [[ -f "$DOWNLOAD_DIR/anaconda3.sh" || -f "$HOME/anaconda3/bin"  ]] ; then
        echo $(ls -hal $DOWNLOAD_DIR)
    else
        wget http://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh -O $DOWNLOAD_DIR/anaconda3.sh
        chmod +x $DOWNLOAD_DIR/anaconda3.sh
    fi

    if [[ -f "$HOME/anaconda3/bin"  ]] ; then
        echo $(ls -hal "$HOME/anaconda3")
    else
        bash $DOWNLOAD_DIR/anaconda3.sh -b -u -p $HOME/anaconda3
	    export PATH=$HOME/anaconda3/bin:$PATH
	    conda update -y conda
	    conda install -y pip swig nltk

	    # Configure the conda environment and put it in the path using the provided versions
	    if [[ -f "$ENVIRONMENT_YML" ]]; then
	        conda env create -n $CENV_NAME -f "$ENVIRONMENT_YML" || echo "conda env $CENV_NAME already exists"
	    else
	        echo "WARNING: Unable to find an environment.yml file !!!!!!"
	        conda create -n $CENV_NAME --yes python=$PYTHON_VERSION pip
	    fi
    fi

    source activate $CENV_NAME
    conda install -y pip swig nltk
    pip install --upgrade pip

    if [[ -f "$REQUIREMENTS_PATH" ]] ; then
    	echo "Installing requirements file $REQUIREMENTS_PATH from PWD=$PWD"
        pip install -r "$REQUIREMENTS_PATH"
   	else
        echo "Unable to find requirements file $REQUIREMENTS_PATH from PWD=$PWD"
        echo "Currently working directory: $PWD"
        echo "ls:"
        ls
    fi

    # download spacy English language model
    pip install spacy
	python -m spacy download en

    # download NLTK punkt, Penn Treebank, and wordnet corpora 
    pip install nltk
    python -c "import nltk; nltk.download('punkt'); nltk.download('treebank'); nltk.download('wordnet');"
    which python
    python --version

    # if [[ "$INSTALL_MKL" == "true" ]]; then
    #     TO_INSTALL="$TO_INSTALL -c anaconda mkl"
    # else
    #     TO_INSTALL="$TO_INSTALL -c anaconda nomkl"
    # fi

    # if [[ -n "$PANDAS_VERSION" ]]; then
    #     TO_INSTALL="$TO_INSTALL -c anaconda pandas=$PANDAS_VERSION"
    # fi

    # if [[ -n "$PYAMG_VERSION" ]]; then
    #     TO_INSTALL="$TO_INSTALL -c anaconda pyamg=$PYAMG_VERSION"
    # fi

    # if [[ -n "$PILLOW_VERSION" ]]; then
    #     TO_INSTALL="$TO_INSTALL -c anaconda pillow=$PILLOW_VERSION"
    # fi

    # conda create -n $CENV_NAME --yes $TO_INSTALL

    echo "conda list: $(conda list)"
    echo "pip freeze: $(pip freeze)"

elif [[ "$DISTRIB" == "ubuntu" ]]; then
    # Use standard ubuntu packages in their default version
    echo $DISTRIB
fi

if [[ "$COVERAGE" == "true" ]]; then
    pip install coverage coveralls
fi



