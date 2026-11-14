from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.domain.exceptions import DeviceNotAvailableError, DeviceNotIssuedError


class DeviceStatus(str, Enum):
    AVAILABLE = "available"  # лежить у лабораторії, можна видати
    ISSUED = "issued"        # виданий конкретній особі


@dataclass
class Device:
    """Сутність «Пристрій»: інвентарний номер, назва, розташування, статус, власник."""
    inventory_number: str
    name: str
    location: str
    status: DeviceStatus = DeviceStatus.AVAILABLE
    holder: Optional[str] = None

    def issue_to(self, person: str) -> None:
        """Видати пристрій особі. Бізнес-правило: видати можна лише вільний пристрій."""
        if self.status != DeviceStatus.AVAILABLE:
            raise DeviceNotAvailableError(
                f"Пристрій {self.inventory_number} уже виданий: {self.holder}"
            )
        person = person.strip()
        if not person:
            raise ValueError("Вкажіть, кому видається пристрій")
        self.status = DeviceStatus.ISSUED
        self.holder = person

    def return_back(self) -> None:
        """Повернути пристрій. Бізнес-правило: повернути можна лише виданий пристрій."""
        if self.status != DeviceStatus.ISSUED:
            raise DeviceNotIssuedError(
                f"Пристрій {self.inventory_number} не був виданий"
            )
        self.status = DeviceStatus.AVAILABLE
        self.holder = None