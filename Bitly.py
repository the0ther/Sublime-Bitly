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

		self.view.sel().clear()

		edit = self.view.begin_edit('bitly')

		self.handle_threads(edit, threads)

	def handle_threads(self, edit, threads, offset=0, i=0, dir=1):
		next_threads = []
		for thread in threads:
			if thread.is_alive():
				next_threads.append(thread)
				continue
			if thread.result == False:
				continue
			offset = self.replace(edit, thread, offset)
		threads = next_threads



		if len(threads):
			# This animates a little activity indicator in the status area
			before = i % 8
			after = (7) - before
			if not after:
				dir = -1
			if not before:
				dir = 1
			i += dir
			self.view.set_status('prefixr', 'Prefixr [%s=%s]' % (' ' * before, ' ' * after))

			sublime.set_timeout(lambda: self.handle_threads(edit, threads, offset, i, dir), 100)
    	return