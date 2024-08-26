#!/bin/bash
save_path=$1

# Read filenames 
file1=$(sed -n '1p' $save_path/partial-imagesChecked.txt)
file2=$(sed -n '2p' $save_path/partial-imagesChecked.txt)

# Debugging: Print file paths
echo "File1: static$file1"
echo "File2: static$file2"

if [ ! -f "static$file1" ]; then
    echo "File $file1 does not exist."
    exit 1
fi

if [ ! -f "static$file2" ]; then
    echo "File $file2 does not exist."
    exit 1
fi


python3 code/hsv.py static$file1 static$file2 > $save_path/PartialHSVresult.txt
python3 code/partialSSIM.py static$file1 static$file2 > $save_path/PartialSSIMresult.txt
python3 code/cnn.py static$file1 static$file2 > $save_path/PartialCNNresult.txt