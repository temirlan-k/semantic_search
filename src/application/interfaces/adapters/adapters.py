

from abc import ABC, abstractmethod


class IAdapter(ABC):

    @abstractmethod
    async def close(self) -> None:
        pass

