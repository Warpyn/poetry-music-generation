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

dynamicTestSet = pd.DataFrame(np.array([  
                                [0.8, 0.8, -0.8, -0.8],
                                [-0.8, -0.8, 0.8, 0.8],
                                [0.8, -0.8, -0.8, 0.8],
                                [-0.8, 0.8, 0.8, -0.8],
                                ]),
             columns=['valence', 'arousal', 'valence2', 'arousal2'])

# change directory to inside midi-emotion repo

cwd = os.getcwd().split('/')
cwd.remove('control')
cwd.append('midi-emotion')
cwd.append('dev_src')
newdir = '/'.join(cwd)

os.chdir(newdir)

# pull valence and arousal values from dataframe -> generate
# (for i in range(0, num of rows))
df = dynamicTestSet
num_rows, num_cols = df.shape

gen_len = 2048
max_input_len = 1024
batch_size = 1

# for i in range(num_rows):
#     valence = df.loc[i]['valence']
#     arousal = df.loc[i]['arousal']
    
#     os.system(f"python generate.py --model_dir continuous_concat --conditioning continuous_concat --valence {valence} --arousal {arousal} --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len}")
#     # os.system(f"python dynamic-generate.py --model_dir continuous_concat --conditioning continuous_concat --valence {valence} {valence2} --arousal {arousal} {arousal2} --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len} --smooth_change")

os.system(f"python dynamic-generate.py --model_dir continuous_concat --conditioning continuous_concat --batch_size {batch_size} --gen_len {gen_len} --max_input_len {max_input_len} --smooth_change --max_condition 0.8")