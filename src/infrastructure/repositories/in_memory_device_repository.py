from typing import Dict, List, Optional

from src.domain.entities.device import Device
from src.domain.interfaces.device_repository import IDeviceRepository


class InMemoryDeviceRepository(IDeviceRepository):
    """Зберігає пристрої в оперативній пам’яті (дані зникають після виходу)."""

    def __init__(self) -> None:
        self._items: Dict[str, Device] = {}

    def add(self, device: Device) -> None:
        self._items[device.inventory_number] = device

    def get_by_inventory_number(self, inventory_number: str) -> Optional[Device]:
        return self._items.get(inventory_number)

    def get_all(self) -> List[Device]:
        return list(self._items.values())

    def update(self, device: Device) -> None:
        self._items[device.inventory_number] = device