import os
import pandas as pd

# read in csv to dataframe

vad = pd.read_csv('./NRC-VAD-Lexicon.csv')
vad = vad[['valence', 'arousal', 'dominance']]

# change directory to inside midi-emotion repo

cwd = os.getcwd().split('/')
cwd.remove('control')
cwd.append('midi-emotion')
cwd.append('src')
newdir = '/'.join(cwd)

os.chdir(newdir)

# pull valence and arousal values from dataframe -> generate
# (for i in range(0, num of rows))
num_rows, num_cols = vad.shape

valence = vad.loc[0]['valence']
arousal = vad.loc[0]['arousal']

os.system(f"python generate.py --model_dir continuous_concat --conditioning continuous_concat --valence {valence} --arousal {arousal} --batch_size 1 --gen_len 512 --max_input_len 64")