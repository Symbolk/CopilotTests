import ast
import os
from os.path import join as pjoin
import sys
import re
import time

category='plib_runnable'
files = os.listdir('./{}'.format(category))
files = [f for f in files if f.endswith(".py")]
def get_lineno(file_index):
    with open('./urls.txt','r') as f:
        files = f.read()
        files = files.split('\n')
        files = [file for file in files if len(file) > 0]
        request = [file for file in files if file.startswith(category+'/'+str(file_index))][0]
        file_paths,url= request.split(' ')
        lineno = url.split('#')[-1]
    return int(lineno[1:])
for f in files:
    with open(pjoin('./{}/{}'.format(category,f)), 'r') as fp:
        lineno = get_lineno(f.split('.')[0].split('_')[-1])
        lines = fp.readlines()
        signature = lines[lineno-1].split('(')[0]
        signature = signature.split('def ')[-1]
        print(signature)
        test = '\n\n\ndef test_{}():\n    \"\"\"Check the correctness of {}\n    \"\"\"\n    assert '.format(signature,signature)
    with open(pjoin('./{}/{}'.format(category,f)), 'a') as fp:
        fp.write(test)
