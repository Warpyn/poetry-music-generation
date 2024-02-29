import os
import pandas as pd
import numpy as np

# create dataframe of valence arousal test data

df = pd.DataFrame(np.array([[0.8, 0.8], 
                            [-0.8, 0.8], 
                            [0.8, -0.8], 
                            [-0.8, -0.8],
                            [0, 0],
                            [0.5, 0],
                            [-0.5, 0],
                            [0, -0.5],
                            [0, 0.5]]),
             columns=['valence', 'arousal'])

# change directory to inside midi-emotion repo

cwd = os.getcwd().split('/')
cwd.remove('control')
cwd.append('midi-emotion')
cwd.append('src')
newdir = '/'.join(cwd)

os.chdir(newdir)

# pull valence and arousal values from dataframe -> generate
# (for i in range(0, num of rows))
num_rows, num_cols = df.shape

for i in range(num_rows):
    valence = df.loc[i]['valence']
    arousal = df.loc[i]['arousal']
    
    gen_len = 2048
    max_input_len = 1024
    batch_size = 2

    os.system(f"python generate.py --model_dir continuous_concat --conditioning continuous_concat --valence {valence} --arousal {arousal} --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len}")