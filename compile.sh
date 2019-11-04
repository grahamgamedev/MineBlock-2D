#! /bin/bash
echo run
python3 MineBlock\ 2D.py

pyinstaller --onefile --windowed MineBlock\ 2D.py

echo run
cd dist
./MineBlock\ 2D

echo copying
mkdir MineBlock\ 2D\ V$1
mkdir MineBlock\ 2D\ V$1/Screenshots
mkdir MineBlock\ 2D\ V$1/Worlds

cp Arial\ Black.ttf MineBlock\ 2D\ V$1/
cp Default_skin.png MineBlock\ 2D\ V$1/
cp MineBlock\ 2D MineBlock\ 2D\ V$1/
cp options.txt MineBlock\ 2D\ V$1/
cp Readme.html MineBlock\ 2D\ V$1/
cp LICENSE MineBlock\ 2D\ V$1/
cp -R Texture\ Packs/ MineBlock\ 2D\ V$1/

echo compressing
file-roller -d MineBlock\ 2D\ V$1/
echo done


