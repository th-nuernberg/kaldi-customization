#!/bin/bash

if [ ! -d converted/ ]; then 
    mkdir converted/ 
fi 
for i in ./*.wav 
do
    sox -S $i -r 16000 -b 16 "converted/$i"; 
done
