import ast
import os
from os.path import join as pjoin
import sys
import re
import time

files = os.listdir('./self_contained')
files = [f for f in files if f.endswith(".py")]
for f in files:
    os.system("mv ./self_contained/%s ./self_contained/%s" % (f, "test_"+f))
