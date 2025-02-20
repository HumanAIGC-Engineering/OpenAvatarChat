#!/usr/bin/env bash

if [ ! -d "./models/MiniCPM-o-2_6" ]; then
  echo "Downloading MiniCPM-o 2.6"
  git lfs install
  git clone https://www.modelscope.cn/OpenBMB/MiniCPM-o-2_6.git ./models/MiniCPM-o-2_6
  echo "Download complete"
else
  echo "MiniCPM-o-2_6 already exists"
fi