export PYTHONPATH=/Users/thorh/Develop/DarkFactor/adventofcode/Libs

for i in {2022..2025}
do
   cd $i
   echo "Running $i"
   source run_all.sh
   cd ..
done
