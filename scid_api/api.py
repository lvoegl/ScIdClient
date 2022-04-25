import json

import requests

import settings
from games import Games
from scid_api.auth import ScIdAuth
from scid_api.exceptions import ApiException, ApiContextException, AuthException


class ScIdApi:
    BASE_URL = 'https://id.supercell.com/api/'

    def __init__(self, mail: str, game: Games, auth_file_name: str):
        self.__client_version = settings.CLIENT_VERSION
        self.__client_os = settings.CLIENT_OS
        self.__lang = settings.LANG_CODE
        self.__game = game.value
        self.__mail = mail
        self.__auth = None
        self.__auth_file_name = auth_file_name

    def authenticate(self):
        auth = self.__load_auth()

        if auth is not None and auth.get_mail() == self.__mail and not auth.has_expired():
            self.__auth = auth
        else:
            self.__login()
            pin = self.__get_pin()
            self.__validate(pin)
            auth_json = self.__confirm(pin)
            self.__auth = ScIdAuth(auth_json)
            self.__save_auth()

    def __load_auth(self):
        try:
            with open(self.__auth_file_name, 'r', encoding='utf-8') as auth_file:
                auth_data = auth_file.read()
                try:
                    return ScIdAuth(json.loads(auth_data))
                except ValueError:
                    return None
        except FileNotFoundError:
            return None

    def __save_auth(self):
        with open(self.__auth_file_name, 'w', encoding='utf-8') as auth_file:
            auth_file.write(self.__auth.json_dump())

    def __get_pin(self):
        while True:
            try:
                pin_str = input(f'Pin for {self.__mail}: ')
                return int(pin_str)
            except ValueError:
                print('Pin must be a 6-digit number')

    def __login(self):
        login_data = {
            'lang': self.__lang,
            'email': self.__mail,
            'remember': True,
            'game': self.__game,
            'env': 'prod'
        }
        return self.__post('ingame/account/login', data=login_data, authenticate=False)

    def __send_pin(self, endpoint: str, pin: int):
        pin_data = {
            'email': self.__mail,
            'pin': pin
        }
        return self.__post(endpoint, data=pin_data, authenticate=False)

    def __validate(self, pin: int):
        return self.__send_pin('ingame/account/login.validate', pin)

    def __confirm(self, pin: int):
        return self.__send_pin('ingame/account/login.confirm', pin)

    def send_friend_request(self, player_tag: str):
        return self.send_friend_requests([player_tag])

    def send_friend_requests(self, player_tags: list[str]):
        normalized_tags = [
            f'#{tag.replace("#", "").upper()}' for tag in player_tags]
        str_tags = str(normalized_tags).replace("'", '"')
        friend_data = {
            'appAccounts': str_tags
        }
        content = self.__post('social/v3/friends.createRequest',
                              data=friend_data, authenticate=True)
        players = content.get('appAccounts', {}).items()
        failed_players = [p for p in players if not p[1].get('ok', False)]

        if len(failed_players) > 0:
            error_msgs = [
                f'{p[0]}: {p[1].get("error", "no error message")}' for p in failed_players
            ]
            raise ApiContextException('; '.join(error_msgs))

        return content

    def __post(self, endpoint: str, data=None, authenticate: bool = False):
        headers = self.__build_headers(authenticate)
        req = requests.post(
            f'{ScIdApi.BASE_URL}/{endpoint}', data=data, headers=headers)

        if req.status_code != 200:
            raise ApiException(f'response code {req.status_code}: {req.text}')

        content = req.json()
        if not content.get('ok', False):
            raise ApiContextException(content.get('error', 'no error message'))

        return content.get('data', None)

    def __build_headers(self, authenticate: bool):
        headers = {
            'User-Agent': f'scid/{self.__client_version} ({self.__client_os}; {self.__game}-prod)'
        }

        if authenticate:
            if self.__auth is None:
                raise AuthException('no authentication found')

            if self.__auth.has_expired():
                raise AuthException('authentication token has expired')

        if authenticate:
            headers['Authorization'] = f'Bearer {self.__auth.get_token()}'

        return headers
