#!/bin/zsh
mkdir $1
mv boss.out $1
mv boss.rst $1
if [ -d postprocessing ]
then
    mv postprocessing $1
fi

