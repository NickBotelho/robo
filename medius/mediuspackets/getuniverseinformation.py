
from utils import utils

class GetUniverseInformationSerializer:
	data_dict = [
		{'name': 'mediusid', 'n_bytes': 2, 'cast': None}
	]

class GetUniverseInformationHandler:
	def process(self, serialized, monolith, con):
		raise Exception('Unimplemented Handler: GetUniverseInformationHandler')

