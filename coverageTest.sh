cd tests
coverage erase

coverage run Tests_RIS_Filters.py
for f in Tests_*.py
do
   coverage run -a $f
done
coverage report
coverage html
open htmlcov/index.html

