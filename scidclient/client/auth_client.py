from typing import Any

from auth_storage.storage_provider import StorageProvider
from exceptions.exception_handler import ExceptionHandler
from exceptions.specific.invalid_pin_exception import InvalidPinException
from models.auth import Auth
from models.game_client import GameClient

from .base_client import BaseClient
from .pin_resolver.pin_resolver import PinResolver


class AuthClient:
    def __init__(
        self,
        mail: str,
        auth_storage: StorageProvider,
        game_client: GameClient,
        pin_resolver: PinResolver,
    ):
        self._request = BaseClient(game_client)
        self.__game_client = game_client
        self.__auth_storage = auth_storage
        self.__email = mail
        self.__pin_resolver = pin_resolver

    def authenticate(self) -> None:
        stored_auth = self.__auth_storage.load()
        if stored_auth and stored_auth.get_email() == self.__email:
            self._auth = stored_auth
        else:
            self.reauthenticate()

    def reauthenticate(self) -> None:
        self.__login()
        pin = self.__pin_resolver.get_pin(self.__email)
        try:
            self.__validate(pin)
        except InvalidPinException:
            self.reauthenticate()

        auth_response = self.__confirm(pin)
        auth = Auth(auth_response.get("email"), auth_response.get("scidToken"))
        self._auth = auth
        self.__auth_storage.store(auth)

    def __login(self) -> Any:
        login_data = {
            "lang": self.__game_client.get_language(),
            "email": self.__email,
            "remember": "true",
            "game": self.__game_client.get_game().value,
            "env": "prod",
        }
        return self._request.post("ingame/account/login", login_data)

    def __send_pin(self, endpoint: str, pin: int) -> Any:
        pin_data = {"email": self.__email, "pin": pin}
        return self._request.post(endpoint, pin_data)

    def __validate(self, pin: int) -> Any:
        return self.__send_pin("ingame/account/login.validate", pin)

    def __confirm(self, pin: int) -> Any:
        return self.__send_pin("ingame/account/login.confirm", pin)
