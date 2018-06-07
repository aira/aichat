#!/bin/bash
# $1 is the script name
# $2 is the first argument in post_install_args
source /etc/cfncluster/cfnconfig

case ${cfn_node_type} in
	MasterServer)
		echo "I am the master" >> /home/ubuntu/master.txt
		wget -c https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o $HOME/install_miniconda3.sh
		chmod +x $HOME/install_miniconda3.sh
		cd $HOME
		./install_miniconda.sh -b -p $HOME/miniconda
		export PATH=$HOME/miniconda/bin:$PATH
		echo 'export PATH=$HOME/miniconda/bin:$PATH' >> $HOME/.bash_profile
		git clone https://github.com/aira/aichat.git
		cd aichat
		;;

	ComputeFleet)
		echo "I am a compute node" >> /tmp/compute.txt
		;;
esac