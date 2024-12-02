from dataclasses import dataclass


@dataclass
class ValidDataClass:
    user_code: str
    name: str


@dataclass
class InvalidDataClass1:
    user_code: int
    name: str


@dataclass
class InvalidDataClass2:
    custom_user_code: int
    name: str
