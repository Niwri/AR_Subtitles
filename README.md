# Caption Glasses
The Caption Glasses provide captions displayed on glasses after detecting American Sign Language (ASL). The captions are instant and in real-time, allowing for effective translations into the English language for the glasses wearer.

# Building Process
Caption Glasses began with prototyping hardware and design, starting off by programming a SSD1306 OLED 0.96'' display with an Arduino Nano. The glasses attachment is a 3D printed Solidworks design from a Prusa I3 3D printer and compiled with all key hardware components. On the software side, we loaded computer vision models onto a Raspberry Pi4. Although we were successful in loading a basic model that looks at generic object recognition, we were unable to find an ASL gesture recognition model that was compact enough to fit on the RPi. To circumvent this problem, we used MediaPipe Hand Recognition models which marked out 21 landmarks of the human hand (including wrist, fingertips, knuckles, etc.). We then created a custom Artificial Neural Network that takes the position of these landmarks and determines what letter we are trying to sign. The machine-learning model is trained with thousands of our own data points.

# Built With
arduino, arduino-c, C++, mediapipe, neural-net-modelling, numpy, Python, pytorch, raspberry-pi, Solidworks, spi
