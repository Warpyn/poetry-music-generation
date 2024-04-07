import os
import pandas as pd
import numpy as np

# create dataframe of valence arousal test data


broadTestSet = pd.DataFrame(np.array([  
                                [0.8, 0.8], 
                                [-0.8, 0.8], 
                                [0.8, -0.8], 
                                [-0.8, -0.8],
                                [0, 0],
                                [0.5, 0],
                                [-0.5, 0],
                                [0, -0.5],
                                [0, 0.5]
                                ]),
             columns=['valence', 'arousal'])

originTestSet = pd.DataFrame(np.array([  
                                [0, 0.1],
                                [0.1, 0],
                                [0, 0.001],
                                [0.001, 0]
                                ]),
             columns=['valence', 'arousal'])

arousalTestSet = pd.DataFrame(np.array([  
                                [0.1, 1],
                                [0.1, 0.8],
                                [0.1, 0.6],
                                [0.1, 0.4],
                                [0.1, 0.2],
                                [0.1, -1],
                                [0.1, -0.8],
                                [0.1, -0.6],
                                [0.1, -0.4],
                                [0.1, -0.2],
                                ]),
             columns=['valence', 'arousal'])

valenceTestSet = pd.DataFrame(np.array([  
                                [1, 0.1],
                                [0.8, 0.1],
                                [0.6, 0.1],
                                [0.4, 0.1],
                                [0.2, 0.1],
                                [-1, 0.1],
                                [-0.8, 0.1],
                                [-0.6, 0.1],
                                [-0.4, 0.1],
                                [-0.2, 0.1]
                                ]),
             columns=['valence', 'arousal'])


# change directory to inside midi-emotion repo

cwd = os.getcwd().split('/')
cwd.remove('control')
cwd.append('midi-emotion')
cwd.append('dev_src')
newdir = '/'.join(cwd)

os.chdir(newdir)

# pull valence and arousal values from dataframe -> generate
df = arousalTestSet
num_rows, num_cols = df.shape

gen_len = 2048
max_input_len = 512
batch_size = 1

for i in range(num_rows):
    valence = df.loc[i]['valence']
    arousal = df.loc[i]['arousal']
    
    os.system(f"python generate.py --model_dir continuous_concat --conditioning continuous_concat --valence {valence} --arousal {arousal} --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len}")
