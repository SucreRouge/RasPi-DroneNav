Program which controls drone with vision system (Raspberry PI + Python + OpenCV + Curses).

<pre>
F:.
|   .gitignore
|   README.md
|   requirements.txt
|
+---src
|   |   shapeDetectNav.py
|   |
|   +---CLInterface
|   |       CLInterface.py
|   |       unicurses.py
|   |       __init__.py
|   |
|   +---piVideoStream
|   |       pivideostream.py
|   |       __init__.py
|   |
|   +---SerialCom
|   |       serialcom.py
|   |       __init__.py
|   |
|   \---shapeDetector
|           shapedetector.py
|           __init__.py
|
\---src_ard
    +---dronePWMControl
    |       dronePWMControl.ino
    |
    \---dronePWMControlv2
            dronePWMControlv2.ino
</pre>

**requirements.txt** - the list of packages required to run this. Can be used with pip to install automatically.

**shapeDetectNav.py** - Program with threaded stream which searches for shapes and analyzes them.

**CLInterface.py** - Class of an object which displays the parameters the stdout being the CLI. Stores settings which are read by shapeDetectNav.py .

**pivideostream.py** - Class of an object which starts the streaming. Contains settings for the video capture.

**shapedetector.py** - Class of an object which identifies the shape.

**dronePWMControl** - First version of generating custom PWM on Arduino Uno.

**dronePWMControlv2** - Working version of Arduino Uno program which reads from
serial port the PWM values and applies them to specific pins.
