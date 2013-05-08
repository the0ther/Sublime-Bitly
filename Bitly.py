# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import re
import json
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

		# self.view.sel().clear()

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
			self.view.set_status('bitly', 'Bitly [%s=%s]' % (' ' * before, ' ' * after))

			sublime.set_timeout(lambda: self.handle_threads(edit, threads, offset, i, dir), 100)
			return

		self.view.end_edit(edit)

		self.view.erase_status('bitly')
		#selections = len(self.view.sel())
		matches = len(urls)
		sublime.status_message('Bitly successfully run on %s selection%s' % (matches, '' if matches == 1 else 's'))

	def replace(self, edit, thread, offset):
		print 'entering replace()'
		sel = thread.sel
		original = thread.original
		result = thread.result
		print result

		# bitlyObj = json.loads(result)
		# print bitlyObj['data']['url']
		# bitlyUrl = bitlyObj['data']['url']

		# Here we adjust each selection for any text we have already inserted
		if offset:
			sel = sublime.Region(sel.begin() + offset, sel.end() + offset)

		# result = self.normalize_line_endings(result)
		# (prefix, main, suffix) = self.fix_whitespace(original, result, sel)
		#self.view.replace(edit, sel, prefix + main + suffix)
		# self.view.replace(edit, sel, prefix + main + suffix)
		self.view.replace(edit, sel, result)

		# We add the end of the new text to the selection
		# end_point = sel.begin() + len(prefix) + len(main)
		# self.view.sel().add(sublime.Region(end_point, end_point))

		# return offset + len(prefix + main + suffix) - len(original)
		return offset + 1

	def normalize_line_endings(self, string):
		string = string.replace('\r\n', '\n').replace('\r', '\n')
		line_endings = self.view.settings().get('default_line_ending')
		if line_endings == 'windows':
			string = string.replace('\n', '\r\n')
		elif line_endings == 'mac':
			string = string.replace('\n', '\r')
		return string

	def fix_whitespace(self, original, prefixed, sel):
		# If braces are present we can do all of the whitespace magic
		# if braces:
		# 	return ('', prefixed, '')

		(row, col) = self.view.rowcol(sel.begin())
		indent_region = self.view.find('^\s+', self.view.text_point(row, 0))
		if self.view.rowcol(indent_region.begin())[0] == row:
			indent = self.view.substr(indent_region)
		else:
			indent = ''

		prefixed = prefixed.strip()
		prefixed = re.sub(re.compile('^\s+', re.M), '', prefixed)

		settings = self.view.settings()
		use_spaces = settings.get('translate_tabs_to_spaces')
		tab_size = int(settings.get('tab_size', 8))
		indent_characters = '\t'
		if use_spaces:
			indent_characters = ' ' * tab_size
		prefixed = prefixed.replace('\n', '\n' + indent + indent_characters)
		match = re.search('^(\s*)', original)
		prefix = match.groups()[0]
		match = re.search('(\s*)\Z', original)
		suffix = match.groups()[0]

		return (prefix, prefixed, suffix)


# class BitlyResponse(object):
# 	def __init__(self, long_url, url, hash, global_hash, new_hash):
# 		self.long_url = long_url
# 		self.url = url
# 		self.hash = hash
# 		self.global_hash = global_hash
# 		self.new_hash = new_hash