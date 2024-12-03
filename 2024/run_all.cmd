@echo off
set PYTHONPATH=/Users/thorh/Develop/DarkFactor/adventofcode/Libs

set var=01 02 03

for %%i in (%var%) do  (
   python3 "%%i/Thor/solution.py" "PATH=%%i/Thor" "COMPACT"
)
