from typing import Any, Dict, List

from exceptions.api_exception import ApiException

from .auth_client import AuthClient


class Client(AuthClient):
    @staticmethod
    def __stringify_list(data: list[str]) -> str:
        return str(data).replace("'", '"')

    @staticmethod
    def __validate_response_data(data: dict[Any, Any]) -> None:
        for it in data.items():
            content = it[1]

            if content.get("ok") is False:
                raise ApiException(content.get("error"))

    @staticmethod
    def __normalize_tag(tag: str) -> str:
        return f'#{tag.replace("#", "").upper()}'

    def send_friend_request(self, player_tag: str) -> Any:
        return self.send_friend_requests([player_tag])

    def send_friend_requests(self, player_tags: list[str]) -> Any:
        key = "appAccounts"
        normalized_tags = [self.__normalize_tag(tag) for tag in player_tags]
        friend_data = {key: self.__stringify_list(normalized_tags)}
        content = self._request.post(
            "social/v3/friends.createRequest", friend_data, self._auth.get_token()
        )
        self.__validate_response_data(content.get(key, {}))

        return content
