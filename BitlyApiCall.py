import urllib
import urllib2
import threading
import sublime

class BitlyApiCall(threading.Thread):
	def __init__(self, sel, string, timeout):
		self.sel = sel
		self.original = string
		self.timeout = timeout
		self.result = None
		threading.Thread.__init__(self)

	def run(self):
		login = 'the0ther'
		key = 'R_fa589cfdddea41f62a78e21f6e63677f'
		try:
			encUrl = urllib.urlencode({"longUrl": self.original})
			# reqUrl = 'https://ssl-api.bitly.com/v3/shorten?login=' + login + '&apiKey=' + key + '&' + encUrl
			reqUrl = 'http://api.bitly.com/v3/shorten?login=' + login + '&apiKey=' + key + '&' + encUrl
			print reqUrl
			request = urllib2.Request(reqUrl)
			http_file = urllib2.urlopen(request, timeout=self.timeout)
			self.result = http_file.read()
			print self.result
			return

		except (urllib2.HTTPError) as (e):
			err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
		except (urllib2.URLError) as (e):
			err = '%s: URL error %s contacting API' % (__name__, str(e.reason))

		sublime.error_message(err)
		self.result = False