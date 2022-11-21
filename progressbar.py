import sys

""" Personal go at the progress bar. Inspired by various solutions"""
class ProgressBar():
	def __init__(self, n_elements, prefix="", width=20, char_void=" ", char_fill="#", start_now=True):
		self.delta = width/n_elements
		self.width = width
		self.char_fill = char_fill
		self.char_void = char_void
		self.prefix = prefix
		self.current = 0.5
		if start_now:
			self.start()

	""" Initializes the progressbar display."""
	def start(self):
		print("{}[{}{}] {}".format(self.prefix, 
								"", 
								self.char_void*self.width,
								"0%"), 
                end='\r', file=sys.stdout, flush=True)
	""" Terminates the progress, wrapping up."""
	def end(self):
		print("\n", file=sys.stdout, flush=False)

	""" Brings back to original state."""
	def refresh(self):
		self.current = 0.5

	""" Increments the pb according to the calculated width delta per unit."""
	def update(self):
		self.current += self.delta
		percent = min(int(100*self.current/self.width), 100)
		print("{}[{}{}] {}%".format(self.prefix, 
								int(self.current)*self.char_fill, 
								(self.width-int(self.current))*self.char_void,
								percent),
                end='\r', file=sys.stdout, flush=True)