import urllib
import urllib2
import threading

class BitlyApiCall(threading.Thread):
	def __init__(self, sel, string, timeout):
		self.sel = sel
		self.original = string
		self.timeout = timeout
		self.result = None
		threading.Thread.__init__(self)

		# the0ther
		# R_fa589cfdddea41f62a78e21f6e63677f
	def run(self):
		try:
			data = urllib.urlencode({'longUrl': self.original})
			request = urllib2.Request('http://bit.ly/v3/shorten', data, headers={"User-Agent": "Sublime Bitly"})
			http_file = urllib2.urlopen(request, timeout=self.timeout)
			self.result = http_file.read()
			return

		except (urllib2.HTTPError) as (e):
			err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
		except (urllib2.URLError) as (e):
			err = '%s: URL error %s contacting API' % (__name__, str(e.reason))

		sublime.error_message(err)
		self.result = False