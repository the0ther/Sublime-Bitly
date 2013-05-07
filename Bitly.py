# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from BitlyApiCall import BitlyApiCall

class BitlyShortenCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#api_call = BitlyApiCall()
		# replace with regex from here: http://stackoverflow.com/questions/1986059/grubers-url-regular-expression-in-python
		urls = self.view.find_all(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^%s\s]|/)))')
		#print urls
		threads = []
		for url in urls:
			string = self.view.substr(url)
			#print string
			thread = BitlyApiCall(url, string, 15)
			threads.append(thread)
			thread.start()