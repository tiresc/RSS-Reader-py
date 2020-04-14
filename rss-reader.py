#
# RSS Reader
# Take url input
# List all titles
# give choice of which
#

import urllib.request
import sys
import requests
import feedparser
import wget
import os
import platform 
from pathlib import Path, PureWindowsPath

class SITE():
	def __init__(self):
		self.site_address = ' '
		self.website = ' '
		self.default = 'https://lexfridman.com/category/ai/feed/'
		self.site = input('RSS feed: ')#'https://lexfridman.com/category/ai/feed/'#input('RSS feed: ')
		self.feed = ' '
		self.site_size = 0
		self.response = ' '
		self.file_number = 0
		self.mp3_name = ' '

	def download_site(self):
		with urllib.request.urlopen(self.site) as f:
			self.website = f.read(self.site_size).decode('utf-8')
			print( self.site_size )
	
		self.feed = feedparser.parse( self.site )
	
	def get_site_size(self):
		# Gets Byte size of website
		self.response = requests.get(self.site)
		self.site_size = len(self.response.content)

	def print_info(self):
		for x in range(0,len(self.feed.entries)):
			print(self.feed.entries[x].title)
		#print( self.website )

def create_directories():
	if os.path.isdir('feeds') and os.path.isdir('config'):
		return 0
	else:
		os.system('md config feeds')
		return 1

def get_file_list():
	unix_path = './feeds'
	path_on_windows = '.'
	file_list = []
	rootDir = '.'
	print('')

	for dirName, subdirList, fileList in os.walk(rootDir):
		if(platform.system() == 'Linux' or platform.system() == 'Darwin'):
			print(dirName)
			if(dirName == unix_path):
				for fname in fileList:
					print("\t%s" % fname)
					file_list.append(fname)	
					print(file_list)	
		elif platform.system() == 'Windows':
			#print(dirName)
			if(dirName == path_on_windows):
				for fname in fileList:
					print("\t%s" % fname)
					#file_list.append(fname)
					return subdirList

			
		else:
			print("os not recognized")

def main():
	create_directories()
	sub_directory = get_file_list()
	print(sub_directory)
	unix_path = './feeds/'
	path_on_windows = '.\\feeds\\'
	feed_path = ' '

	new_site = SITE()
	new_site.get_site_size()
	new_site.download_site()
	new_site.print_info()

	#len(new_site.feed.entries)-1
	for x in range(0,len(new_site.feed.entries)-1):
		print(new_site.feed.entries[x].title)
	
	new_site.site = new_site.feed.entries[0].links[1].href
	#print(new_site.site)
	
	#names mp3 file with title of podcast episode
	new_site.mp3_name = new_site.feed.entries[0].title + '.mp3'
	
	if(platform.system() == 'Linux' or platform.system() == 'Darwin'):
		feed_path = unix_path
	elif platform.system() == 'Windows':
		feed_path = path_on_windows
	else:
		print("os not recognized")
	
	wget.download(new_site.site, feed_path + new_site.mp3_name)

if __name__ == '__main__':
	main()
	