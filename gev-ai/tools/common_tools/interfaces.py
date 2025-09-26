from abc import ABC, abstractmethod


class SystemInfoInterface(ABC):
    @abstractmethod
    def get_fastfetch_specs(self) -> str | None:
        pass

    @abstractmethod
    def get_neofetch_specs(self) -> str | None:
        pass
