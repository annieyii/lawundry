#!/bin/bash

rm -r HSVresult.txt
rm -r SSIMresult.txt
rm -r YOLOresult1.txt
rm -r YOLOresult2.txt

# Read filenames from filenames.txt
file1=$(sed -n '1p' filenames.txt)
file2=$(sed -n '2p' filenames.txt)

rm -r code/*.jpg
rm -r code/*.png
rm -r code/*.jepg
rm -r code/*.gif


rm -r filenames.txt

# 清空partpic
rm -rf partpic/*