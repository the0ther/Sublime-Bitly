# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import re
import json
from BitlyApiCall import BitlyApiCall


class BitlyShortenCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # replace with regex from here: http://stackoverflow.com/questions/1986059/grubers-url-regular-expression-in-python
    self.urls = self.view.find_all(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^%s\s]|/)))')
    threads = []
    for url in self.urls:
      string = self.view.substr(url)
      thread = BitlyApiCall(url, string, 15)
      threads.append(thread)
      thread.start()

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
    matches = len(self.urls)
    sublime.status_message('Bitly successfully run on %s selection%s' % (matches, '' if matches == 1 else 's'))

  def replace(self, edit, thread, offset):
    sel = thread.sel
    original = thread.original
    result = thread.result

    # Here we adjust each selection for any text we have already inserted
    if offset:
      # print 'offset: %s' % offset
      sel = sublime.Region(sel.begin() + offset, sel.end() + offset)

    self.view.replace(edit, sel, result)

    # We add the end of the new text to the selection
    return offset + len(result) - len(original)