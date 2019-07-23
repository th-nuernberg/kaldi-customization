#!/bin/bash

if [ $# != 2 ]; then
   echo "Usage: prep_model.sh <graph-dir> <model-dir>"
   exit 1;
fi


function copy_link_target_to {
    target=`readlink $1/$3`
    cp "$1/$target" "$2/$3"
}


copy_link_target_to $1 $2 final.mdl
cp -r $1/graph $2/graph
