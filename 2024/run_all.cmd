@echo off
set PYTHONPATH=/Users/thorh/Develop/DarkFactor/adventofcode/Libs

set var=01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20

for %%i in (%var%) do  (
   python3 "%%i/Thor/solution.py" "PATH=%%i/Thor" "COMPACT"
)
