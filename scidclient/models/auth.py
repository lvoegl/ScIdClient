class Auth:
    def __init__(self, email: str, token: str):
        self.__email = email
        self.__token = token

    def get_token(self) -> str:
        return self.__token

    def set_token(self, token: str) -> None:
        self.__token = token

    def get_email(self) -> str:
        return self.__email
