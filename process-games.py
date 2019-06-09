import os
import pandas as pd

def abspath(file):
	return os.path.abspath(os.path.join(os.path.dirname(__file__), file))

df = pd.read_csv(abspath('./all-games.csv'))

# Reformat the column names.
df.rename(columns={
	'Main Story': 'main_story',
	'Main + Extras': 'main_plus_extras',
	'Completionist': 'completionist',
	'All Styles': 'all_styles',
	'Co-Op': 'coop',
	'Vs.': 'versus',
	'Type': 'type',
	'Developers': 'developers',
	'Publishers': 'publishers',
	'Playable On': 'platforms',
	'Genres': 'genres',
	'NA': 'release_na',
	'EU': 'release_eu',
	'JP': 'release_jp'
}, inplace=True)

# I'm not overwriting the original just in case - it takes a long time to scrape!
df.to_csv(abspath('./all-games-processed.csv'), index=None)