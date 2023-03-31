from models.games import Games


class GameClient:
    def __init__(self, game: Games, version: int, os: str, language: str):
        self.__game = game
        self.__version = version
        self.__os = os
        self.__language = language

    def get_game(self) -> Games:
        return self.__game

    def get_version(self) -> int:
        return self.__version

    def get_os(self) -> str:
        return self.__os

    def get_language(self) -> str:
        return self.__language
