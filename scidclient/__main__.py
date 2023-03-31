from auth_storage.file_storage import FileStorage
from client.client import Client
from client.pin_resolver.manual_pin_resolver import ManualPinResolver
from exceptions.specific.unauthorized_exception import UnauthorizedException
from models.game_client import GameClient
from models.games import Games

game_client = GameClient(Games.CLASH_ROYALE, 4543, "Android", "en")
auth_storage = FileStorage("auth.json")
pin_resolver = ManualPinResolver()

client = Client("example@example.org", auth_storage, game_client, pin_resolver)
client.authenticate()

tag = "#A0B1C2"

try:
    res = client.send_friend_request(tag)
except UnauthorizedException:
    client.reauthenticate()
    res = client.send_friend_request(tag)

print(res)
