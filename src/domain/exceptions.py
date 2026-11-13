"""Доменні винятки: помилки бізнес-правил, не прив’язані до БД чи інтерфейсу."""
class DomainError(Exception):
    """Базовий клас для всіх помилок предметної області."""
class DuplicateDeviceError(DomainError):
    """Пристрій із таким інвентарним номером уже існує."""
class DeviceNotFoundError(DomainError):
    """Пристрій із таким інвентарним номером не знайдено."""
class DeviceNotAvailableError(DomainError):
    """Пристрій неможливо видати: він уже виданий."""
class DeviceNotIssuedError(DomainError):
    """Пристрій неможливо повернути: він не був виданий."""