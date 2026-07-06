"""Validacion de entrada con patron Strategy."""

from abc import ABC, abstractmethod
from typing import Optional


class ValidationError(Exception):
    pass


class Validator(ABC):
    @abstractmethod
    def validate(self, value: str) -> str:
        ...


class RucValidator(Validator):
    def validate(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned.isdigit():
            raise ValidationError("El RUC debe contener solo numeros.")
        if len(cleaned) != 11:
            raise ValidationError(f"El RUC debe tener 11 digitos (ingresaste {len(cleaned)}).")
        return cleaned


class DniValidator(Validator):
    def validate(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned.isdigit():
            raise ValidationError("El DNI debe contener solo numeros.")
        if len(cleaned) != 8:
            raise ValidationError(f"El DNI debe tener 8 digitos (ingresaste {len(cleaned)}).")
        return cleaned


class NombreValidator(Validator):
    def validate(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValidationError("El nombre no puede estar vacio.")
        return cleaned


class NonEmptyValidator(Validator):
    def validate(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValidationError("El valor no puede estar vacio.")
        return cleaned


class ValidatorEngine:
    def __init__(self):
        self._validators: dict[str, Validator] = {}

    def register(self, name: str, validator: Validator):
        self._validators[name] = validator

    def validate(self, name: str, value: str) -> str:
        validator = self._validators.get(name)
        if not validator:
            return value.strip()
        return validator.validate(value)
