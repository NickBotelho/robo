from enums.enums import MediusEnum, CallbackStatus, WorldSecurityLevelType
from utils import utils
from medius.mediuspackets.channellist_extrainforesponse import ChannelList_ExtraInfoResponseSerializer

class ChannelList_ExtraInfo1Serializer:
    data_dict = [
        {'name': 'mediusid', 'n_bytes': 2, 'cast': None},
        {'name': 'message_id', 'n_bytes': MediusEnum.MESSAGEID_MAXLEN, 'cast': None},
        {'name': 'page_id', 'n_bytes': 2, 'cast': None},
        {'name': 'page_size', 'n_bytes': 2, 'cast': None}
    ]


class ChannelList_ExtraInfo1Handler:
    def process(self, serialized, monolith, con):
        generic_field1 = 1
        generic_field2 = 1
        generic_field3 = 0
        generic_field4 = 0
        generic_field_filter = 32
        
        packets = []
        channels = monolith.get_channels()
        for i in range(len(channels)):
            packets.append(ChannelList_ExtraInfoResponseSerializer.build(
                serialized['message_id'],
                CallbackStatus.SUCCESS,
                channels[i]['id'], # World id
                0, # TODO: update later, not really needed, doesn't through later. [PLAYER COUNT]
                channels[i]['max_players'],
                WorldSecurityLevelType.WORLD_SECURITY_NONE, # This will always be none for UYA cities
                generic_field1,
                generic_field2,
                generic_field3,
                generic_field4,
                generic_field_filter,
                channels[i]['name'],
                int(i == (len(channels)-1)) # end of list
            ))

        return packets