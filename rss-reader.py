#
# RSS Reader
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
		self.default = 'https://lexfridman.com/category/ai/feed/'#http://feeds.noisia.nl/NoisiaRadio
		self.site = ' '
		self.feed = ' '
		self.site_size = 0
		self.response = ' '
		self.file_number = 0
		self.mp3_feed = ' '
		self.mp3_name = ' '
		self.feed_length = 0
		self.podcast_number = None

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
			print(("%d: %s") % (x ,self.feed.entries[x].title))
		# Prints out entire website
		# Print( self.website )

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
			# print(dirName)
			if(dirName == unix_path):
				for fname in fileList:
					print("\t%s" % fname)
					# file_list.append(fname)	
					print(file_list)	
		elif platform.system() == 'Windows':
			# print(dirName)
			if(dirName == path_on_windows):
				for fname in fileList:
					print("\t%s" % fname)
					# file_list.append(fname)
					return subdirList
		else:
			print("os not recognized")

def options():
	menu = ['Add new Feed', 'Load Feeds', 'download']
	for x, i in enumerate(menu):
		print('%s. %s' % (x, i))
	menu_option = input("What would you like to do?")
	return menu_option

def save_file(feed_path, config_path, site):
	s = str(site.site)
	with open(config_path + 'config.txt', 'a+') as f:
		f.write(s + '\n')
	f.close()

def load_file(feed_path, config_path):
	new = SITE()
	with open(config_path + 'config.txt', 'r') as f:
		s = f.readlines()
	f.close()
	for x, i in enumerate(s):
		print('%s: %s' % (x,i),end='')
	get_user_input = int(input("What feed would you like to load?"))
	for x, i in enumerate(s):
		if get_user_input == x:
			new.site = str(i)
	
	download_feed(feed_path, config_path, new)

def add_new_feeds(feed_path, config_path):
	new = SITE()
	new.site = input('rss feed to add: ')
	save_file(feed_path, config_path, new)

def download_feed(feed_path, config_path, new_site):
	create_directories()
	sub_directory = get_file_list()
	print(sub_directory)
	if new_site.site == ' ':
		new_site.site = input('RSS feed to add: ')
	new_site.get_site_size()
	new_site.download_site()
	new_site.print_info()
	numbers = 0
	
	new_site.feed_length = len(new_site.feed.entries)-1
	new_site.podcast_number = int(input('What file would you like to download?'))
	new_site.mp3_feed = new_site.feed.entries[new_site.podcast_number].links[1].href

	# Names mp3 file with title of podcast episode
	# as well as replace any spaces with underscores
	new_site.mp3_name = new_site.feed.entries[new_site.podcast_number].title[0:20] + '.mp3'
	new_site.mp3_name.replace(' ', '_')
	
	# download preferred mp3
	answer = input("Are you sure you want to download " + "'" + new_site.feed.entries[new_site.podcast_number].title + "'")
	answer = answer.upper()

	if answer == 'Y':
		print(feed_path)
		print(new_site.site)
		print(new_site.mp3_feed)
		newnew = new_site.mp3_feed.find('/')
		i = 0
		for x in new_site.mp3_feed:
			if x == '\\':
				print(x)

		print(newnew)
		wget.download(new_site.mp3_feed, feed_path + new_site.mp3_name)

	save_it = input("Would you like to save this feed to use for later?")
	save_it = save_it.upper()
	
	if save_it == 'Y':
		save_file(feed_path, config_path, new_site)
	
def main():
	unix_feed_path = './feeds/'
	unix_config_path = './config/'
	windows_feed_path = '.\\feeds\\'
	windows_config_path = '.\\config\\'
	feed_path = ' '
	config_path = ' '

	if(platform.system() == 'Linux' or platform.system() == 'Darwin'):
		feed_path = unix_feed_path
		config_path = unix_config_path
	elif platform.system() == 'Windows':
		feed_path = windows_feed_path
		config_path = windows_config_path
	else:
		print("os not recognized")

	menu_option = options()

	if menu_option == '0':
		add_new_feeds(feed_path, config_path)
	elif menu_option == '1':
		load_file(feed_path, config_path)
	elif menu_option == '2':
		new_site = SITE()
		download_feed(feed_path, config_path, new_site)
	else: 
		print("none")

if __name__ == '__main__':
	main()
	