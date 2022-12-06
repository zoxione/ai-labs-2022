set loopcount=10
set x=0
:loop
set /a x2=x+100
start /b python ./parse.py --input "prefetch_cars_20221206122926365004.csv" --start %x% --end %x2%
set /a loopcount=loopcount-1
set /a x=x2+1
if %loopcount%==0 goto exitloop
goto loop
:exitloop
pause
