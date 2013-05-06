import sublime, sublime_plugin

class BitlyShortenCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.view.insert(edit, 0, "Hello, World!")
		href = False
		sels = self.view.sel()
		for sel in sels:
			if self.view.substr(sel).find('{') != -1:
				href = True
		if not href:
			new_sels = []
			for sel in sels:
				new_sels.append(self.view.find('\}', sel.end()))
			sels.clear()
			for sel in new_sels:
				sels.add(sel)
			self.view.run_command("expand_selection", { "to": "brackets" })