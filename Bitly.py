import sublime
import sublime_plugin
import re
import json
import urlparse



from BitlyApiCall import BitlyApiCall


class BitlyShortenCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # print "inside run"

    # replace with regex from here: http://stackoverflow.com/questions/1986059/grubers-url-regular-expression-in-python
    # here is the full explanation of this regex: http://alanstorm.com/url_regex_explained
    # Using now:
    # \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^%s\s]|/)))
    # Original Gruber:
    # \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))

    # Best try in Python:

    # 1. \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]|/)))
    # 2. \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[-!\"#$%&\'()*+,./:;<=>?@\\[\\\\]^_`{|}~]\s]|/)))
    # 3. \b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\s]|/)))
    # 4. Jeff Atwoods \(?\bhttp://[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]
    #     This also has a parens cleanup routine at the end of it

    # str = re.findall(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[-!\"#$%&\'()*+,./:;<=>?@\\[\\\\]^_`{|}~]\s]|/)))', 'http://example.com/this/path/1?asdf=qwer&qwer=asdf')

    self.settings = sublime.load_settings("Bitly.sublime-settings")

    self.urls = self.view.find_all(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\s]|/)))\b')
    # print self.urls
    threads = []
    for url in self.urls:
      # print url
      string = self.view.substr(url)
      string = self.strip_parens(string)

      # print "string stripped: " + string

      # print self.settings.get("api_login")
      # print "user " + str(self.view.settings().get("api_login"))

      thread = BitlyApiCall(url, string, 15, self.settings.get("api_login"), self.settings.get("api_key"))
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

  def strip_parens(self, strUrl):
    asStr = str(strUrl)
    # print asStr
    # return asStr    
    if asStr[-1] == ")":
      # print "found parens"
      return asStr[0:len(asStr)-1]
    else:
      return asStr