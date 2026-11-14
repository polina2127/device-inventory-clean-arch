import json
from pathlib import Path
from typing import List, Optional

from src.domain.entities.device import Device, DeviceStatus
from src.domain.interfaces.device_repository import IDeviceRepository


class JsonDeviceRepository(IDeviceRepository):
    """Зберігає пристрої у JSON-файлі (дані лишаються між запусками)."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = Path(file_path)

    def add(self, device: Device) -> None:
        devices = self._load()
        devices.append(device)
        self._save(devices)

    def get_by_inventory_number(self, inventory_number: str) -> Optional[Device]:
        for device in self._load():
            if device.inventory_number == inventory_number:
                return device
        return None

    def get_all(self) -> List[Device]:
        return self._load()

    def update(self, device: Device) -> None:
        devices = self._load()
        for index, item in enumerate(devices):
            if item.inventory_number == device.inventory_number:
                devices[index] = device
                break
        self._save(devices)

    def _load(self) -> List[Device]:
        if not self._file_path.exists():
            return []
        with open(self._file_path, "r", encoding="utf-8") as file:
            raw_items = json.load(file)
        return [
            Device(
                inventory_number=item["inventory_number"],
                name=item["name"],
                location=item["location"],
                status=DeviceStatus(item["status"]),
                holder=item["holder"],
            )
            for item in raw_items
        ]

    def _save(self, devices: List[Device]) -> None:
        raw_items = [
            {
                "inventory_number": d.inventory_number,
                "name": d.name,
                "location": d.location,
                "status": d.status.value,
                "holder": d.holder,
            }
            for d in devices
        ]
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(raw_items, file, ensure_ascii=False, indent=2)