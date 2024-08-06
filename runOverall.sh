#!/bin/bash

# Read filenames from filenames.txt
file1=$(sed -n '1p' filenames.txt)
file2=$(sed -n '2p' filenames.txt)

mv uploads/$file1 code/
mv uploads/$file2 code/

# Call the Python script to compare the images
pip3 install -r requirement.txt
python3 code/hsv_similarity.py $file1 $file2 > HSVresult.txt
python3 code/ssim.py $file1 $file2 > SSIMresult.txt
python3 code/yolo.py code/$file1 > YOLOresult1.txt 
python3 code/yolo.py code/$file2 > YOLOresult2.txt
