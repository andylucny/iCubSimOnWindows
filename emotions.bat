@echo off

rem  neu (neutral)
rem  hap (happy)
rem  sad (sad)
rem  sur (surprised)
rem  ang (angry)
rem  evi (evil)
rem  shy (shy)
rem  cun (cunning)

echo neutral
python noyarp.py /emotion/in "set all neu"
pause

echo happy
python noyarp.py /emotion/in "set all hap"
pause

echo sad
python noyarp.py /emotion/in "set all sad"
pause

echo surprised
python noyarp.py /emotion/in "set all sur"
pause

echo angry
python noyarp.py /emotion/in "set all ang"
pause

echo evil
python noyarp.py /emotion/in "set all evi"
pause

echo shy
python noyarp.py /emotion/in "set all shy"
pause

echo cunning
python noyarp.py /emotion/in "set all cun"
pause
