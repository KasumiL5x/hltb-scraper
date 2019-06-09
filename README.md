# HowLongToBeat Scraper
> A web spider that crawls HowLongToBeat to extract game and completion time data.

*A big thank you to [HowLongToBeat](https://howlongtobeat.com) for providing such a great service with such rich data.  Sorry about the scraping!*

## Purpose
[HowLongToBeat](https://howlongtobeat.com) (HLTB) is a great website for discovering times that people take to complete games.  While ripe with data, it's unfortunately lacking an API.  This project scrapes all known games (at the time of writing) on the website, extracting the game data as well as all existing completion entries.

This project is part of my venture into the world of data science.

## Structure
The `HLTB_Game_Spider` in `hltb-game.py` scrapes all games available through the website's search functionality.  The `HLTB_Completions_Spider` in `hltb-completions.py` scrapes all user-submitted completion entries for each of the same game (although some have no entries and therefore will be missing).

The `HLTB_Game_Spider` extracts columns (post-cleaning):
* `id` - Game ID from the website.
* `title` - Game name.
* `main_story` - Average completion time of 'Main Story' in hours.
* `main_plus_extras` - Average completion time of 'Main + Extras' in hours.
* `completionist` - Average completion time of 'Completionist' in hours.
* `all_styles` - Average completion time of 'All Styles' in hours.
* `coop` - Average completion time of 'Co-Op' in hours.
* `versus` - Average completion time of 'Vs.' in hours.
* `type` - Type entry to differentiate `DLC/Expansion`, `Mod`, and `ROM Hack` from regular game entries.
* `developers` - Comma-space separated list of all developers of an entry.
* `publishers` - Comma-space separated list of all publishers of an entry.
* `platforms` - Comma-space separated list of all platforms an entry is available on.
* `genres` - Comma-separated list of genres for an entry.
* `release_na` - Release date in North America (if available).
* `release_eu` - Release date in Europe (if available).
* `release_jp` - Release date in Japan (if available).

The `HLTB_Completions_Spider` extracts columns (post-cleaning):
* `id` - Game ID **that can be cross-referenced with the above dataset**.
* `type` - Type of completion entry (`Main Story`, `Main + Extras`, `Completionists`, `Co-Op Multiplayer`, `Speed Run - Any%`, `Speed Run - 100%`).
* `platform` - Platform the particular entry was completed on.
* `time` - Time of entry in hours and minutes (e.g., `2hr 50m`).
