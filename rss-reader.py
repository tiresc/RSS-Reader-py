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
		self.content = ' ' # Raw website information
		self.site = ' ' # Site Address
		self.site_size = 0 # Size in Bytes
		self.parsed_site = ' ' # Parsed website

		self.mp3 = ' ' # mp3 url
		self.mp3_name = ' ' # name of mp3
		self.mp3_index = 0 # mp3 index

	def if_empty(self):
		if self.site == ' ':
			self.site = input('RSS feed to add/download: ')

	def download_site(self):
		with urllib.request.urlopen(self.site) as f:
			self.content = f.read(self.site_size).decode('utf-8')
			print(self.site_size)
		self.parsed_site = feedparser.parse(self.site)
	
	# byte size of website
	def get_site_size(self):
		# Gets Byte size of website
		response = requests.get(self.site)
		self.site_size = len(response.content)

	def print_info(self):
		for x in range(0,len(self.parsed_site.entries)):
			print(("%d: %s") % (x ,self.parsed_site.entries[x].title))
		
		# Prints out entire website
		# Print( self.content )

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

def options(menu):
	length = 0
	for x, i in enumerate(menu):
		length = length + 1
		print('%s. %s' % (x, i))
		
	menu = input("What would you like to do?")
	return menu, length


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

def download_feed(feed_path, config_path, site):
	create_directories()
	sub_directory = get_file_list()
	print(sub_directory)
	
	site.if_empty()
	site.get_site_size()
	site.download_site()
	site.print_info()
	numbers = 0
	
	site.mp3_index = int(input('What file would you like to download?'))
	site.mp3_feed = site.parsed_site.entries[site.mp3_index].links[1].href

	# Names mp3 file with title of podcast episode
	# as well as replace any spaces with underscores
	site.mp3_name = site.parsed_site.entries[site.mp3_index].title[0:20] + '.mp3'
	site.mp3_name.replace(' ', '_')
	
	# download preferred mp3
	answer = input("Are you sure you want to download " + "'" + site.parsed_site.entries[site.mp3_index].title + "'")
	answer = answer.upper()

	if answer == 'Y':
		print('feed path:' + feed_path)
		print('site_url' + site.site)
		print('mp3 feed:' + site.mp3_feed)
		print('mp3 name:' + site.mp3_name)
		newnew = site.mp3_feed.find('/')
		i = 0
		for x in site.mp3_feed:
			if x == '\\':
				print(x)

		print(newnew)
		wget.download(site.mp3_feed, feed_path + site.mp3_name)

	save_it = input("\nWould you like to save this feed to use for later?")
	save_it = save_it.upper()
	
	if save_it == 'Y':
		save_file(feed_path, config_path, site)

def assign_paths():
	unix_feed_path = './feeds/'
	unix_config_path = './config/'
	windows_feed_path = '.\\feeds\\'
	windows_config_path = '.\\config\\'

	if(platform.system() == 'Linux' or platform.system() == 'Darwin'):
		feed_path = unix_feed_path
		config_path = unix_config_path
		return feed_path, config_path
	elif platform.system() == 'Windows':
		feed_path = windows_feed_path
		config_path = windows_config_path
		return feed_path, config_path
	else:
		print("os not recognized")

def menu_options():
	while True:
		try:
			menu, length = options(['Add new Feed', 'Load Feeds', 'download'])
			menu = int(menu)
		except ValueError:
			print("Sorry, I didn't understand that.")
			continue
		if menu < 0 or menu > length:
			print("Sorry, your response must within choice range given.")
			continue
		else:
			return menu

def main():
	feed_path, config_path = assign_paths()

	menu = menu_options()
	print(menu)
	
	if menu == 0:
		add_new_feeds(feed_path, config_path)
	elif menu == 1:
		load_file(feed_path, config_path)
	elif menu == 2:
		site = SITE()
		download_feed(feed_path, config_path, site)
	
	
if __name__ == '__main__':
	main()