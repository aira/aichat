#!/bin/bash
# Install all `./gradlew build` dependencies


#########################################
# Figure out the OS and path

SCRIPTS_DIR="$(dirname "$0")"
cd $HOME

if [ $# -eq 1 ] ; then
    export HOST_OS=$1  # linux or darwin
else
	export HOST_OS=$OSTYPE  # linux or darwin17
fi

echo "HOST_OS=$HOST_OS"

export UNVERSIONED_OS=${HOST_OS::6}
if [ $UNVERSIONED_OS == "darwin" ] ; then
    # since we're not on travis we need to set the BUILD_DIR
    export BUILD_DIR=$HOME/build
    mkdir -p $HOME/build

    export UNVERSIONED_OS="darwin"
    export HOST_OS=$UNVERSIONED_OS  # linux or darwin
else
    # we're on travis so we need to exit with an error code on any error
    set -e
    export UNVERSIONED_OS="linux"
	export HOST_OS=$UNVERSIONED_OS  # linux or darwin
fi

echo "HOST_OS=$HOST_OS"

export PROJECT_DIR=$BUILD_DIR/aira/aira-cabo-app

#
###################################################################


####################################################################
# Install OS package manager (brew) and python package manager (miniconda)

if test "$HOST_OS" == "darwin" ; then
	if test ! $(which brew) ; then
	    echo "Installing homebrew..."
	    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	fi

	if test ! $(which wget) ; then
		brew update
		brew install wget
	fi

	if test -e "$HOME/local/bin/python" ; then
	    echo "python already installed"
	else
		wget -c https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
		chmod +x Miniconda3-latest-MacOSX-x86_64.sh
		./Miniconda3-latest-MacOSX-x86_64.sh -b -p $HOME/miniconda
		export PATH=$HOME/miniconda/bin:$PATH
		echo 'export PATH=$HOME/miniconda/bin:$PATH' >> $HOME/.bash_profile
		conda upgrade -y conda
		conda env create --file "$SCRIPTS_DIR/environment.yml"
	    # # installing python 2.7.3
	    # mkdir -p ~/local
	    # wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
	    # tar xvzf Python-2.7.3.tgz
	    # cd Python-2.7.3
	    # ./configure
	    # make
	    # make altinstall prefix=~/local  # specify local installation directory
	    # ln -s ~/local/bin/python2.7 ~/local/bin/python
	    # cd ..
	    # # install setuptools and pip for package management
	    # wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz#md5=7df2a529a074f613b509fb44feefe74e
	    # tar xvzf setuptools-0.6c11.tar.gz
	    # cd setuptools-0.6c11
	    # ~/local/bin/python setup.py install  # specify the path to the python you installed above
	    # cd ..
	    # wget http://pypi.python.org/packages/source/p/pip/pip-1.2.1.tar.gz#md5=db8a6d8a4564d3dc7f337ebed67b1a85
	    # tar xvzf pip-1.2.1.tar.gz
	    # cd pip-1.2.1
	    # ~/local/bin/python setup.py install  # specify the path to the python you installed above
	    # # Now you can install other packages using pip
	    # ~/local/bin/pip install pandas
	fi
fi


# Done installing OS package manager (brew) and python package manager (miniconda)
######################################################################


export ANDROID_HOME=$HOME/android-sdk

export ANDROID_DOWNLOAD_DIR="$HOME/android-sdk-dl"

export SDK_VERSION=26
export ANDROID_SDK_HOME="$HOME/android-sdk"
export PATH=${ANDROID_SDK_HOME}:${PATH}
export NDK_VERSION=r16b
export ANDROID_NDK_HOME=$HOME/android-ndk-$NDK_VERSION
# this is redundant (seems to already be set)
export PATH=${ANDROID_NDK_HOME}:${PATH}
export ANDROID_NDK_ZIP="$ANDROID_DOWNLOAD_DIR/android-ndk-$NDK_VERSION.zip"

# mkdir -p $HOME/.android
# touch $HOME/.android/repositories.cfg


##############################################
# Download Android SDK Tools if not already cached

if test ! -e "$ANDROID_SDK_HOME/tools/bin/sdkmanager" ; then
    mkdir -p $ANDROID_DOWNLOAD_DIR
    curl https://dl.google.com/android/repository/sdk-tools-$HOST_OS-3859397.zip > $ANDROID_DOWNLOAD_DIR/sdk-tools.zip
else
    echo "Android SDK zip file found so skipping download"
fi

if test ! -e "$ANDROID_SDK_HOME/tools/bin/sdkmanager" ; then
    echo "unzip -qq -u $ANDROID_DOWNLOAD_DIR/sdk-tools.zip -d $ANDROID_SDK_HOME"
    unzip -qq -u $ANDROID_DOWNLOAD_DIR/sdk-tools.zip -d "$ANDROID_SDK_HOME"
    mkdir -p "$ANDROID_SDK_HOME/.android"
    touch "$ANDROID_SDK_HOME/.android/repositories.cfg"
else
    echo "Android SDKManager found at $ANDROID_SDK_HOME/tools/bin/sdkmanager so skipping unzip"
fi

echo "ls -al $ANDROID_SDK_HOME"
ls -al "$ANDROID_SDK_HOME"


# this is all redundant
echo "Adding $ANDROID_SDK_HOME to $PATH"
export PATH="${ANDROID_SDK_HOME}:${PATH}"


# Download Android SDK Tools if not already cached
##############################################


##############################################
# Install or update Android SDK components 
# (will not do anything if already up to date thanks to the cache mechanism)

# - mkdir -p touch $ANDROID_SDK_HOME/.android
# - touch $ANDROID_SDK_HOME/.android/repositories.cfg

echo y | $ANDROID_SDK_HOME/tools/bin/sdkmanager 'tools' > sdkmanager.tools.stdout.log
echo y | $ANDROID_SDK_HOME/tools/bin/sdkmanager 'platform-tools' > sdkmanager.platform.stdout.log
echo y | $ANDROID_SDK_HOME/tools/bin/sdkmanager 'build-tools;24.0.2' > sdkmanager.24.02.stdout.log
echo y | $ANDROID_SDK_HOME/tools/bin/sdkmanager 'build-tools;26.0.2' > sdkmanager.26.02.stdout.log
echo y | $ANDROID_SDK_HOME/tools/bin/sdkmanager 'build-tools;27.0.2' > sdkmanager.27.02.stdout.log
echo y | $ANDROID_SDK_HOME/tools/bin/sdkmanager 'platforms;android-24' > sdkmanager.24.stdout.log
echo y | $ANDROID_SDK_HOME/tools/bin/sdkmanager 'platforms;android-26' > sdkmanager.26.stdout.log
echo y | $ANDROID_SDK_HOME/tools/bin/sdkmanager 'platforms;android-27' > sdkmanager.27.stdout.log
echo y | $ANDROID_SDK_HOME/tools/bin/sdkmanager 'extras;google;m2repository' > sdkmanager.extras.stdout.log
# tail -n 5 sdkmanager*
rm -f sdkmanager*

echo "ls -al $ANDROID_SDK_HOME"
ls -al $ANDROID_SDK_HOME
echo "$ANDROID_SDK_HOME/tools/bin/sdkmanager --list"
$ANDROID_SDK_HOME/tools/bin/sdkmanager --list

# Install or update Android SDK components 
##############################################


##############################################
# Download Android NDK Tools if not already cached

if test ! -e "$ANDROID_NDK_HOME/ndk-build" ; then
    mkdir -p $ANDROID_DOWNLOAD_DIR
    echo "curl -L https://dl.google.com/android/repository/android-ndk-${NDK_VERSION}-${HOST_OS}-x86_64.zip > $ANDROID_NDK_ZIP"
    curl -L "https://dl.google.com/android/repository/android-ndk-${NDK_VERSION}-$HOST_OS-x86_64.zip" > "$ANDROID_NDK_ZIP"
    ls -al $ANDROID_DOWNLOAD_DIR/
else
    echo "Android NDK zip file found so skipping download"
fi

# Download Android NDK Tools if not already cached
##############################################


##############################################
# Install Android NDK Tools if not already installed

if test ! -e "$ANDROID_NDK_HOME/ndk-build" ; then
    rm -rf $ANDROID_NDK_HOME
    echo "unzip -qq -f $ANDROID_NDK_ZIP -d $HOME"
    unzip -qq -u "$ANDROID_NDK_ZIP" -d "$HOME"
    echo "ls -al $ANDROID_NDK_HOME"
    ls -al $ANDROID_NDK_HOME
else
    echo "Android NDK found at $ANDROID_NDK_HOME/ndk-build so skipping unzip"
fi

ls $ANDROID_NDK_HOME

# mv "$ANDROID_NDK_ZIP" "$ANDROID_NDK_HOME"

# export PATH="${ANDROID_NDK_HOME}:${PATH}"

# install Android NDK Tools
##############################################
