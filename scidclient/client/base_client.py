from typing import Any, Dict

import json

import requests

from auth_storage.storage_provider import StorageProvider
from exceptions.api_exception import ApiException
from exceptions.exception_handler import ExceptionHandler
from models.auth import Auth
from models.game_client import GameClient
from models.games import Games

from .pin_resolver.pin_resolver import PinResolver


class BaseClient:
    __BASE_URL = "https://id.supercell.com/api"

    def __init__(
        self,
        game_client: GameClient,
    ):
        self.__game_client = game_client

    def __handle_response(self, req: requests.Response) -> dict[str, Any]:
        try:
            content = req.json()
        except json.decoder.JSONDecodeError:
            raise ApiException(req.text)

        if not content.get("ok", False):
            error = content.get("error")

            specific_exception = ExceptionHandler.get_exception(error)
            if specific_exception is not None:
                raise specific_exception()

            raise ApiException(error)

        return content.get("data")

    @staticmethod
    def __format_token(token: str) -> str:
        if token != "":
            token = f"Bearer {token}"

        return token

    def _build_headers(self, token: str) -> dict[str, str]:
        headers = {
            "User-Agent": f"scid/{self.__game_client.get_version()} ({self.__game_client.get_os()}; {self.__game_client.get_game().value}-prod)",
            "Authorization": self.__format_token(token),
        }

        return headers

    def post(self, endpoint: str, data: dict[str, Any], token: str = "") -> dict[str, Any]:
        headers = self._build_headers(token)
        res = requests.post(f"{BaseClient.__BASE_URL}/{endpoint}", data=data, headers=headers)

        return self.__handle_response(res)
