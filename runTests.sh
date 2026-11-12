cd tests
for f in Tests*.py
do
   echo $f
   python $f
done
