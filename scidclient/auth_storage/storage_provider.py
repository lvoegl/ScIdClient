from abc import ABC, abstractmethod

from models.auth import Auth


class StorageProvider(ABC):
    @abstractmethod
    def load(self) -> Auth | None:
        pass

    @abstractmethod
    def store(self, auth: Auth) -> None:
        pass
