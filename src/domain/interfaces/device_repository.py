from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.device import Device


class IDeviceRepository(ABC):
    """Контракт сховища пристроїв. Реалізації живуть в Infrastructure."""

    @abstractmethod
    def add(self, device: Device) -> None:
        ...

    @abstractmethod
    def get_by_inventory_number(self, inventory_number: str) -> Optional[Device]:
        ...

    @abstractmethod
    def get_all(self) -> List[Device]:
        ...

    @abstractmethod
    def update(self, device: Device) -> None:
        ...