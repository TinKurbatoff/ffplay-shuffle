import subprocess
from os import walk
from os import path
from time import sleep

from rich.progress import Progress

import random
import pickle

music_list_file = 'music_list.pickle' # list with music
curr_pos_file = 'current_play_idx.pickle'
delay = 5 # delay between tracks in seconds

### Read the list of music tracks or create one
if path.isfile(music_list_file): 
    with open(music_list_file, 'rb') as f:
        music_list = pickle.load(f)
else:
    ## ..or create a new shuffled list 
    mypath = './'
    _, _, filenames = next(walk(mypath))
    random.shuffle(filenames)
    music_list=[]
    for i in filenames:
        if i.endswith("mp3"):
            # pick only mp3
            music_list.append(i)
    # remember the new list        
    with open(music_list_file, 'wb') as f:
        pickle.dump(music_list, f)

## Read last used index in file
if path.isfile(curr_pos_file):  
    with open(curr_pos_file, 'r') as f:
        last_used_idx = int(f.read().strip())
        print(f'Skipped {last_used_idx} tracks...')
else:
    last_used_idx = 0 # if not — start from 0 — the begining

# play music from current dir
dirpath = path.dirname(path.realpath(__file__))

### Playing from the last position
for current_index in range(last_used_idx,len(music_list)):
    try:
        with open(curr_pos_file, 'w') as f:
            # save current index
            f.write(f'{current_index}')
        # use ffplay with suppressed stats and limiting window to 450x250
        # ffplay OPTIONS available: https://ffmpeg.org/ffplay.html#Options
        command_line = ['ffplay','-autoexit', '-x','450', '-y', '250','-loglevel', 'error','-stats']
        music_file = f'{dirpath}/{music_list[current_index]}' # add path to filename
        command_line.append(music_file)
        # Derive length of track
        ## TO DO: use ffmpeg
        ## $ ffmpeg -i foo.mp3 2>&1 | grep Duration
        ##  Duration: 01:02:20.20, start: 0.000000, bitrate: 128 kb/s
        ##
        process = subprocess.Popen(['mp3info', '-p', '"%S"', music_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            ## Something wrong with mp3info
            len_sec = float('inf')
        else:
            len_sec = int("".join(filter(str.isdigit, stdout.decode())))

        print(f"{current_index+1}. /{len_sec//60}:{len_sec%60}/ {music_list[current_index]}") # Show what track is playing
        ## Finaly — play the music with ffplay!!
        process = subprocess.Popen(command_line,
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
        # This string is required to wait to end of the track: 
        stdout, stderr = process.communicate()
        ## TO_DO: read info from stdout and make a progress bar: 
        ## https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python
        # Delay before the next track and allow to break sequence (index saved!)
        with Progress(transient=True) as progress:
            # beautiful progress bar
            task1 = progress.add_task(f"[green]next in {delay} sec...", total=100)
            while not progress.finished:
                progress.update(task1, advance=1)
                sleep(delay/100)   
    except KeyboardInterrupt as e:
        print(f'\nKeyboard interrupt  ...exiting')
        break;
    # break
print('Bye!')
