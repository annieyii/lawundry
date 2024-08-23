#!/bin/bash
save_path=$1

# Read filenames 
file1=$(sed -n '1p' $save_path/partial-imagesChecked.txt)
file2=$(sed -n '2p' $save_path/partial-imagesChecked.txt)

python3 code/hsv.py static/$file1 static/$file2 > $save_path/PartialHSVresult.txt
python3 code/ssim.py ../static/$file1 ../static/$file2 > $save_path/PartialSSIMresult.txt
python3 code/cnn.py static/$file1 static/$file2 > $save_path/PartialCNNresult.txt