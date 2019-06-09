import os
import pandas as pd

def abspath(file):
	return os.path.abspath(os.path.join(os.path.dirname(__file__), file))

games_df = pd.read_csv(abspath('./all-games-processed.csv'))
compl_df = pd.read_csv(abspath('./all-completions.csv'))

game_ids = games_df.id.values
compl_ids = compl_df.id.values

missing_ids = []
for id in game_ids:
	if not(id in compl_ids):
		missing_ids.append(id)

# NOTE: It is *expected* that many ids are missing as not all have times submitted.

print('Total missing IDs:', len(missing_ids))
for id in missing_ids:
	print(id)