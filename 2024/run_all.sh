export PYTHONPATH=/Users/thorh/Develop/DarkFactor/adventofcode/Libs

for i in {1..3}
do
   python3 "$i/Thor/solution.py" "PATH=$i/Thor" "COMPACT"
done
