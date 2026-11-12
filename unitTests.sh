#!/bin/bash
cd tests

FAILED=0
for f in Tests*.py
do
   echo $f
   pytest --no-header -W ignore::DeprecationWarning  $f
   if [ $? -ne 0 ]
   then
      FAILED=1
      afplay ~/source/utilityScripts/Sounds/error-when-entering-the-game-menu-132111.mp3
   else
      afplay ~/source/utilityScripts/Sounds/sfx_coin_double1.wav
   fi
done
if [ $FAILED -ne 0 ]
then
   afplay ~/source/utilityScripts/Sounds/error-89612.mov
else
   afplay ~/source/utilityScripts/Sounds/ShortTrumpet.mov
fi

cd ../
linter.sh