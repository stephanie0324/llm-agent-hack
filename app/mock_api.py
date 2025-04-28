import json
import random
from typing import List, TypedDict


class DaySchedule(TypedDict):
    day: int
    schedule: List[dict]


class ItineraryPlan(TypedDict):
    title: str
    highlights: List[str]
    total_cost: int
    avg_per_day: float
    details: List[DaySchedule]


def get_mock_itineraries() -> List[ItineraryPlan]:
    """
    Return mock travel itinerary data
    """
    return [
        {
            "title": "Gastronomic Exploration & Urban Serenity",
            "highlights": [
                "Traditional Japanese cuisine",
                "Tea ceremony experience",
                "Day trip to Nikko",
            ],
            "total_cost": 4500,
            "currency": "USD",
            "avg_per_day": 1500.0,
            "hotels": [
                {
                    "name": "Park Hyatt Tokyo",
                    "price": 800,
                    "rating": 4.9,
                    "start_date": "2025-05-28",
                    "end_date": "2025-05-31",
                    "booking_link": "https://www.hyatt.com/en-US/hotel/japan/park-hyatt-tokyo",
                }
            ],
            "flights": [
                {
                    "start_date": "2025-05-27",
                    "from": "San Francisco International Airport (SFO)",
                    "to": "Narita International Airport (NRT)",
                    "airline": "ANA",
                    "class": "Business",
                    "check-in luggage": True,
                    "price": 1500,
                    "booking_link": "https://www.ana.co.jp/en/us/",
                }
            ],
            "details": [
                {
                    "date": "2025-05-28",
                    "schedule": [
                        {
                            "start_time": "08:30",
                            "end_time": "10:00",
                            "activity": "Omakase Breakfast at Tsukiji Fish Market",
                            "description": "Start your day with a luxurious sushi breakfast at Tsukiji Fish Market, recommended is Sushi Maruyama - fresh and expertly crafted.",
                        },
                        {
                            "start_time": "10:30",
                            "end_time": "12:30",
                            "activity": "Hamarikyu Gardens Exploration",
                            "description": "Enjoy tranquil Japanese landscaping at Hamarikyu Gardens. A perfect spot for photography and relaxation.",
                        },
                        {
                            "start_time": "13:00",
                            "end_time": "14:30",
                            "activity": "Udon Noodles Lunch at Shin Udon",
                            "description": "Try flavorful handmade udon in Tokyo, highly praised by locals and tourists alike.",
                        },
                        {
                            "start_time": "15:00",
                            "end_time": "17:00",
                            "activity": "Tea Ceremony at Tokyo National Museum",
                            "description": "Immerse in Japanese culture with a traditional tea ceremony. The museum also showcases stunning art collections.",
                        },
                        {
                            "start_time": "19:00",
                            "end_time": "21:00",
                            "activity": "Kaiseki Dining at Kagurazaka Ishikawa",
                            "description": "Indulge in a Michelin-star kaiseki meal at Kagurazaka Ishikawa, offering beautifully crafted multi-course Japanese fine dining.",
                        },
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
                {
                    "date": "2025-05-29",
                    "schedule": [
                        {
                            "start_time": "08:00",
                            "end_time": "09:30",
                            "activity": "Pancakes at bills Omotesando",
                            "description": "Savor fluffy pancakes at a stylish caf\u00e9 perfect for a comforting breakfast.",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "12:30",
                            "activity": "Shopping at Harajuku\u2019s Takeshita Street & Omotesando",
                            "description": "Discover quirky and luxury items while enjoying trendy vibes and Japanese street fashion.",
                        },
                        {
                            "start_time": "13:00",
                            "end_time": "14:30",
                            "activity": "Tonkatsu Lunch at Maisen Omotesando",
                            "description": "Enjoy breaded pork cutlet served crispy but tender, a hallmark of Japanese cuisine.",
                        },
                        {
                            "start_time": "15:00",
                            "end_time": "17:00",
                            "activity": "teamLab Borderless Museum Visit",
                            "description": "Explore an iconic digital art experience in Tokyo. Timely reservations recommended.",
                        },
                        {
                            "start_time": "19:00",
                            "end_time": "21:30",
                            "activity": "Dinner at New York Grill",
                            "description": "High-end dining with stunning city views, located in Shinjuku. A perfect evening finale.",
                        },
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
                {
                    "date": "2025-05-30",
                    "schedule": [
                        {
                            "start_time": "07:30",
                            "end_time": "09:30",
                            "activity": "Breakfast at About Life Coffee Brewers in Shibuya",
                            "description": "A cozy caf\u00e9 offering premium coffee and freshly baked goods for a delightful morning.",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "15:00",
                            "activity": "Nikko Day Trip (Toshogu Shrine & Kegon Falls)",
                            "description": "Explore Nikko's heritage at Toshogu Shrine and marvel at the natural beauty of Kegon Falls.",
                        },
                        {
                            "start_time": "13:00",
                            "end_time": "14:30",
                            "activity": "Lunch at Kanaya Hotel Restaurant, Nikko",
                            "description": "Relish yuba, a local tofu skin specialty, paired perfectly with local delicacies.",
                        },
                        {
                            "start_time": "18:00",
                            "end_time": "20:00",
                            "activity": "Dinner at Sushi Saito",
                            "description": "End your Tokyo adventure with an exquisite sushi experience at this highly-rated restaurant.",
                        },
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
            ],
        },
        {
            "title": "Luxury and Relaxation",
            "highlights": [
                "Luxury dining experiences",
                "Roppongi exhibits",
                "Shibuya Sky views",
            ],
            "total_cost": 4000,
            "currency": "USD",
            "avg_per_day": 1333.33,
            "hotels": [
                {
                    "name": "The Ritz-Carlton Tokyo",
                    "price": 1200,
                    "rating": 5.0,
                    "start_date": "2025-05-28",
                    "end_date": "2025-05-31",
                    "booking_link": "https://www.ritzcarlton.com/en/hotels/japan/tokyo",
                }
            ],
            "flights": [
                {
                    "start_date": "2025-05-27",
                    "from": "John F. Kennedy International Airport (JFK)",
                    "to": "Tokyo Haneda Airport (HND)",
                    "airline": "Japan Airlines",
                    "class": "First",
                    "check-in luggage": True,
                    "price": 1700,
                    "booking_link": "https://www.jal.co.jp/en/",
                }
            ],
            "details": [
                {
                    "date": "2025-05-28",
                    "schedule": [
                        {
                            "start_time": "08:30",
                            "end_time": "10:00",
                            "activity": "Japanese Breakfast at Chaya Macrobiotics Tokyo Midtown",
                            "description": "Healthy Japanese meals to energize your day within a modern setting.",
                        }
                    ],
                    "hotel": {"name": "The Ritz-Carlton Tokyo"},
                }
            ],
        },
        {
            "title": "Hidden Gems & Local Meets",
            "highlights": [
                "Rustic charm in Yanaka Ginza",
                "Matcha experiences",
                "Asakusa exploration",
            ],
            "total_cost": 3500,
            "currency": "USD",
            "avg_per_day": 1166.67,
            "hotels": [
                {
                    "name": "Mandarin Oriental Tokyo",
                    "price": 1000,
                    "rating": 4.8,
                    "start_date": "2025-05-28",
                    "end_date": "2025-05-31",
                    "booking_link": "https://www.mandarinoriental.com/tokyo",
                }
            ],
            "flights": [
                {
                    "start_date": "2025-05-27",
                    "from": "Los Angeles International Airport (LAX)",
                    "to": "Narita International Airport (NRT)",
                    "airline": "United Airlines",
                    "class": "Premium Economy",
                    "check-in luggage": True,
                    "price": 1200,
                    "booking_link": "https://www.united.com/en/us/",
                }
            ],
            "details": [
                {
                    "date": "2025-05-28",
                    "schedule": [
                        {
                            "start_time": "08:30",
                            "end_time": "10:00",
                            "activity": "Taiyaki breakfast at Naniwa Taiyaki in Kagurazaka",
                            "description": "Savor delightful fish-shaped cakes stuffed with sweet fillings, ideal for a relaxed start.",
                        }
                    ],
                    "hotel": {"name": "Mandarin Oriental Tokyo"},
                }
            ],
        },
    ]


def get_mock_modified_itinerary(
    original_plan, selected_activities, modification_instruction
):
    """Mock function to simulate itinerary modification"""
    # Create a deep copy of the original plan
    modified_plan = json.loads(json.dumps(original_plan))

    # Random activity options with descriptions
    random_activities = [
        {
            "activity": "Visit Tokyo Skytree",
            "description": "Experience breathtaking views from Japan's tallest structure, standing at 634 meters. Visit the observation decks for panoramic views of Tokyo, and explore the modern shopping complex at its base.",
        },
        {
            "activity": "Shopping at Shibuya 109",
            "description": "Explore the trendy fashion mecca of Tokyo, featuring over 100 boutiques across 10 floors. Experience the heart of Japanese youth fashion culture and latest trends in this iconic shopping destination.",
        },
        {
            "activity": "Explore Akihabara",
            "description": "Discover Japan's electronics and anime culture center, filled with gaming arcades, manga stores, and electronics shops. Experience the unique otaku culture and find the latest technology and anime merchandise.",
        },
        {
            "activity": "Visit Ueno Park",
            "description": "Stroll through one of Tokyo's largest public parks, home to major museums, zoo, and beautiful seasonal flowers. Enjoy street performances and local festivals while experiencing the cultural heart of Tokyo.",
        },
        {
            "activity": "Tea Ceremony Experience",
            "description": "Learn about traditional Japanese tea culture through an authentic tea ceremony. Experience the precise rituals, taste matcha green tea, and learn about the philosophy of harmony and respect.",
        },
        {
            "activity": "Karaoke Session",
            "description": "Enjoy a fun karaoke session in the heart of Tokyo at a premium karaoke chain. Experience this beloved Japanese pastime in a private room with state-of-the-art equipment and extensive song selection.",
        },
        {
            "activity": "Visit Ghibli Museum",
            "description": "Immerse yourself in the magical world of Studio Ghibli at this whimsical museum designed by Hayao Miyazaki himself. Explore original artwork, exclusive short films, and interactive exhibits celebrating animation.",
        },
        {
            "activity": "Explore Tsutaya T-Site",
            "description": "Visit one of the most beautiful bookstores in the world, featuring stunning architecture and comprehensive collection of books, music, and movies. Enjoy the attached café while browsing through carefully curated collections.",
        },
        {
            "activity": "Relax at Onsen",
            "description": "Unwind in a traditional Japanese hot spring bath with various pools, saunas, and relaxation areas. Experience this fundamental aspect of Japanese culture while enjoying therapeutic mineral waters.",
        },
        {
            "activity": "Japanese Cooking Class",
            "description": "Learn to make authentic Japanese dishes from professional chefs in a hands-on cooking class. Master the basics of sushi, tempura, or other traditional dishes while learning about Japanese culinary culture.",
        },
        {
            "activity": "Visit Teamlab Borderless",
            "description": "Experience immersive digital art installations at this revolutionary museum. Explore ever-changing interactive artworks that respond to visitor presence in this unique digital art space.",
        },
        {
            "activity": "Sushi Making Experience",
            "description": "Learn the art of sushi making from expert chefs in a professional kitchen. Master the techniques of rice preparation, fish selection, and proper rolling while creating your own sushi masterpieces.",
        },
    ]

    # Track which activities need to be modified
    activities_to_modify = {
        (act["date"], act["activity"]) for act in selected_activities
    }

    # Process each day's schedule
    for day in modified_plan["details"]:
        new_schedule = []
        for activity in day["schedule"]:
            if (day["date"], activity["activity"]) in activities_to_modify:
                # Replace with random activity
                new_activity = random.choice(random_activities)
                new_schedule.append(
                    {
                        "start_time": activity["start_time"],
                        "end_time": activity["end_time"],
                        "activity": new_activity["activity"],
                        "description": new_activity["description"],
                    }
                )
            else:
                new_schedule.append(activity)
        day["schedule"] = new_schedule

    # Update highlights with some random activities
    modified_plan["highlights"] = [
        act["activity"] for act in random.sample(random_activities, 3)
    ]

    # Slightly adjust the cost (randomly between -10% to +10%)
    cost_multiplier = random.uniform(0.9, 1.1)
    modified_plan["total_cost"] = int(original_plan["total_cost"] * cost_multiplier)
    modified_plan["avg_per_day"] = modified_plan["total_cost"] / len(
        modified_plan["details"]
    )

    return modified_plan
