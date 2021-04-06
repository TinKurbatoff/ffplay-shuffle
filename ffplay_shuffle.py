import subprocess
from os import walk
from os import path
from time import sleep

from rich.progress import Progress

import random
import pickle

music_list_file = 'music_list.pickle' # list with music
curr_pos_file = 'current_play_idx.pickle'
delay = 5 # delay between tracks

### Read list of the music o create one
if path.isfile(music_list_file): 
    with open(music_list_file, 'rb') as f:
        music_list = pickle.load(f)
else:
    ## create a shuffled list 
    mypath = './'
    _, _, filenames = next(walk(mypath))
    random.shuffle(filenames)
    music_list=[]
    for i in filenames:
        if i.endswith("mp3"):
            music_list.append(i)
            # print(i)
    with open(music_list_file, 'wb') as f:
        pickle.dump(music_list, f)

## Read last used index in file
if path.isfile(curr_pos_file):  
    with open(curr_pos_file, 'r') as f:
        last_used_idx = int(f.read().strip())
        print('Skipped {} tracks...')
else:
    last_used_idx = 0 # if not — start from begining

# play music from current dir
dirpath = path.dirname(path.realpath(__file__))

### Playing from the last position
for current_index in range(last_used_idx,len(music_list)):
    with open(curr_pos_file, 'w') as f:
        f.write(f'{current_index}')
    command_line = ['ffplay','-autoexit', '-x','450', '-y', '250','-loglevel', 'error','-stats']
    music_file = f'{dirpath}/{music_list[current_index]}'
    command_line.append(music_file)
    print(f"{current_index}. {music_list[current_index]}")
    # print(f"Executing command: {command_line}")
    # with open('playing.out', 'w') as f:
    #     process = subprocess.Popen(command_line, stdout=f)
    process = subprocess.Popen(command_line,
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    with Progress(transient=True) as progress:
        task1 = progress.add_task(f"[green]next in {delay} sec...", total=1000)
        while not progress.finished:
            progress.update(task1, advance=10)
            sleep(delay/100)   
    # break
print('Bye!')
