
from utils import utils

class CreateChannelSerializer:
	data_dict = [
		{'name': 'mediusid', 'n_bytes': 2, 'cast': None}
	]

class CreateChannelHandler:
	def process(self, serialized, monolith, con):
		raise Exception('Unimplemented Handler: CreateChannelHandler')

