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

    # Use the miniconda installer for faster download / install of conda
    # itself
    DOWNLOAD_DIR=${DOWNLOAD_DIR:-$HOME/.tmp/miniconda}
    mkdir -p $DOWNLOAD_DIR
    wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh \
        -O $DOWNLOAD_DIR/miniconda.sh
    chmod +x $DOWNLOAD_DIR/miniconda.sh && \
        bash $DOWNLOAD_DIR/miniconda.sh -b -p $HOME/miniconda && \
        rm -r -d -f $DOWNLOAD_DIR
    export PATH=$HOME/miniconda/bin:$PATH
    conda update --yes conda

    conda env create -f environment.yml
    echo "python=$PYTHON_VERSION"
    # Configure the conda environment and put it in the path using the provided versions
    TO_INSTALL="python=$PYTHON_VERSION pip pytest pytest-cov \
                swig \
                numpy=$NUMPY_VERSION scipy=$SCIPY_VERSION \
                cython=$CYTHON_VERSION"

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
    source activate testenv

    # conda install -c mutirri pyaudio  # unsatisfiable because pyaudio 2.7 only works on python 2.7
    conda install --yes -c conda-forge speechrecognition

    pip install exrex regex

    conda list


elif [[ "$DISTRIB" == "ubuntu" ]]; then
    # Use standard ubuntu packages in their default version
    echo $DISTRIB
fi

if [[ "$COVERAGE" == "true" ]]; then
    pip install coverage coveralls
fi
