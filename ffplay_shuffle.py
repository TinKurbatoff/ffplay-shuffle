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
        print('Skipped {} tracks...')
else:
    last_used_idx = 0 # if not — start from the begining

# play music from current dir
dirpath = path.dirname(path.realpath(__file__))

### Playing from the last position
for current_index in range(last_used_idx,len(music_list)):
    with open(curr_pos_file, 'w') as f:
        # save current index
        f.write(f'{current_index}')
    # use ffplay with suppressed stats and limiting window to 450x250
    command_line = ['ffplay','-autoexit', '-x','450', '-y', '250','-loglevel', 'error','-stats']
    music_file = f'{dirpath}/{music_list[current_index]}' # add path to filename
    command_line.append(music_file)
    print(f"{current_index}. {music_list[current_index]}") # Show what track is playing
    process = subprocess.Popen(command_line,
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    # FOR DEBUG PURPOSES: stdout, stderr = process.communicate()
    # Delay before the next track and allow to break sequence (index saved!)
    with Progress(transient=True) as progress:
        # beautiful progress bar
        task1 = progress.add_task(f"[green]next in {delay} sec...", total=100)
        while not progress.finished:
            progress.update(task1, advance=1)
            sleep(delay/100)   
    # break
print('Bye!')
