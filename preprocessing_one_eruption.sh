#!/bin/sh
cd ./script
echo Run Move_nodata.py
python Move_nodata.py
echo -e \\nRun framerate_transform.py
python framerate_transform.py
echo -e \\nRun interpolation.py
python interpolation.py
echo -e \\nRun graph.py
python graph.py