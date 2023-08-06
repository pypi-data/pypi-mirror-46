import unittest
import asyncio

from rcon_server import RCONServer
from rcon_packet import RCONPacket

class TestRCONServer(RCONServer):

    def handle_execcommand(self, packet, connection):
        packet.type = RCONPacket.SERVERDATA_RESPONSE_VALUE
        connection.send_packet(packet)

server = TestRCONServer(bind=("127.0.0.1",27015),password="test")
asyncio.run(server.listen())
