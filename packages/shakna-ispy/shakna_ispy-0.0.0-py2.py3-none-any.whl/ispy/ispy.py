class fn(object):
	def __init__(self, *args):
		self.values = list(args)

	def __call__(self):
		return slist(*self.values)

	def __iter__(self):
		yield from self.values

	def __getitem__(self, key):
		return self.values[key]

	def __setitem__(self, key, value):
		self.values[key] = value

class _SList(object):
	"""The backend of the slist."""
	def __init__(self, *args):
		if hasattr(args[0], "__call__"):
			self.values = list(args[1:])

			# Convert list items to slist too.
			for idx, item in enumerate(self.values):
				if isinstance(item, list):
					self.values[idx] = slist(*item)

			self.exec = args[0]
		else:
			self.values = list(args)
			self.exec = None

	def __call__(self):
		if self.exec:
			return self.exec(*self.values)
		else:
			return self.values

	def __iter__(self):
		if self.exec:
			yield from [self.exec, *self.values]
		else:
			yield from self.values

	def __getitem__(self, key):
		if self.exec:
			return [self.exec, *self.values][key]
		else:
			return self.values[key]

def slist(*args):
	"""Create a lisp-style list that is also a lambda"""
	return _SList(*args)()