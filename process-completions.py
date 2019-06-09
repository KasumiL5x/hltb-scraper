import os
import glob
import pandas as pd

def abspath(file):
	return os.path.abspath(os.path.join(os.path.dirname(__file__), file))

input_files = glob.glob(abspath('./completions/*.csv'))
merged_df = pd.concat([pd.read_csv(f) for f in input_files])
merged_df.index = pd.RangeIndex(start=0, stop=len(merged_df))

merged_df.to_csv(abspath('./all-completions.csv'), index=None)