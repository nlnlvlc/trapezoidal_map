# Programming Assignment Three: Trapezoidal Map
This project builds a Trapezoidal map using line segments. The map can then be used to search for the planar location
of a user given point

## Language & Libraries

Both programs were built using Python3. This program makes use of the Shapely library in order to calculate
the intersecting point of segments. If needed, it can be installed by using the following: 

```commandline
pip install shapely
```

The program also uses pandas.

## Before Running

All files should be stored in the same directory. Only one file will be run to build the Trapezoidal Map.

## Run the Trapezoidal Map Program

The program can be run via the commandline:
```commandline 
python3 trapezoidalMap.py
```

When prompted, the program ask the user to submit a point, which is made up of an x and y, separated by a space.
```
x y
```

Once the program has finished execution, it will produce a csv file containing an agency matrix of Map. It will also
print to console the path the user input point would take to find which trapezoid the point is located in within the 
Map.

