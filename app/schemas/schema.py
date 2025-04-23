from typing import List, Tuple
from pydantic import BaseModel, Field


class Flight(BaseModel):
    start_date: str
    from_: str = Field(..., alias="from")
    to: str
    airline: str
    class_: str = Field(..., alias="class")
    check_in_luggage: bool = Field(..., alias="check-in luggage")
    price: int


class Hotel(BaseModel):
    name: str
    price: int
    rating: float
    start_date: str
    end_date: str


class DayHotel(BaseModel):
    name: str


class DaySchedule(BaseModel):
    date: str
    schedule: List[Tuple[str, str]]
    hotel: DayHotel


class ItineraryPlan(BaseModel):
    title: str
    highlights: List[str]
    total_cost: int
    avg_per_day: float
    hotels: List[Hotel]
    flights: List[Flight]
    details: List[DaySchedule]
