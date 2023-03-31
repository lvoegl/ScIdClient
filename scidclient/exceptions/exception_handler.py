from exceptions.api_exception import ApiException
from exceptions.specific.invalid_pin_exception import InvalidPinException
from exceptions.specific.unauthorized_exception import UnauthorizedException


class ExceptionHandler:
    EXCEPTION_MAPPING = {
        "incorrect_pin": InvalidPinException,
        "unauthorized": UnauthorizedException,
    }

    @staticmethod
    def get_exception(error: str) -> type[ApiException] | None:
        return ExceptionHandler.EXCEPTION_MAPPING.get(error)
