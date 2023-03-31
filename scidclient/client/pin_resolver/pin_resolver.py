from abc import ABC, abstractmethod


class PinResolver(ABC):
    @abstractmethod
    def get_pin(self, email: str) -> int:
        pass
