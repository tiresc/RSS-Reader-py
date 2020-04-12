#
# RSS Reader
# Take url input
# List all titles
# give choice of which
#
#
import urllib.request
import sys
import requests
import feedparser
import wget

def main():
	website = ' '
	default = 'https://lexfridman.com/category/ai/feed/'
	site = input('RSS feed: ')
	
	if site == '':
		site = default

	# Gets Byte size of website
	response = requests.get(site)
	site_length = len(response.content)

	# Puts content of site in 'website' for further parsing
	with urllib.request.urlopen(site) as f:
		website = f.read(site_length).decode('utf-8')
	print( site_length )
	
	feed = feedparser.parse( site )

	for x in range(0,len(feed.entries)):
		print(feed.entries[x].title)
		print(feed.entries[x].link)
	print( website )
	
if __name__ == '__main__':
	main()
	