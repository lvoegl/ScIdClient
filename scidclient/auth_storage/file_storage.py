import json
import os

from models.auth import Auth

from .storage_provider import StorageProvider


class FileStorage(StorageProvider):
    __EMAIL_KEY = "email"
    __TOKEN_KEY = "token"

    def __init__(self, file_name: str):
        self.__file_name = file_name

    def load(self) -> Auth | None:
        if not os.path.isfile(self.__file_name):
            return None

        with open(self.__file_name) as auth_file:
            auth = auth_file.read()

        auth_json = json.loads(auth)
        email = auth_json.get(FileStorage.__EMAIL_KEY)
        token = auth_json.get(FileStorage.__TOKEN_KEY)

        return Auth(email, token)

    def store(self, auth: Auth) -> None:
        auth_json_str = json.dumps(
            {FileStorage.__EMAIL_KEY: auth.get_email(), FileStorage.__TOKEN_KEY: auth.get_token()}
        )

        with open(self.__file_name, "w") as auth_file:
            auth_file.write(auth_json_str)
