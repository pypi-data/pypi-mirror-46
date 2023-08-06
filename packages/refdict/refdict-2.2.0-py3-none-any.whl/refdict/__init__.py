class refdict:
	def __init__(self, data, refPrefix = '@', separator = '.'):
		self.__prefix = refPrefix
		self.data = data
		self.__separator = separator

	def load(self, data):
		self.data = data
		return self

	def __getitem__(self, keys):
		# if keys is an int or a slice (self.data is a str or list or tuple)
		if isinstance(keys, int) or isinstance(keys, slice):
			return self.data[keys]
		# else, keys must be a str
		elif not isinstance(keys, str):
			raise TypeError('refdict.__getitem__ can just accept str, int or slice as keys')
		# default result is the whole dict
		result = self.data
		keys = keys.split(self.__separator)
		while len(keys):
			# every time pop the first key
			key = keys.pop(0)
			# get the original result
			if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
				# use `eval` to support slice operation
				result = eval('result[' + key + ']')
			else:
				# see result as a dict, use key as a string
				result = result[key]
			# if result is a reference string, redirect it to its target
			while isinstance(result, str) and result.startswith(self.__prefix):
				# add target infront of keys
				# because target can have many parts divided by self.__separator
				keys = result[len(self.__prefix):].split(self.__separator) + keys
				# result is the top-level object again
				result = self.data
		return result

	def __setitem__(self, keys, value):
		# if keys is a slice or an int (maybe self.data is str or list or tuple)
		if isinstance(keys, int) or isinstance(keys, slice):
			self.data[keys] = value
			return
		# else, keys must be str
		elif not isinstance(keys, str):
			raise TypeError('refdict.__setitem__ can just accept int, str or slice as keys')

		result = None
		keys = keys.split(self.__separator)
		# idea: self.data[keys[:-1]][keys[-1]] = value, based on self.__getitem__
		# first, let result = self.data[keys[:-1]]
		if len(keys) == 1:
			result = self.data
		else:
			result = self[self.__separator.join(keys[:-1])]
		# then, result = result[keys[-1]]
		# if result is a reference string, redirect it to its target
		if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
			# use `exec` to support slice assignment
			result = exec('result[' + keys[-1] + '] = value')
		else:
			result[keys[-1]] = value
	
	def text(self, keys):
		'''
		get value, if the value the last key is a ref string, return the ref string
		'''
		# if keys is a slice or an int (maybe self.data is a str or list or tuple)
		if isinstance(keys, int) or isinstance(keys, slice):
			return self.data[keys]
		elif not isinstance(keys, str):
			raise TypeError('refdict.text can just accept int, str or slice as keys')
		keys = keys.split(self.__separator)
		# idea: return self.data[keys[:-1]][key[-1]], based on self.__getitem__
		# first, let result = self.data[keys[:-1]]
		if len(keys) == 1:
			result = self.data
		else:
			result = self[self.__separator.join(keys[:-1])]
		# then, result = result[keys[-1]]
		if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
			# use `eval` to support slice operation
			result = eval('result[' + keys[-1] + ']')
		else:
			# see result as a dict, use key as a string
			result = result[keys[-1]]
		return result

	def __getattr__(self, funcName):
		return eval('self.data.' + funcName)

	def __str__(self):
		return str(self.data)

	def __contains__(self, keys):
		if not isinstance(keys, str):
			return keys in self.data
		keys = keys.split(self.__separator)
		if len(keys) == 1:
			return keys in self.data
		resultContainer = None
		try:
			resultContainer = self['.'.join(keys[:-1])]
		except:
			return False
		return keys[-1] in resultContainer


	def __delitem__(self, keys):
		# if keys is an int or a slice (maybe self.data is a str or list or tuple)
		if isinstance(keys, int) or isinstance(keys, slice):
			del self.data[keys]
		# or keys must be a str
		elif not isinstance(keys, str):
			raise TypeError('refdict.__delitem__ can just accept int, str or slice as keys')
		keys = keys.split(self.__separator)
		# idea: del self.data[keys[:-1]][keys[-1]], based on self.__getitem__
		# first, let result = self.data[keys[:-1]]
		result = self.data
		if len(keys) > 1:
			result = self[self.__separator.join(keys[:-1])]
		# then, result = result[keys[-1]]
		if isinstance(result, list) or isinstance(result, tuple) or isinstance(result, str):
			# use `eval` to support slice operation
			exec('del result[' + keys[-1] + ']')
		else:
			# see result as a dict, use key as a string
			del result[keys[-1]]

	def __iter__(self):
		return iter(self.data)

	def __repr__(self):
		return repr(self.data)
