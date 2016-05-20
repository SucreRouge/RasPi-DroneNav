Program which controls drone with vision system (Raspberry PI + Python + OpenCV + Curses).

<pre>
C:.
|   .gitignore
|   README.md
|   requirements.txt
|   
\---src
    |   shapeDetectNav.py
    |   
    +---curses
    |       CLInterface.py
    |       pdcurses.dll
    |       unicurses.py
    |       
    \---shapeDetector
            shapedetector.py
            __init__.py
</pre>
          
**requirements.txt** - the list of packages required to run this. Can be used with pip to install automatically.

**shapeDetectNav.py** - Program with threaded stream which searches for shapes and analyzes them.

**shapedetector.py** - Class of an object which identifies the shape.

**CLInterface.py** - Class of an object which displays the parameters the stdout being the CLI.
