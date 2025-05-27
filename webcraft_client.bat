@echo off
setlocal

:: Get the nickname from custom URI: webcraft://launch?nickname=Player
for /f "tokens=2 delims==" %%A in ("%~1") do set "nickname=%%A"

if "%nickname%"=="" set "nickname=Player"

echo Launching WebCraft for: %nickname%

:: Run the Python client with the nickname
python webcraft_client.py %nickname%

pause
