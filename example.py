from scid_api.api import ScIdApi
from games import Games


mail = 'name@example.org'
game = Games.CLASH_ROYALE
auth_file_name = 'auth.json'

api = ScIdApi(mail, game, auth_file_name=auth_file_name)
api.authenticate()

api.send_friend_request('#PLAYER_TAG')
