#!/bin/sh
echo 'install requirements'
sudo apt-get install -y
sudo apt-get install build-essential cmake -y
sudo apt-get install libgtk-3-dev -y
sudo apt-get install libboost-all-dev -y
pip install numpy scipy scikit-image opencv-python imutils
pip install dlib