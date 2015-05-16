#!/bin/bash


for i in maven/*/*
do
	FILENAME=`basename $i`		
	if [ -d $i ] ;
	then
		echo "Compressing ... $FILENAME ($i)"
		tar cf /Volumes/Maven/$FILENAME.tar $i/*
	fi	
done