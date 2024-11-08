#Modules needed
import requests
import argparse
import time
import sys
import os
import threading

#Colors using ANSI escapes
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
RESET='\033[0m'

class Dirbuster:
	def __init__(self, url, wordlist, thread, ext, filter_size, filter_code, method):
		self.url = url
		self.wordlist = wordlist
		self.thread = int(thread)
		self.extensions = ext
		self.filter_size = filter_size
		self.filter_code = filter_code
		self.method = method
		
	def write_file(self, line):
		with open("lines.txt", "a") as writing:
			writing.write(line)
			
	def check_url(self):
		if not self.url.endswith("/"):
			self.url += "/"
	
	def read_wordlist(self):
		#Will contain our valid directory names to try
		lines = []
		with open(self.wordlist, "r") as word_list:
			for line in word_list:
				if ("#" not in line):
					lines.append(line.strip())
					if self.extensions:
						ext_list = self.extensions.split(",")
						for ext in ext_list:
							#add everything together while removing the newline from the wordlist input
							end = line.strip()+"."+ext
							lines.append(end.strip())
		return lines

	#function that seperates the wordlist into groups for threading
	def seperate_wordlist(self):
		lines = self.read_wordlist()
		#To count the number of lines, help seperate for threads equally
		size = len(lines)
		#Value that determines how many lines of the wordlist we will have
		num_group = int(size / self.thread)
		#list of lists that will contain all the groups
		line_struct = []
		#temporary list that will hold the values of the wordlist for the group until we hit the maximum, which then will be cleared
		temp_list = []
		#to keep track of the file ending, so that the rest of the lines can be added to the final structure
		counter = 1
		for line in lines:
			temp_list.append(line)
			if ((len(temp_list) == num_group) or (counter == size)):
				#the list of list will append the list of a given size to create groups for our threads
				line_struct.append(temp_list)
				temp_list = []
			counter += 1
		return line_struct

	#function to send directory names with a list as input (our threads will execute this function at the same time)
	def send_payload(self, payload_list):
		for payload in payload_list:
			#add a slash at the end of the base URL if there isn't one already
			self.check_url()
			#append the entry of the wordlist to the url
			full_path = self.url+payload
			try:
				r = requests.get(url=full_path)
			#maybe get precise on errors here one day
			except Exception as e:
				print(RED+"Error with request, sleeping for 10 seconds"+RESET)
				time.sleep(10)
			#option to change this potentially
			if (r.status_code != 404):
				size = len(r.content)
				code = r.status_code
				
				if ((self.filter_size != size) and (self.filter_code != code)):
					final = "[+] /" + payload + " seems to exist | Size: " + str(size) + " | Response: " + str(code)
					#self.write_file(final) - for later
					#dividing color based on response code value
					if (code < 300):
						print(GREEN+final+RESET)
					elif (code < 400):
						print(BLUE+final+RESET)
					else:
						#useful for code 405, wrong method but endpoint or file still exists					
						print(YELLOW+final+RESET)
					
	
	def thread_dirs(self, dir_list):
		threads = []
		
		for dir in dir_list:
			thread = threading.Thread(target=self.send_payload, args=(dir,))
			threads.append(thread)
			#To exit program on CTRL+C, not a very clean exit but it works for now
			thread.daemon = True
			thread.start()

		try:
			for thr in threads:
				thr.join()
		#detect CTRL+C for a cleaner terminal output
		except KeyboardInterrupt:
			print(RED+"Aborting..."+RESET)


def main():
	parser = argparse.ArgumentParser(
		description='Brute-force the existence of files, folders and endpoints.', 
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	
	parser.add_argument('url', type=str, help='The target URL')
	parser.add_argument('wordlist', type=str, help='A list of possible results')
	parser.add_argument('-t', '--threads', type=int, default=40, help='The number of threads to run')
	parser.add_argument('-x', '--extensions', type=str, help='A list of extensions to check at the end of files: php,html,...')
	parser.add_argument('-fs', '--size', type=int, help='Size of the response to filter out')
	parser.add_argument('-fc', '--code', type=int, help='Status code of the response to filter out')
	parser.add_argument('-m', '--method', type=str, help='HTTP method to use')
	
	args = parser.parse_args()

	URL = args.url
	WORD = args.wordlist
	THR = args.threads
	EXT = args.extensions
	SIZE = args.size
	CODE = args.code
	METHOD = args.method
	
	dirb = Dirbuster(URL, WORD, THR, EXT, SIZE, CODE, METHOD)
	test = dirb.seperate_wordlist()
	dirb.thread_dirs(test)
	
if __name__ == '__main__':		
	main()
