# photograph-tools
My photographing tools

## Installing requirements
run ./install.sh

## Installing training data (optional)
run those line of codes
sudo apt-get install wget
wget http://dlib.net/files/data/ibug_300W_large_face_landmark_dataset.tar.gz
tar -xvf ibug_300W_large_face_landmark_dataset.tar.gz

## features
- filter the photos where the people has the eyes open
- filter the photos where the people smiles
- filter the photos where the people are in frame
- filter the photos where the people are in focus
- filter the photos where the people look at the camera
- filter the photos where the photo does not have to much high lights and low lights
- filter by people (solo / group)