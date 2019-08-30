@echo off
title PyInstaller Compile

pyinstaller --onefile --windowed -i "..\icon.ico" "MineBlock 2D.py"

robocopy ".\Texture Packs" ".\dist\Texture Packs" -MIR
robocopy ".\Worlds" ".\dist\Worlds" -MIR
robocopy .\ .\dist\ options.txt Readme.html "Arial Black.ttf" Default_skin.png

echo Run...
".\Dist\MineBlock 2D.exe"

echo Compile Installer
call "..\..\..\PortableApps\Inno Setup 6\Compil32.exe" Installer.iss