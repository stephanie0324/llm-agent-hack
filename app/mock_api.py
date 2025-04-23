from typing import List, TypedDict


class DaySchedule(TypedDict):
    day: int
    schedule: List[tuple[str, str]]


class ItineraryPlan(TypedDict):
    title: str
    highlights: List[str]
    total_cost: int
    avg_per_day: float
    details: List[DaySchedule]


def get_mock_itineraries() -> List[ItineraryPlan]:
    """
    返回模擬的旅遊行程資料
    """
    return [
        {
            "title": "Gastronomic Tokyo Adventure",
            "highlights": [
                "Explore Senso-ji Temple",
                "Enjoy traditional Japanese breakfast",
                "Savor tempura and kaiseki-style dinner",
                "Relax along Sumida River",
                "Visit Meiji Jingu Shrine",
            ],
            "total_cost": 10000,
            "avg_per_day": 2500,
            "hotels": [
                {
                    "name": "Hotel Okura Tokyo",
                    "price": 5500,
                    "rating": 4.5,
                    "start_date": "2025/05/01",
                    "end_date": "2025/05/02",
                },
                {
                    "name": "Hotel Sakura Tokyo",
                    "price": 4500,
                    "rating": 4.5,
                    "start_date": "2025/05/02",
                    "end_date": "2025/05/03",
                },
            ],
            "details": [
                {
                    "date": "2025/05/01",
                    "schedule": [
                        ("09:00", "Arrive in Tokyo"),
                        ("11:00", "Explore Senso-ji Temple"),
                        ("13:00", "Traditional Japanese breakfast"),
                    ],
                    "hotel": {
                        "name": "Hotel Okura Tokyo",
                    },
                },
                {
                    "date": "2025/05/02",
                    "schedule": [
                        ("10:00", "Relax along Sumida River"),
                        ("19:00", "Kaiseki-style dinner"),
                    ],
                    "hotel": {
                        "name": "Hotel Sakura Tokyo",
                    },
                },
                {
                    "date": "2025/05/03",
                    "schedule": [
                        ("11:00", "Visit Meiji Jingu Shrine"),
                        ("15:00", "Shopping in Harajuku"),
                        ("18:00", "Back to hotel"),
                    ],
                    "hotel": {
                        "name": "Hotel Okura Tokyo",
                    },
                },
            ],
        },
        {
            "title": "Romance in Tokyo",
            "highlights": [
                "Visit Senso-ji and Tokyo Skytree",
                "Explore Shinjuku Gyoen's Gardens",
                "Dine at Omoide Yokocho",
                "Relax in Akihabara",
                "Enjoy a dinner cruise in Tokyo Bay",
            ],
            "total_cost": 10000,
            "avg_per_day": 2500,
            "hotels": [
                {
                    "name": "Park Hotel Tokyo",
                    "price": 5000,
                    "rating": 4.6,
                    "start_date": "2025/05/01",
                    "end_date": "2025/05/02",
                },
                {
                    "name": "Hotel Ryumeikan Tokyo",
                    "price": 5000,
                    "rating": 4.7,
                    "start_date": "2025/05/02",
                    "end_date": "2025/05/03",
                },
            ],
            "details": [
                {
                    "date": "2025/05/01",
                    "schedule": [
                        ("10:00", "Visit Senso-ji & Tokyo Skytree"),
                        ("14:00", "Stroll around Asakusa"),
                        ("17:00", "Dinner at Omoide Yokocho"),
                    ],
                    "hotel": {
                        "name": "Park Hotel Tokyo",
                    },
                },
                {
                    "date": "2025/05/02",
                    "schedule": [
                        ("11:00", "Relaxing walk at Shinjuku Gyoen National Garden"),
                        ("14:00", "Explore tech and pop culture in Akihabara"),
                        ("17:30", "Shopping at Shibuya Crossing"),
                    ],
                    "hotel": {
                        "name": "Hotel Ryumeikan Tokyo",
                    },
                },
                {
                    "date": "2025/05/03",
                    "schedule": [
                        ("13:00", "Leisure time at Odaiba Seaside Park"),
                        ("17:30", "Dinner cruise in Tokyo Bay"),
                    ],
                    "hotel": {
                        "name": "Hotel Ryumeikan Tokyo",
                    },
                },
            ],
        },
        {
            "title": "Tokyo's Off-the-Beaten-Track Luxury",
            "highlights": [
                "Explore Yanaka Ginza old-town charm",
                "Savor sushi dining at Sukiyabashi Jiro",
                "Visit Mori Art Museum",
                "Enjoy Afternoon Tea at Andaz Tokyo",
                "Relax at a luxury onsen",
            ],
            "total_cost": 10000,
            "avg_per_day": 2500,
            "hotels": [
                {
                    "name": "Andaz Tokyo - a Concept by Hyatt",
                    "price": 6000,
                    "rating": 4.8,
                    "start_date": "2025/05/01",
                    "end_date": "2025/05/02",
                },
                {
                    "name": "Hoshinoya Tokyo",
                    "price": 4000,
                    "rating": 4.9,
                    "start_date": "2025/05/02",
                    "end_date": "2025/05/03",
                },
            ],
            "details": [
                {
                    "date": "2025/05/01",
                    "schedule": [
                        ("09:00", "Walk through nostalgic streets of Yanaka Ginza"),
                        ("14:00", "Discover artisan shops and hidden tea houses"),
                        ("18:00", "Luxury sushi dining at Sukiyabashi Jiro"),
                    ],
                    "hotel": {
                        "name": "Andaz Tokyo - a Concept by Hyatt",
                    },
                },
                {
                    "date": "2025/05/02",
                    "schedule": [
                        ("10:00", "Visit Mori Art Museum & Roppongi Hills"),
                        ("15:00", "Afternoon Tea with Tokyo Tower view at Andaz"),
                    ],
                    "hotel": {
                        "name": "Hoshinoya Tokyo",
                    },
                },
                {
                    "date": "2025/05/03",
                    "schedule": [
                        ("11:00", "Rejuvenate at a luxury onsen experience"),
                        ("16:00", "Souvenir shopping in Nihonbashi"),
                    ],
                    "hotel": {
                        "name": "Hoshinoya Tokyo",
                    },
                },
            ],
        },
    ]
