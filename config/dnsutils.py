import base64
import dns.query
import dns.tsig
import dns.tsigkeyring
import dns.update
import dns.zone
import json

from django.conf import settings

def get_keyring():
	return dns.tsigkeyring.from_text(settings.DNS_KEYRING)

def serialize(record):
	return base64.b64encode(json.dumps(record).encode('utf8'), altchars = b'+_').decode('utf8')
def unserialize(s):
	return json.loads(base64.b64decode(s.encode('utf8'), altchars = b'+_').decode('utf8'))

class Updater:
	def __init__(self, server, zone):
		self.__keyring = get_keyring()
		self.__update = dns.update.Update(zone, keyring = self.__keyring, keyalgorithm = dns.tsig.HMAC_MD5)
		self.__server = server
	def add(self, r):
		self.__update.add(r['rname'], r['rttl'], r['rtype'], r['rdata'])
	def delete(self, r):
		self.__update.delete(r['rname'], r['rtype'], r['rdata'])
	def send(self):
		return dns.query.tcp(self.__update, self.__server)

def get_zone_records(server, zone):
	records = []
	res = dns.zone.from_xfr(dns.query.xfr(server, zone))
	for name,val in res.iteritems():
		rname = name.to_text()
		for v in val.rdatasets:
			for x in v.items:
				r = {
					"rname": name.to_text(),
					"rttl": v.ttl,
					"rclass": dns.rdataclass.to_text(v.rdclass),
					"rtype": dns.rdatatype.to_text(v.rdtype),
					"rdata": x.to_text(),
				}
				r['serialized'] = serialize(r)
				records.append(r)
	return records
