import json
import random
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
            "title": "Luxurious Food & Culture Bliss",
            "highlights": [
                "Sushi at Sukiyabashi Jiro",
                "Stroll through Sumida Park",
                "Kaiseki dinner at Ishikawa",
            ],
            "total_cost": 5200,
            "avg_per_day": 1733,
            "hotels": [
                {
                    "name": "The Ritz-Carlton Tokyo",
                    "price": 1200,
                    "rating": 4.8,
                    "start_date": "2025-04-24",
                    "end_date": "2025-04-27",
                }
            ],
            "flights": [
                {
                    "start_date": "2025-04-24",
                    "from": "New York (JFK)",
                    "to": "Tokyo (NRT)",
                    "airline": "ANA",
                    "class": "Business",
                    "check-in luggage": True,
                    "price": 2100,
                },
                {
                    "start_date": "2025-04-27",
                    "from": "Tokyo (NRT)",
                    "to": "New York (JFK)",
                    "airline": "ANA",
                    "class": "Business",
                    "check-in luggage": True,
                    "price": 2100,
                },
            ],
            "details": [
                {
                    "date": "2025-04-24",
                    "schedule": [
                        ["8: 00 AM", "Breakfast at Aman Tokyo Café"],
                        ["10: 00 AM", "Visit Senso-ji Temple and Nakamise Street"],
                        ["1: 00 PM", "Lunch at Sukiyabashi Jiro"],
                        ["3: 00 PM", "Stroll through Sumida Park"],
                        ["7: 00 PM", "Dinner at Ishikawa"],
                    ],
                    "hotel": {"name": "The Ritz-Carlton Tokyo"},
                },
                {
                    "date": "2025-04-25",
                    "schedule": [
                        ["8: 30 AM", "Breakfast at Bills Omotesando"],
                        ["10: 00 AM", "Relax at Shinjuku Gyoen National Garden"],
                        ["1: 00 PM", "Lunch at Narisawa"],
                        ["3: 00 PM", "Explore Meiji Shrine"],
                        ["7: 00 PM", "Dinner at Ginza Ukai Tei"],
                    ],
                    "hotel": {"name": "The Ritz-Carlton Tokyo"},
                },
                {
                    "date": "2025-04-26",
                    "schedule": [
                        ["8: 30 AM", "Breakfast at Café de l'Ambre"],
                        ["10: 00 AM", "Day trip to Odaiba"],
                        ["12: 30 PM", "Lunch at Kua Aina"],
                        ["2: 30 PM", "Relax at Oedo-Onsen Monogatari"],
                        [
                            "7: 00 PM",
                            "Dinner at The Peninsula Tokyo's Peter Restaurant",
                        ],
                    ],
                    "hotel": {"name": "The Ritz-Carlton Tokyo"},
                },
            ],
        },
        {
            "title": "Tokyo Foodie Escapade",
            "highlights": [
                "Explore Tsukiji Market",
                "Night views at Mori Tower",
                "Dinner cruise on Yakatabune",
            ],
            "total_cost": 4600,
            "avg_per_day": 1533,
            "hotels": [
                {
                    "name": "Park Hyatt Tokyo",
                    "price": 1100,
                    "rating": 4.9,
                    "start_date": "2025-04-24",
                    "end_date": "2025-04-27",
                }
            ],
            "flights": [
                {
                    "start_date": "2025-04-24",
                    "from": "San Francisco (SFO)",
                    "to": "Tokyo (HND)",
                    "airline": "United Airlines",
                    "class": "Premium Economy",
                    "check-in luggage": True,
                    "price": 1750,
                },
                {
                    "start_date": "2025-04-27",
                    "from": "Tokyo (HND)",
                    "to": "San Francisco (SFO)",
                    "airline": "United Airlines",
                    "class": "Premium Economy",
                    "check-in luggage": True,
                    "price": 1750,
                },
            ],
            "details": [
                {
                    "date": "2025-04-24",
                    "schedule": [
                        ["8: 00 AM", "Breakfast at Le Pain Quotidien Shibuya"],
                        ["10: 00 AM", "Explore Tsukiji Outer Market"],
                        ["12: 30 PM", "Lunch at Sushi Dai"],
                        ["3: 00 PM", "Visit Tokyo Tower"],
                        ["7: 00 PM", "Dinner at Seryna Honten"],
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
                {
                    "date": "2025-04-25",
                    "schedule": [
                        ["8: 30 AM", "Breakfast at Hyatt Regency Tokyo's Café du Parc"],
                        ["10: 00 AM", "Explore Akihabara"],
                        ["1: 00 PM", "Lunch at Yakiniku Jumbo Hanare"],
                        ["4: 00 PM", "Night views at Roppongi Hills Mori Tower"],
                        ["7: 30 PM", "Dinner at Tempura Kondo"],
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
                {
                    "date": "2025-04-26",
                    "schedule": [
                        ["8: 30 AM", "Breakfast at Blue Bottle Coffee Kyoto Café"],
                        ["10: 00 AM", "Visit Tokyo National Museum"],
                        ["12: 30 PM", "Lunch at Tapas Molecular Bar"],
                        ["5: 00 PM", "Dinner cruise on yakatabune boat"],
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
            ],
        },
        {
            "title": "Scenic Tokyo Retreat",
            "highlights": [
                "Visit Imperial Palace Gardens",
                "Scenic hike at Mt. Takao",
                "Spa retreat at Mandarin Oriental",
            ],
            "total_cost": 4800,
            "avg_per_day": 1600,
            "hotels": [
                {
                    "name": "Hotel Chinzanso Tokyo",
                    "price": 1200,
                    "rating": 4.8,
                    "start_date": "2025-04-24",
                    "end_date": "2025-04-27",
                }
            ],
            "flights": [
                {
                    "start_date": "2025-04-24",
                    "from": "Los Angeles (LAX)",
                    "to": "Tokyo (HND)",
                    "airline": "Japan Airlines",
                    "class": "Economy",
                    "check-in luggage": True,
                    "price": 1800,
                },
                {
                    "start_date": "2025-04-27",
                    "from": "Tokyo (HND)",
                    "to": "Los Angeles (LAX)",
                    "airline": "Japan Airlines",
                    "class": "Economy",
                    "check-in luggage": True,
                    "price": 1800,
                },
            ],
            "details": [
                {
                    "date": "2025-04-24",
                    "schedule": [
                        ["8: 00 AM", "Breakfast at Café Kitsuné Aoyama"],
                        ["10: 00 AM", "Tour Imperial Palace East Gardens"],
                        ["12: 30 PM", "Lunch at Maisen Omotesando"],
                        ["3: 00 PM", "Browse Harajuku and Omotesando boutiques"],
                        ["7: 00 PM", "Dinner at Quintessence"],
                    ],
                    "hotel": {"name": "Hotel Chinzanso Tokyo"},
                },
                {
                    "date": "2025-04-25",
                    "schedule": [
                        ["8: 30 AM", "Breakfast at Sarabeth's Shinjuku"],
                        ["10: 00 AM", "Explore Ryogoku and Sumo Museum"],
                        ["12: 30 PM", "Lunch at Irokawa (Unagi)"],
                        ["3: 00 PM", "Stroll through Yanaka Ginza"],
                        ["7: 30 PM", "Dinner at Ryugin"],
                    ],
                    "hotel": {"name": "Hotel Chinzanso Tokyo"},
                },
                {
                    "date": "2025-04-26",
                    "schedule": [
                        ["8: 00 AM", "Breakfast at Grain Bar"],
                        ["9: 00 AM", "Day trip and hike at Mt. Takao"],
                        ["1: 00 PM", "Lunch at Yakuo-In Temple"],
                        ["4: 00 PM", "Spa retreat at Mandarin Oriental Spa Tokyo"],
                        ["7: 00 PM", "Dinner at Andaz Tokyo Rooftop Bar"],
                    ],
                    "hotel": {"name": "Hotel Chinzanso Tokyo"},
                },
            ],
        },
    ]


def get_mock_modified_itinerary(
    original_plan, selected_activities, modification_instruction
):
    """Mock function to simulate itinerary modification"""
    # Create a deep copy of the original plan
    modified_plan = json.loads(json.dumps(original_plan))

    # Random activity options
    random_activities = [
        "Visit Tokyo Skytree",
        "Shopping at Shibuya 109",
        "Explore Akihabara",
        "Visit Ueno Park",
        "Tea Ceremony Experience",
        "Karaoke Session",
        "Visit Ghibli Museum",
        "Explore Tsutaya T-Site",
        "Relax at Onsen",
        "Japanese Cooking Class",
        "Visit Teamlab Borderless",
        "Sushi Making Experience",
    ]

    # Track which activities need to be modified
    activities_to_modify = {
        (act["date"], act["activity"]) for act in selected_activities
    }

    # Process each day's schedule
    for day in modified_plan["details"]:
        new_schedule = []
        for time, activity in day["schedule"]:
            if (day["date"], activity) in activities_to_modify:
                # Replace with random activity
                activity = random.choice(random_activities)
            new_schedule.append((time, activity))
        day["schedule"] = new_schedule

    # Update highlights with some random activities
    modified_plan["highlights"] = random.sample(random_activities, 3)

    # Slightly adjust the cost (randomly between -10% to +10%)
    cost_multiplier = random.uniform(0.9, 1.1)
    modified_plan["total_cost"] = int(original_plan["total_cost"] * cost_multiplier)
    modified_plan["avg_per_day"] = modified_plan["total_cost"] / len(
        modified_plan["details"]
    )

    return modified_plan
