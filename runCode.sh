#!/bin/bash

# Read filenames from filenames.txt
file1=$(sed -n '1p' filenames.txt)
file2=$(sed -n '2p' filenames.txt)

mv uploads/$file1 code/
mv uploads/$file2 code/
# Call the Python script to compare the images
python3 code/hsv_similarity.py $file1 $file2 > HSVresult.txt
python3 code/ssim.py $file1 $file2 > SSIMresult.txt
