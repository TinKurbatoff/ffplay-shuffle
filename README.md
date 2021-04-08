# ffplay-shuffle

A command-line tool (a wrapper) was written with Python (ver.3) to play all music from the current folder with the ffplay tool preserving order between sessions.

This is a simple Python script that iterates through the mp3 files in the current directory and plays them in a shuffled order.

Advantages:
* it shuffles once and then plays tracks from the list one-by-one until all files are played
* it remembers shuffled list between runs, so every composition will be played once even after forced exit or reboot
* it remembers the last composition played when it was interrupted and starts with the same track next time
* limited output: track number / length mm:ss / track name
* delays between tracks 5 sec
* allows to break playing by pressing Ctrl-C

Requirements:
* Python installed
* ffplay installed (part of ffmpeg package)
* mp3info installed (not mandatory)

Tested on:
Mac OS Catalina
