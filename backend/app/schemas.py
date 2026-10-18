from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

REGIONS = [
    "Toshkent shahri", "Toshkent viloyati", "Samarqand viloyati", "Buxoro viloyati",
    "Andijon viloyati", "Farg‘ona viloyati", "Namangan viloyati", "Qashqadaryo viloyati",
    "Surxondaryo viloyati", "Jizzax viloyati", "Sirdaryo viloyati", "Navoiy viloyati",
    "Xorazm viloyati", "Qoraqalpog‘iston Respublikasi"
]

class TripCreate(BaseModel):
    driver_user_id: int = Field(gt=0)
    origin_region: str
    destination_region: str
    origin_address: str = Field(min_length=3, max_length=240)
    destination_address: str = Field(min_length=3, max_length=240)
    departure_at: datetime
    seats_available: int = Field(ge=1, le=8)
    price_uzs: Decimal = Field(gt=0, max_digits=14, decimal_places=0)
    car_make_model: str = Field(min_length=2, max_length=120)
    note: str | None = Field(default=None, max_length=1000)
    return_trip: bool = False

class TripOut(BaseModel):
    id: int
    driver_user_id: int
    origin_region: str
    destination_region: str
    origin_address: str
    destination_address: str
    departure_at: datetime
    seats_available: int
    price_uzs: Decimal
    car_make_model: str
    note: str | None
    return_trip: bool
    status: str
    model_config = ConfigDict(from_attributes=True)
