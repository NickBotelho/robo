import os
os.chdir('test')
print(os.getcwd())
x = '''
	CLIENT_CONNECT_TCP = 0x00
	CLIENT_DISCONNECT = 0x01
	CLIENT_APP_BROADCAST = 0x02
	CLIENT_APP_SINGLE = 0x03
	CLIENT_APP_LIST = 0x04
	CLIENT_ECHO = 0x05
	SERVER_CONNECT_REJECT = 0x06
	SERVER_CONNECT_ACCEPT_TCP = 0x07
	SERVER_CONNECT_NOTIFY = 0x08
	SERVER_DISCONNECT_NOTIFY = 0x09
	SERVER_APP = 0x0a
	CLIENT_APP_TOSERVER = 0x0b
	UDP_APP = 0x0c
	CLIENT_SET_RECV_FLAG = 0x0d
	CLIENT_SET_AGG_TIME = 0x0e
	CLIENT_FLUSH_ALL = 0x0f
	CLIENT_FLUSH_SINGLE = 0x10
	SERVER_FORCED_DISCONNECT = 0x11
	CLIENT_CRYPTKEY_PUBLIC = 0x12
	SERVER_CRYPTKEY_PEER = 0x13
	SERVER_CRYPTKEY_GAME = 0x14
	CLIENT_CONNECT_TCP_AUX_UDP = 0x15
	CLIENT_CONNECT_AUX_UDP = 0x16
	CLIENT_CONNECT_READY_AUX_UDP = 0x17
	SERVER_INFO_AUX_UDP = 0x18
	SERVER_CONNECT_ACCEPT_AUX_UDP = 0x19
	SERVER_CONNECT_COMPLETE = 0x1a
	CLIENT_CRYPTKEY_PEER = 0x1b
	SERVER_SYSTEM_MESSAGE = 0x1c
	SERVER_CHEAT_QUERY = 0x1d
	SERVER_MEMORY_POKE = 0x1e
	SERVER_ECHO = 0x1f
	CLIENT_DISCONNECT_WITH_REASON = 0x20
	CLIENT_CONNECT_READY_TCP = 0x21
	SERVER_CONNECT_REQUIRE = 0x22
	CLIENT_CONNECT_READY_REQUIRE = 0x23
	CLIENT_HELLO = 0x24
	SERVER_HELLO = 0x25
	SERVER_STARTUP_INFO_NOTIFY = 0x26
	CLIENT_PEER_QUERY = 0x27
	SERVER_PEER_QUERY_NOTIFY = 0x28
	CLIENT_PEER_QUERY_LIST = 0x29
	SERVER_PEER_QUERY_LIST_NOTIFY = 0x2a
	CLIENT_WALLCLOCK_QUERY = 0x2b
	SERVER_WALLCLOCK_QUERY_NOTIFY = 0x2c
	CLIENT_TIMEBASE_QUERY = 0x2d
	SERVER_TIMEBASE_QUERY_NOTIFY = 0x2e
	CLIENT_TOKEN_MESSAGE = 0x2f
	SERVER_TOKEN_MESSAGE = 0x30
	CLIENT_SYSTEM_MESSAGE = 0x31
	CLIENT_APP_BROADCAST_QOS = 0x32
	CLIENT_APP_SINGLE_QOS = 0x33
	CLIENT_APP_LIST_QOS = 0x34
	CLIENT_MAX_MSGLEN = 0x35
	SERVER_MAX_MSGLEN = 0x36
'''
template = '''
from utils import utils

class {serializer}:
	data_dict = [
		{'name': 'rtid', 'n_bytes': 1, 'cast': utils.empty_cast},
		{'name': 'len', 'n_bytes': 2, 'cast': utils.bytes_to_int_little}
	]

	def serialize(self, data: bytes):
		raise Exception('Unimplemented Handler: {serializer}')
		return utils.serialize(data, self.data_dict)

class {handler}:
	def process(self, serialized, monolith, con):
		raise Exception('Unimplemented Handler: {handler}')

'''
for j in x.split("\n"):
	j = j.strip()
	if not j:
		continue
	kind = j.split()[0]
	val = j.split()[2]
	l = kind.lower().replace("_","")
	camelcase = ''.join([word.capitalize() for word in kind.lower().split("_")])
	serializer = camelcase + 'Serializer'
	handler = camelcase + 'Handler'
	print(l, serializer, handler)
	with open(f"{l}.py", 'w') as f:
		s = template.replace("{serializer}", serializer)
		s = s.replace("{handler}", handler)
		f.write(s)
	
