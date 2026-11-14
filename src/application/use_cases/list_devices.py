from typing import List

from src.domain.entities.device import Device
from src.domain.interfaces.device_repository import IDeviceRepository


class ListDevicesUseCase:
    def __init__(self, repository: IDeviceRepository) -> None:
        self._repository = repository

    def execute(self) -> List[Device]:
        return self._repository.get_all()