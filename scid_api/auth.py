import json
from datetime import datetime

import jwt

from scid_api.exceptions import AuthException


class ScIdAuth:
    JWT_KEY = 'scidToken'
    MAIL_KEY = 'email'

    def __init__(self, json_data: dict):
        self.__mail = json_data.get(ScIdAuth.MAIL_KEY, None)
        self.__token = json_data.get(ScIdAuth.JWT_KEY, None)

        if self.__mail is None or self.__token is None:
            raise AuthException('malformed authentication data')

        token_data = jwt.decode(self.__token, options={
                                'verify_signature': False})
        self.__expires = datetime.fromtimestamp(token_data.get('exp', 0))

    def get_token(self):
        return self.__token

    def get_mail(self):
        return self.__mail

    def has_expired(self):
        now = datetime.now()
        return now > self.__expires

    def json_dump(self):
        return json.dumps({
            ScIdAuth.MAIL_KEY: self.get_mail(),
            ScIdAuth.JWT_KEY: self.get_token()
        })
