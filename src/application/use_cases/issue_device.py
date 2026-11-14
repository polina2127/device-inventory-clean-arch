from src.domain.entities.device import Device
from src.domain.exceptions import DeviceNotFoundError
from src.domain.interfaces.device_repository import IDeviceRepository


class IssueDeviceUseCase:
    def __init__(self, repository: IDeviceRepository) -> None:
        self._repository = repository

    def execute(self, inventory_number: str, person: str) -> Device:
        device = self._repository.get_by_inventory_number(inventory_number.strip())
        if device is None:
            raise DeviceNotFoundError(f"Пристрій {inventory_number} не знайдено")
        device.issue_to(person)
        self._repository.update(device)
        return device