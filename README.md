# PayloadSoftware

## Directories:
In general, each directory represents a software sub-system with a single entry-point.

### air_quality
Python source code for the AIR subsystem. Interfaces with 'lcd' and 'transmission'

### target_detection
Python source code for the TD subsystem. Interfaces with 'lcd' and 'transmission'

### transmission
Python source code for the module that communicates with the ground control station. Interfaces with 'air_quality' and 'target_detection'.

### lcd
Python source code for the LCD monitor on the Enviro+. Interfaces with 'air_quality' and 'target_detection'.

### display_mode
Script used by the payload operator to switch the graphics on the LCD display. Current mode is stored in a file within this directory. 'setmode.sh' should be added to the path variable and made executable, allowing 'setmode' to be entered into the shell to run the script.

### lib
Python library source code.

### test
Unit and integration tests for the system.

### docs
Manual for the command-line options of each Python script.





## Dependencies (APT):
### Python packages
pip3

Requirements.txt contains the list of Pip packages that need to be installed. (sudo pip install -r requirements.txt)
### OpenCV
libopencv-dev
python3-opencv
### Pimoroni Enviroplus
python-numpy python-pil python-setuptools
python3-pip python3-cffi python3-rpi.gpio
libortaudio2
### Redis
redis-server

## Additional installation steps:
Place Roboto-Medium.ttf in ~/.local/share/fonts