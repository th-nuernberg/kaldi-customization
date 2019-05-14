#!/bin/bash

echo "###########################################################"
echo "Starting preparation scripts to prepare and build the project structure for Kaldi execution!"
echo "Prepare project structure!"
bash prepare_developer_structure.sh
echo "Finished preparation of project structure!"
echo "###########################################################"
echo ""
echo ""
echo "###########################################################"
echo "Prepare data files for Kaldi execution!"
bash prepare_developer_data_files.sh
echo "Finished preparation of data files!"
echo "###########################################################"
echo ""
echo "Finished preparation!"
echo "###########################################################"