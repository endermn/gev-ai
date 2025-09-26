from abc import ABC, abstractmethod

# from typing import Any


class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    # -- INFO: static type checker doesn't accept kwargs the way it's supposed to?
    # @abstractmethod
    # def execute(self, **kwargs) -> Any:
    #     pass
