from enums.enums import MediusWorldStatus, MediusEnum, RtIdEnum
from utils import utils

import logging
logger = logging.getLogger('robo.game')


class Game:
	def __init__(self, dme_world_id: int, create_game_serialized: dict):
		self._status = MediusWorldStatus.WORLD_PENDING_CREATION
		self._dme_world_id = dme_world_id
		self._create_game_serialized = create_game_serialized

		self._stats = utils.bytes_from_hex(''.join(['00'] * MediusEnum.GAMESTATS_MAXLEN))


		self._possible_dme_player_ids = {0,1,2,3,4,5,6,7}
		# Dict for dme player id -> Player
		self._players = {}

	def get_mls_world_id(self):
		return self._create_game_serialized['game_level']

	def get_game_status(self) -> MediusWorldStatus:
		return self._status

	def player_tcp_connected(self, player, dmetcp_con) -> None:
		'''A player has just connected to this dme world via tcp.

		1. Generate a new dme player id for this player.
		2. Add this connection to the player list
		3. Set this game in the dmetcp connection
		4. Start the tcpflusher coroutine

		'''
		dme_player_id = self._generate_new_dme_player_id()
		self._players[dme_player_id] = player

		player.set_dmetcp_con(dmetcp_con)
		# Set the game to be referenced by this player
		player.set_game(self)
		# Start the TCP flush coroutine
		player.start_tcpflusher()

		self._status = MediusWorldStatus.WORLD_STAGING

	def player_udp_connected(self, dme_player_id: int, udp_con) -> None:
		player = self._players[dme_player_id]
		player.set_dmeudp_con(udp_con)
		# Start the UDP flush coroutine
		player.start_udpflusher()


	def player_disconnected(self, player):
		pass

	def _generate_new_dme_player_id(self):
		return min(self._possible_dme_player_ids.difference(set(self._players.keys())))

	def get_player_count(self) -> int:
		return len(self._players)

	def get_dme_world_id(self):
		return self._dme_world_id

	def get_dme_player_id(self, player):
		for dme_player_id, p in self._players.items():
			if player == p:
				return dme_player_id

	def get_player_by_dme_player_id(self, dme_player_id):
		return self._players[dme_player_id]

	def dmetcp_broadcast(self, player, data: bytes):
		source_dme_player_id = self.get_dme_player_id(player)

		packet = utils.format_rt_message(RtIdEnum.CLIENT_APP_SINGLE, utils.int_to_bytes_little(2,source_dme_player_id), data)

		for dest_player in self._players.values():
			if dest_player != player:
				dest_player.send_dmetcp(packet)

	def dmeudp_broadcast(self, player, data: bytes):
		source_dme_player_id = self.get_dme_player_id(player)

		packet = utils.format_rt_message(RtIdEnum.CLIENT_APP_SINGLE, utils.int_to_bytes_little(2, source_dme_player_id), data)

		for dest_player in self._players.values():
			if dest_player != player:
				dest_player.send_dmeudp(packet)


	def get_created_info(self):
		return self._create_game_serialized

	def get_stats(self):
		return self._stats

	def set_stats(self, stats):
		self._stats = stats