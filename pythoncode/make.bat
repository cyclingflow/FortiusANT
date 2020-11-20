REM "c:\Program Files\python38\python.exe" -m pip install --upgrade pyinstaller
del dist\FortiusANT.exe
REM "c:\Program Files\python38\Scripts\pyinstaller" --clean MakeFortiusANT.spec
pyinstaller --clean MakeFortiusANT.spec
move dist\FortiusANT.exe ..\WindowsExecutable
copy /Y ..\WindowsExecutable\FortiusANT.exe E:\VirtualTraining\Tools\FortiusAnt\FortiusANT.exe
pause

