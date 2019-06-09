"""
HowLongToBeat Spider
Daniel Greeen / KasumiL5x

Purpose:
  This spider crawls HowLongToBeat (HLTB) and retrieves game information for each known game on the website.
  This is my first web scraping project! :)

Notes:
  HLTB's url doesn't change unless accessing a game directly, so scraping a search page is hard, as it's dynamically inserted.
  Their game page is 'game.php?id=ID', so the obvious method is to find the maximum ID.  However, I have found IDs that are
  vastly beyond their number of games, and found plenty of empty IDs that should be valid, so this isn't an option.
  However, I noticed that main page JS queries '/search_results.php?page=ID' which yields what would be injected in.
  We can find the page limit (1996 a the time of writing) and generate the appropriate links to parse, which in turn should
  give us every game on the website.

  I will be exporting two separate scrapes:
    On the game's Overview tab, I will pull game information and *overall* summary statistics.
    On the game's Completions tab, I will pull all entries for each game by hand.

  search_results.php:
    div.search_list_image > a
      Returns all of the individual game tiles in the search.
    ./@href
      Chained to the above, extracts the partial game link as 'game.php?id=ID'.

  game.php
    Overview
      div.profile_header
        Game title.
      li.short.time_100
        Array of game times. Nested <h5> is the name, and <div> is the value. Value may be '--' for missing.
        Expected names are 'Main Story', 'Main + Extras', 'Completionist', 'All Styles'.
      div.profile_info
        Array of game information. Its text is the actual value. Nested <strong> is the name of the data.
        'Type' is a single entry (for DLC etc.).
        'Developer' is a single entry. 'Developers' is a comma-space separated list.
        'Publisher' is a single entry. 'Publishers' is a comma-space separated list.
        'Playable On' is a comma-space separated list.
        'Genre' is a single entry. 'Genres' is a comma-space separated list.
        'NA' is a single entry (North America release date).
        'EU' is a single entry (EU release date).
        'JP' is a single entry (Japan release date).
"""

import os
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

def abspath(file):
	return os.path.abspath(os.path.join(os.path.dirname(__file__), file))

class HLTB_Game_Spider(scrapy.Spider):
	name = 'hltb_game_spider'

	def start_requests(self):
		min_page = 1
		max_page = 1996
		page_range = range(min_page, max_page+1)
		for page_id in page_range:
			page_url = 'https://howlongtobeat.com/search_results.php?page=%s' % page_id
			# print("Parsing search page:", page_id)
			yield scrapy.Request(url=page_url, callback=self.parse_page)
	#end

	def parse_page(self, response):
		games = response.css('div.search_list_image > a')
		for game in games:
			# Extract ID (check split length in case an ID is missing).
			raw_id = game.xpath('./@href').extract_first().split('=')
			game_id = raw_id[1] if (len(raw_id) == 2) else 'INVALID'

			# Safety check.
			if('' == game_id):
				print('Error parsing game on page (%s)!' % response.url)
				continue
			
			# Generate game link.
			game_link = 'https://howlongtobeat.com/game.php?id=%s' % game_id
			# print('\tParsing game w/ id:', game_id)

			# Trigger the game page parsing!
			yield response.follow(url=game_link, callback=self.parse_game)
		#end
	#end

	def parse_game(self, response):
		game_df = pd.DataFrame()

		# Game ID.
		game_df['id'] = [response.url.split('=')[1]]

		# Title.
		game_df['title'] = [response.css('div.profile_header::text').extract_first().strip()] # preceded by \n and followed by space, so strip

		# Game times
		all_times = response.css('div.game_times > li')
		time_names = all_times.xpath('./h5/text()').extract()
		time_times = all_times.xpath('./div/text()').extract()
		# Strip all spaces, replace '--' with 'NA', replace '1/2' with '.5'.
		time_times = [s.strip().replace('--', '').replace('½', '.5') for s in time_times]
		# There are two time formats: 'Mins' and 'Hours'.
		# If 'Mins', strip and convert into a fraction of hours, but convert back to string for consistency.
		# If 'Hours', just strip.
		time_times = [str(float(s.split(' ')[0]) / 60.0) if 'Mins' in s else s.split(' ')[0] for s in time_times]
		# Loop through as a dict here as not all game pages have all entries, and I don't want literal missing values.
		names_times = dict(zip(time_names, time_times))
		for key in ['Main Story', 'Main + Extras', 'Completionist', 'All Styles', 'Co-Op', 'Vs.']:
			game_df[key] = names_times[key] if key in names_times else ''

		# Profile (game information).
		profile = {
			'Type': '',
			'Developers': '', # includes both 'Developer' and 'Developers'
			'Publishers': '', # includes both 'Publisher' and 'Publishers'
			'Playable On': '',
			'Genres': '', # includes both 'Genre' and 'Genres'
			'NA': '',
			'EU': '',
			'JP': ''
		}
		profile_info = response.css('div.profile_info')
		for info in profile_info:
			info_title = info.xpath('./strong/text()').extract_first().replace(':', '').strip()
			info_text = info.xpath('./text()').extract()[1].strip() # first element is always '\n'

			# Handle special cases, and otherwise just shove it in using the title as the key.
			if ('Developer' == info_title) or ('Developers' == info_title):
				profile['Developers'] = info_text
			elif ('Publisher' == info_title) or ('Publishers' == info_title):
				profile['Publishers'] = info_text
			elif ('Genre' == info_title) or ('Genres' == info_title):
				profile['Genres'] = info_text
			elif info_title not in ['Updated']: # ignore list
				profile[info_title] = info_text

		for key, value in profile.items():
			game_df[key] = value

		# Add game DF to all games DF.
		global all_games_df
		all_games_df = pd.concat([all_games_df, game_df], sort=False)
	#end
#end

all_games_df = pd.DataFrame()

process = CrawlerProcess()
process.crawl(HLTB_Game_Spider)
process.start()

# sort by title and reset index
all_games_df.sort_values('title', inplace=True)
all_games_df.index = pd.RangeIndex(start=0, stop=len(all_games_df))

# write out csv
all_games_df.to_csv(abspath('./all-games.csv'), index=None)
# print(all_games_df)