import subprocess
from os import walk

process = subprocess.Popen(['echo', 'More output'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stdout)
# stdout, stderr

# with open('test.txt', 'w') as f:
#     process = subprocess.Popen(['ls', '-l'], stdout=f)

_, _, filenames = next(walk(mypath))

print(filenames)