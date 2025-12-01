export PYTHONPATH=/Users/thorh/Develop/DarkFactor/adventofcode/Libs

for i in {1..25}
do
   if [ $i -lt 10 ]
   then
      python3 "0$i/Thor/solution.py" "PATH=0$i/Thor" "COMPACT"
   else
      python3 "$i/Thor/solution.py" "PATH=$i/Thor" "COMPACT"
   fi
done
