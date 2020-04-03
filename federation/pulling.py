from django.utils import timezone

from .models import Server, Zone

import copy
import json
import urllib.parse
import urllib.request

class Pull:
	def __init__(self, remote):
		self.__remote = remote
		self.__missing = []
		self.__modified = []
		self.__warnings = []

	def missing(self):
		return self.__missing
	def modifications(self):
		return self.__modified
	def warnings(self):
		return self.__warnings

	def download(self):
		slaves = Server.objects.filter(remote = None, enabled = True)
		data = urllib.parse.urlencode({
			'remote': self.__remote.name, 
			'token': self.__remote.pull_token,
			'slaves': [s.name for s in slaves],
		}, True).encode("utf8")
		u = urllib.request.urlopen(self.__remote.pull_url, data = data)
		return json.loads(u.read().decode('utf8'))
	
	def get_server(self, name, data):
		try:
			s = Server.objects.get(name = name)
			if s.remote != self.__remote:
				self.__warnings.append("Server {} is associated with {}, please remove it first if you want to allow {} to change it.".format(s.name, s.remote.name, self.__remote.name))
				return None
			old = copy.copy(s.__dict__)
			modified = False
			for k,v in data.items():
				if v != s.__getattribute__(k):
					s.__setattr__(k, v)
					modified = True
			if modified:
				self.__modified.append((old,s))
			return s
		except Exception as e:
			s = Server(name = name, remote = self.__remote)
			for k,v in data.items():
				s.__setattr__(k, v)
			self.__missing.append(s)
			return s
	
	def get_zones(self, data):
		for s in data['server']:
			serv = self.get_server(s, data['server'][s])
			print("{} -> {}".format(s, serv))
			data['server'][s] = serv
		zones = []
		for zone in data['zones']:
			if data['server'][zone['master']] == None:
				continue
			zone['master'] = data['server'][zone['master']]
			zone['slaves'] = list(map(lambda s: data['server'][s], zone['slaves']))
			zones.append(zone)
		return zones

	def store_data(self, zones):
		for m in self.__modified:
			m.save()
		for zone in zones:
			try:
				z = Zone.objects.get(name = zone['name'])
				z.master = zone['master']
				z.slaves_all = zone['slaves_all']
			except Zone.DoesNotExist as e:
				z = Zone(
					name = zone['name'],
					master = zone['master'],
					slaves_all = zone['slaves_all']
				)
			z.save()
			z.slaves.set(zone['slaves'])
		self.__remote.pull_last = timezone.now()
		self.__remote.save()

def get_zones(remote):
	p = Pull(remote)
	zones = p.get_zones(p.download())
	return zones, p

def pull_and_store(remote):
	p = Pull(remote)
	zones = p.get_zones(p.download())
	p.store_data(zones)
