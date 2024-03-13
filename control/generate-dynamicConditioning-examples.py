import os
import pandas as pd
import numpy as np

# change directory to necessary source directory

cwd = os.getcwd().split('/')
cwd.remove('control')
cwd.append('midi-emotion')
cwd.append('dev_src')
newdir = '/'.join(cwd)

os.chdir(newdir)

# generate command
gen_len = 3072
max_input_len = 512
batch_size = 1
max_condition = 0.8
temps = [1.5, 1.7]

# currently using max condition to generate all change conditions
# need to modify generate file to create custom conditions

os.system(f"python dynamic-generate.py --model_dir continuous_concat --conditioning continuous_concat --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len} --smooth_change --max_condition {max_condition} --temp {temps[0]} {temps[1]}")