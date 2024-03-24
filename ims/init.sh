#!/bin/sh

DIRECTORY=pi
DIR_COMPRESS=compressed
DIR_DUP=duplicate
if [ -d "$DIRECTORY" ]; then
    echo "$DIRECTORY existing......"
else
    echo "creating directory $DIRECTORY......"
    mkdir $DIRECTORY
fi

if [ -d "$DIR_COMPRESS" ]; then
    echo "$DIR_COMPRESS existing......"
else
    echo "creating directory $DIR_COMPRESS......"
    mkdir $DIR_COMPRESS
fi

if [ -d "$DIR_DUP" ]; then
    echo "$DIR_DUP existing......"
else
    echo "creating directory $DIR_DUP......"
    mkdir $DIR_DUP
fi

cp -f AIModel/color_svm_9_3.sav ./

nohup python3 ImageServer.py &

echo "init done......"