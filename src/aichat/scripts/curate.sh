#!/usr/bin/env bash

OLDPWD="$PWD"

if [ -d "$1" ] ; do
	cd $1
fi

for f in *.ogg ; do
	ffmpeg -i "$f" "${f/%ogg/wav}" ;
done

for f in *.wav ; do
    audio --play "$f" ; 
    read  -n 1 -p "Delete File? [n]": ans ;

    if [ "$ans" == "y"] ; then
        echo "DELETING" ;
        rm -f "$f" ;
        rm -f "${f/%wav/ogg}" ;
    fi
done
cd "$OLDPWD"
