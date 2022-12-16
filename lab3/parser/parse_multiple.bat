@echo off
set loopcount=10
set x=60000
:loop
set /a x2=x+300
start /b python ./parse.py --input "./prefetch_cars/prefetch_cars.csv" --start %x% --end %x2%
set /a loopcount=loopcount-1
set /a x=x2
if %loopcount%==0 goto exitloop
goto loop
:exitloop
pause
