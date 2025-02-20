#!/usr/bin/env bash

if [ ! -d "./models/MiniCPM-o-2_6-int4" ]; then
  echo "Downloading MiniCPM-o 2.6 int4"
  git lfs install
  git clone https://www.modelscope.cn/OpenBMB/MiniCPM-o-2_6-int4.git ./models/MiniCPM-o-2_6-int4
  echo "Download complete"
else
  echo "MiniCPM-o-2_6-int4 already exists"
fi