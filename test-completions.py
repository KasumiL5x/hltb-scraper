import os
import scrapy
import pandas as pd

pd.set_option('display.max_colwidth', -1)

def abspath(file):
	return os.path.abspath(os.path.join(os.path.dirname(__file__), file))

# Witcher 3 (many)
with open(abspath('./tests/witcher-completions.html')) as file:
	witcher_sel = scrapy.Selector(text=file.read())

# Peggle (smaller)
with open(abspath('./tests/peggle-completions.html')) as file:
	peggle_sel = scrapy.Selector(text=file.read())

def parse_completions(sel):
	game_df = pd.DataFrame(columns=['id', 'type', 'platform', 'time'])

	# Get all game tables as they are the easiest guaranteed way to get the unqiue lists.
	game_tables = sel.xpath('//table[@class="game_main_table"]')
	for table in game_tables:
		# Traverse back up to get the title of this section (which will be used as a key).
		title = table.xpath('./../../../h3/text()').extract_first().strip()

		if title in ['Main Story', 'Main + Extras', 'Completionists', 'Speed Run - Any%', 'Speed Run - 100%', 'Co-Op Multiplayer']:
			entries = table.xpath('./tbody[@class="spreadsheet"]')
			for entry in entries:
				# platform
				platform = entry.xpath('./tr/td[2]/text()').extract_first()
				platform = platform.strip() if platform != None else 'NA' # if it's valid, strip, otherwise, swap out for NA

				# time
				time = entry.xpath('./tr/td[3]/text()').extract_first()
				if None == time:
					print('Skipping completion without time.')
					continue # if there's no time then there's no point in keeping it
				time = time.strip() # now that it's definitely not None

				game_df = game_df.append({'id': 0, 'type': title, 'platform': platform, 'time': time}, ignore_index=True)
			#end
		else:
			print('Skipping unknown table:', title)
	
	game_df.to_csv(abspath('./completions/completions-test.csv'), index=None)
	# print(game_df.info())
	# print(game_df.platform.value_counts())
	# print(game_df.time.value_counts())
#end

# parse_completions(witcher_sel)
parse_completions(peggle_sel)