from typing import List

from src.domain.entities.device import Device, DeviceStatus
from src.domain.interfaces.device_repository import IDeviceRepository


class ListDevicesUseCase:
    def __init__(self, repository: IDeviceRepository) -> None:
        self._repository = repository

    def execute(self, only_available: bool = False) -> List[Device]:
        devices = self._repository.get_all()
        if only_available:
            return [d for d in devices if d.status == DeviceStatus.AVAILABLE]
        return devices