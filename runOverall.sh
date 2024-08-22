#!/bin/bash

save_path=$1

# Read filenames from filenames.txt
file1=$(sed -n '1p' $save_path/filenames.txt)
file2=$(sed -n '2p' $save_path/filenames.txt)

# Call the Python script to compare the images
python3 code/hsv.py $save_path/$file1 $save_path/$file2 > $save_path/HSVresult.txt
python3 code/ssim.py ../$save_path/$file1 ../$save_path/$file2 > $save_path/SSIMresult.txt
python3 code/cnn.py $save_path/$file1 $save_path/$file2 > $save_path/CNNresult.txt
python3 code/yolo.py $save_path/$file1 $save_path/$file2 $save_path
