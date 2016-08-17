Program which controls drone with vision system (Raspberry PI + Python + OpenCV + Curses).

<pre>
F:.
|   .gitignore
|   README.md
|   requirements.txt
|
+---src
|   |   config.ini
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
|   +---pwmGenerator
|   |       pwmgenerator.py
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
+---src_additional
|   |   controlsTest.py
|   |   controlsTest_pure.py
|   |
|   \---SerialCom
|           serialcom.py
|           serialcom.pyc
|           __init__.py
|           __init__.pyc
|
\---src_ard
    +---dronePWMControl
    |       dronePWMControl.ino
    |
    +---dronePWMControlv2
    |       dronePWMControlv2.ino
    |
    +---dronePWMControlv3
    |       dronePWMControlv3.ino
    |
    +---dronePWMControlv4
    |       dronePWMControlv4.ino
    |
    +---dronePWMControlv5
    |       dronePWMControlv4.ino
    |
    \---dronePWMControlv6
            dronePWMControlv5.inoo
</pre>

### *Main folder*

**requirements.txt** - the list of packages required to run this. Can be used with pip to install automatically.

### *src folder - contains main navigation program*

**shapeDetectNav.py** - Program with threaded stream which searches for shapes
and analyzes them.

**CLInterface.py** - Class of an object which displays the parameters the
stdout being the CLI. Stores settings which are read by shapeDetectNav.py .

**pivideostream.py** - Class of an object which starts the streaming. Contains
settings for the video capture.

**shapedetector.py** - Class of an object which identifies the shape.

### *src_additional folder - contains additional programs for testing*

**controlsTest.py** - Allows to test and configure control through LibrePilot
by using computer keyboard.

**controlsTest_pure.py** - Allows to test and configure control through
LibrePilot by using computer keyboard. Only direct keyboard control but with
throttling. Better written than the previous one.

### *src_ard folder - programs for AVR microcontroller which generates PWMs
for CC3D*

**dronePWMControl** - First version of generating custom PWM on Arduino Uno.

**dronePWMControlv2** - Working version of Arduino Uno program which reads from
serial port the PWM values and applies them to specific pins.

**dronePWMControlv3** - Final version of my custom PWM generation. Reads data
from UART and generates PWMs based on this data. Not consistent enough for
Drone.

**dronePWMControlv4** - Same as above but with c strings... doesn't work
properly.

**dronePWMControlv5** - Uses Arduino's servo library which
generates signals with almost perfect 50Hz. With this program LibrePilot
properly configures control.

**dronePWMControlv6** - THE program. Uses Arduino's servo library and uses fill
of 1.5ms, 2ms, 1ms.
