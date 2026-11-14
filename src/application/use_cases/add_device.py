from src.domain.entities.device import Device
from src.domain.exceptions import DuplicateDeviceError
from src.domain.interfaces.device_repository import IDeviceRepository


class AddDeviceUseCase:
    def __init__(self, repository: IDeviceRepository) -> None:
        self._repository = repository

    def execute(self, inventory_number: str, name: str, location: str) -> Device:
        inventory_number = inventory_number.strip()
        name = name.strip()
        if not inventory_number or not name:
            raise ValueError("Інвентарний номер і назва є обов’язковими")
        if self._repository.get_by_inventory_number(inventory_number) is not None:
            raise DuplicateDeviceError(
                f"Пристрій з номером {inventory_number} уже існує"
            )
        device = Device(
            inventory_number=inventory_number,
            name=name,
            location=location.strip(),
        )
        self._repository.add(device)
        return device