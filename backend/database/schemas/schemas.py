from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class ThermometerSchema(BaseModel):
    name: str
    vendor: str
    category: str
    min_temp: float
    max_temp: float
    accuracy: float


class PropertySchema(BaseModel):
    name: str
    units: str


class CategorySchema(BaseModel):
    name: str
