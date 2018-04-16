#!/bin/bash
# This script is meant to be called by the "install" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.
#
# This script is taken from Scikit-Learn (http://scikit-learn.org/)
#
# THIS SCRIPT IS SUPPOSED TO BE AN EXAMPLE. MODIFY IT ACCORDING TO YOUR NEEDS!

set -e

if [[ "$DISTRIB" == "conda" ]]; then
    # Deactivate the travis-provided virtual environment and setup a
    # conda-based environment instead
    deactivate

    # Use the anaconda3 installer
    DOWNLOAD_DIR=${DOWNLOAD_DIR:-$HOME/.tmp/anaconda3}
    mkdir -p $DOWNLOAD_DIR
    wget http://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh \
        -O $DOWNLOAD_DIR/anaconda3.sh
    chmod +x $DOWNLOAD_DIR/anaconda3.sh && \
        bash $DOWNLOAD_DIR/anaconda3.sh -b -u -p $HOME/anaconda3 && \
        # rm -r -d -f $DOWNLOAD_DIR
    export PATH=$HOME/anaconda3/bin:$PATH
    conda update -y conda
    conda install -y pip swig nltk

    # Configure the conda environment and put it in the path using the provided versions
    if [[ -f "$ENVIRONMENT_YML" ]]; then
        conda env create -n testenv -f "$ENVIRONMENT_YML"
    else
        echo "WARNING: Unable to find an environment.yml file !!!!!!"
        conda create -n testenv --yes python=$PYTHON_VERSION pip
    fi
    source activate testenv
    conda install -y pip

    # download spacy English language model
    pip install --upgrade spacy
    python -m spacy download en

    # download NLTK punkt, Penn Treebank, and wordnet corpora 
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

    # conda create -n testenv --yes $TO_INSTALL

    echo "conda list: $(conda list)"
    echo "pip freeze: $(pip freeze)"

elif [[ "$DISTRIB" == "ubuntu" ]]; then
    # Use standard ubuntu packages in their default version
    echo $DISTRIB
fi

if [[ "$COVERAGE" == "true" ]]; then
    pip install coverage coveralls
fi
