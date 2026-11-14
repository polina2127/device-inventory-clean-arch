import json
from pathlib import Path

from src.application.use_cases.add_device import AddDeviceUseCase
from src.application.use_cases.issue_device import IssueDeviceUseCase
from src.application.use_cases.list_devices import ListDevicesUseCase
from src.application.use_cases.return_device import ReturnDeviceUseCase
from src.domain.entities.device import Device, DeviceStatus
from src.domain.exceptions import DomainError
from src.domain.interfaces.device_repository import IDeviceRepository
from src.infrastructure.repositories.in_memory_device_repository import (
    InMemoryDeviceRepository,
)
from src.infrastructure.repositories.json_device_repository import (
    JsonDeviceRepository,
)

ROOT_DIR = Path(__file__).resolve().parents[3]


def load_settings() -> dict:
    with open(ROOT_DIR / "appsettings.json", "r", encoding="utf-8") as file:
        return json.load(file)


def build_repository(settings: dict) -> IDeviceRepository:
    """Єдине місце, де вибирається конкретна реалізація сховища."""
    storage = settings["storage"]
    if storage["type"] == "memory":
        return InMemoryDeviceRepository()
    if storage["type"] == "json":
        return JsonDeviceRepository(ROOT_DIR / storage["path"])
    raise ValueError(f"Невідомий тип сховища: {storage['type']}")


def print_device(device: Device) -> None:
    if device.status == DeviceStatus.AVAILABLE:
        status = "вільний"
    else:
        status = f"виданий ({device.holder})"
    print(f"  [{device.inventory_number}] {device.name} | {device.location} | {status}")


def main() -> None:
    # Dependency Injection: збираємо залежності в одному місці
    repository = build_repository(load_settings())
    add_device = AddDeviceUseCase(repository)
    list_devices = ListDevicesUseCase(repository)
    issue_device = IssueDeviceUseCase(repository)
    return_device = ReturnDeviceUseCase(repository)

    while True:
        print("\n=== Облік обладнання комп’ютерної лабораторії ===")
        print("1. Додати пристрій")
        print("2. Показати всі пристрої")
        print("3. Показати лише вільні пристрої")
        print("4. Видати пристрій")
        print("5. Повернути пристрій")
        print("0. Вийти")
        choice = input("Ваш вибір: ").strip()

        try:
            if choice == "1":
                device = add_device.execute(
                    input("Інвентарний номер: "),
                    input("Назва: "),
                    input("Розташування (кабінет): "),
                )
                print("Додано:")
                print_device(device)
            elif choice == "2":
                devices = list_devices.execute()
                print("Усі пристрої:" if devices else "Список порожній.")
                for device in devices:
                    print_device(device)
            elif choice == "3":
                devices = list_devices.execute(only_available=True)
                print("Вільні пристрої:" if devices else "Вільних пристроїв немає.")
                for device in devices:
                    print_device(device)
            elif choice == "4":
                device = issue_device.execute(
                    input("Інвентарний номер: "),
                    input("Кому видати (ПІБ): "),
                )
                print("Видано:")
                print_device(device)
            elif choice == "5":
                device = return_device.execute(input("Інвентарний номер: "))
                print("Повернено:")
                print_device(device)
            elif choice == "0":
                print("До побачення!")
                break
            else:                                                       
                print("Невідомий пункт меню. Введіть число від 0 до 5.") 
        except (DomainError, ValueError) as error:


if __name__ == "__main__":
    main()