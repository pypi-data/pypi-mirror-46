from rcon_client import RCONClient

#rcon = RCONClient("host-1.swagspace.org", 27015, "wJIw0QDv5iTNhgEz09ESeG9abwulBk3q")
rcon = RCONClient("host-1.swagspace.org", 27015, "derpderp")
rcon.connect()
rcon.login()
print(rcon.send_command("status"))
