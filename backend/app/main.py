from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import Base, engine, get_db
from .models import Trip, User, DriverProfile
from .schemas import TripCreate, TripOut, REGIONS
from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Convenience for local MVP. Use Alembic migrations for production deployments.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Viloyatga Boramiz API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_origin, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/regions")
async def regions():
    return {"regions": REGIONS}

@app.get("/api/trips", response_model=list[TripOut])
async def search_trips(
    origin: str | None = None,
    destination: str | None = None,
    date_from: datetime | None = None,
    seats: int = Query(default=1, ge=1, le=8),
    max_price: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Trip).where(Trip.status == "published", Trip.seats_available >= seats)
    if origin:
        stmt = stmt.where(Trip.origin_region == origin)
    if destination:
        stmt = stmt.where(Trip.destination_region == destination)
    if date_from:
        start = date_from.replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = stmt.where(Trip.departure_at >= start, Trip.departure_at < start + timedelta(days=1))
    if max_price is not None:
        stmt = stmt.where(Trip.price_uzs <= max_price)
    stmt = stmt.order_by(Trip.departure_at.asc()).limit(100)
    return list((await db.scalars(stmt)).all())

@app.post("/api/trips", response_model=TripOut, status_code=201)
async def create_trip(payload: TripCreate, db: AsyncSession = Depends(get_db)):
    if payload.origin_region not in REGIONS or payload.destination_region not in REGIONS:
        raise HTTPException(422, "Hududlar ro‘yxatidan tanlang.")
    if payload.origin_region == payload.destination_region:
        raise HTTPException(422, "Jo‘nash va borish hududlari turlicha bo‘lishi kerak.")
    if payload.departure_at <= datetime.now(timezone.utc):
        raise HTTPException(422, "Jo‘nash vaqti kelajakda bo‘lishi kerak.")
    driver = await db.scalar(select(DriverProfile).where(DriverProfile.user_id == payload.driver_user_id))
    if driver is None:
        raise HTTPException(403, "Avval haydovchi profilini yarating.")
    trial_end = driver.trial_started_at + timedelta(days=settings.trial_days)
    if not driver.subscription_active and datetime.now(timezone.utc) >= trial_end:
        raise HTTPException(402, "Bepul muddat tugagan. Safar e’lon qilish uchun obunani faollashtiring.")
    trip = Trip(**payload.model_dump())
    db.add(trip)
    await db.commit()
    await db.refresh(trip)
    return trip

@app.patch("/api/trips/{trip_id}", response_model=TripOut)
async def update_trip(trip_id: int, driver_user_id: int, payload: TripCreate, db: AsyncSession = Depends(get_db)):
    trip = await db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(404, "Safar topilmadi.")
    if trip.driver_user_id != driver_user_id:
        raise HTTPException(403, "Bu safarni tahrirlash huquqi yo‘q.")
    for key, value in payload.model_dump().items():
        if key != "driver_user_id":
            setattr(trip, key, value)
    await db.commit()
    await db.refresh(trip)
    return trip

@app.delete("/api/trips/{trip_id}")
async def cancel_trip(trip_id: int, driver_user_id: int, db: AsyncSession = Depends(get_db)):
    trip = await db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(404, "Safar topilmadi.")
    if trip.driver_user_id != driver_user_id:
        raise HTTPException(403, "Bu safarni bekor qilish huquqi yo‘q.")
    trip.status = "cancelled"
    await db.commit()
    return {"ok": True, "message": "Safar bekor qilindi."}
