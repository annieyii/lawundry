#!/bin/bash
save_path=$1

# Read filenames 
file1=$(sed -n '1p' $save_path/filenames.txt)
file2=$(sed -n '2p' $save_path/filenames.txt)

python3 code/hsv.py $save_path/$file1 $save_path/$file2 > $save_path/PartialHSVresult.txt
python3 code/ssim.py ../$save_path/$file1 ../$save_path/$file2 > $save_path/PartialSSIMresult.txt
python3 code/cnn.py $save_path/$file1 $save_path/$file2 > $save_path/PartialCNNresult.txt