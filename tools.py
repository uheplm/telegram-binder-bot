import json

class JSONWorker(object):
	'''JSONWorker object
	param path - path to json file
	'''
	def __init__(self, path = None):
		super(JSONWorker, self).__init__()
		self.path = path
		with open(path) as data:
			self._data = json.loads(data.read())

	def get(self, string = ''):
		query = string if type(string) is list else string.split('.')
		query_step = self._data
		try:
			if not string == "":
				for i in query:
					query_step = query_step[i]
				return query_step
			else: return query_step
		except KeyError:
			return None

	def set(self, string = '',value = None):
		query = string.split('.')
		branch = self._data
		cache = []
		try:
			for i in query:
				if type(branch[i]) is dict:
					cache.append(branch[i])
					branch = branch[i]
				else:
					break
			cache.reverse()
			query.reverse()
			cache[0][query[0]] = value
			for b in range(len(cache) - 1):
				if not b == 1:
					cache[b-1].update(cache[b])
			query.reverse()
			self._data[query[0]] = cache[len(cache)-1]
			return True
		except KeyError:
			return False

	def write(self):
		file = open(self.path,'w')
		file.write(json.dumps(storage))
		file.close()

class Chat(object):
	def __init__(self, chatid, bot):
		super(Chat, self).__init__()
		self.cid = chatid
	def getAdmins(self):
		admins = self.bot.get_chat_administrators(self.cid)
		result = []
		for i in admins:
			result.append(i.user.id)
		result.append(cfg.superadmin)
		return result

	def getID(self):
		return self.cid