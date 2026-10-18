from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import String, Integer, DateTime, Boolean, Numeric, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

def now_utc():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(160))
    phone: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
    telegram_id: Mapped[int | None] = mapped_column(unique=True, nullable=True)
    role: Mapped[str] = mapped_column(String(20), default="passenger")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)

class DriverProfile(Base):
    __tablename__ = "driver_profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    car_make_model: Mapped[str] = mapped_column(String(120))
    plate_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    seats: Mapped[int] = mapped_column(Integer, default=4)
    verification_status: Mapped[str] = mapped_column(String(24), default="pending")
    trial_started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    subscription_active: Mapped[bool] = mapped_column(Boolean, default=False)

class Trip(Base):
    __tablename__ = "trips"
    id: Mapped[int] = mapped_column(primary_key=True)
    driver_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    origin_region: Mapped[str] = mapped_column(String(80), index=True)
    destination_region: Mapped[str] = mapped_column(String(80), index=True)
    origin_address: Mapped[str] = mapped_column(String(240))
    destination_address: Mapped[str] = mapped_column(String(240))
    departure_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    seats_available: Mapped[int] = mapped_column(Integer)
    price_uzs: Mapped[Decimal] = mapped_column(Numeric(14, 0))
    car_make_model: Mapped[str] = mapped_column(String(120))
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    return_trip: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="published")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    __table_args__ = (Index("ix_trip_route_departure", "origin_region", "destination_region", "departure_at"),)
