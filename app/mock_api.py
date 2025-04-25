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
                        {
                            "start_time": "8: 00 AM",
                            "end_time": "10: 00 AM",
                            "activity": "Breakfast at Aman Tokyo Café",
                            "description": "Breakfast at Aman Tokyo Café...",
                        },
                        {
                            "start_time": "10: 00 AM",
                            "end_time": "12: 00 PM",
                            "activity": "Visit Senso-ji Temple and Nakamise Street",
                            "description": "Visit Senso-ji Temple and Nakamise Street...",
                        },
                        {
                            "start_time": "1: 00 PM",
                            "end_time": "3: 00 PM",
                            "activity": "Lunch at Sukiyabashi Jiro",
                            "description": "Experience world-famous sushi at Sukiyabashi Jiro...",
                        },
                        {
                            "start_time": "3: 00 PM",
                            "end_time": "5: 00 PM",
                            "activity": "Stroll through Sumida Park",
                            "description": "Enjoy a peaceful walk through the beautiful Sumida Park...",
                        },
                        {
                            "start_time": "7: 00 PM",
                            "end_time": "9: 00 PM",
                            "activity": "Dinner at Ishikawa",
                            "description": "Savor traditional Japanese kaiseki at the prestigious Ishikawa...",
                        },
                    ],
                    "hotel": {"name": "The Ritz-Carlton Tokyo"},
                },
                {
                    "date": "2025-04-25",
                    "schedule": [
                        {
                            "start_time": "8: 30 AM",
                            "end_time": "10: 00 AM",
                            "activity": "Breakfast at Bills Omotesando",
                            "description": "Start your day with famous ricotta pancakes at Bills...",
                        },
                        {
                            "start_time": "10: 00 AM",
                            "end_time": "12: 30 PM",
                            "activity": "Relax at Shinjuku Gyoen National Garden",
                            "description": "Explore one of Tokyo's largest and most beautiful gardens...",
                        },
                        {
                            "start_time": "1: 00 PM",
                            "end_time": "3: 00 PM",
                            "activity": "Lunch at Narisawa",
                            "description": "Experience innovative Japanese cuisine at this acclaimed restaurant...",
                        },
                        {
                            "start_time": "3: 00 PM",
                            "end_time": "5: 00 PM",
                            "activity": "Explore Meiji Shrine",
                            "description": "Visit Tokyo's most important Shinto shrine surrounded by forest...",
                        },
                        {
                            "start_time": "7: 00 PM",
                            "end_time": "9: 00 PM",
                            "activity": "Dinner at Ginza Ukai Tei",
                            "description": "Enjoy premium teppanyaki in an elegant setting...",
                        },
                    ],
                    "hotel": {"name": "The Ritz-Carlton Tokyo"},
                },
                {
                    "date": "2025-04-26",
                    "schedule": [
                        {
                            "start_time": "8: 30 AM",
                            "end_time": "10: 00 AM",
                            "activity": "Breakfast at Café de l'Ambre",
                            "description": "Experience one of Tokyo's oldest and most respected coffee shops...",
                        },
                        {
                            "start_time": "10: 00 AM",
                            "end_time": "12: 30 PM",
                            "activity": "Day trip to Odaiba",
                            "description": "Explore the futuristic artificial island with shopping and entertainment...",
                        },
                        {
                            "start_time": "12: 30 PM",
                            "end_time": "2: 30 PM",
                            "activity": "Lunch at Kua Aina",
                            "description": "Enjoy gourmet burgers with a view of Tokyo Bay...",
                        },
                        {
                            "start_time": "2: 30 PM",
                            "end_time": "4: 30 PM",
                            "activity": "Relax at Oedo-Onsen Monogatari",
                            "description": "Experience a traditional Japanese hot spring theme park...",
                        },
                        {
                            "start_time": "7: 00 PM",
                            "end_time": "9: 00 PM",
                            "activity": "Dinner at The Peninsula Tokyo's Peter Restaurant",
                            "description": "Dine with spectacular views of the Imperial Palace and Tokyo skyline...",
                        },
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
                        {
                            "start_time": "8: 00 AM",
                            "end_time": "10: 00 AM",
                            "activity": "Breakfast at Le Pain Quotidien Shibuya",
                            "description": "Start your day with fresh pastries and organic coffee...",
                        },
                        {
                            "start_time": "10: 00 AM",
                            "end_time": "12: 00 PM",
                            "activity": "Explore Tsukiji Outer Market",
                            "description": "Discover Japan's largest fish market and food street...",
                        },
                        {
                            "start_time": "12: 30 PM",
                            "end_time": "2: 30 PM",
                            "activity": "Lunch at Sushi Dai",
                            "description": "Experience some of Tokyo's finest sushi...",
                        },
                        {
                            "start_time": "3: 00 PM",
                            "end_time": "5: 00 PM",
                            "activity": "Visit Tokyo Tower",
                            "description": "Visit the iconic Tokyo Tower and its observation decks...",
                        },
                        {
                            "start_time": "7: 00 PM",
                            "end_time": "9: 00 PM",
                            "activity": "Dinner at Seryna Honten",
                            "description": "Enjoy premium Kobe beef in the heart of Ginza...",
                        },
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
                {
                    "date": "2025-04-25",
                    "schedule": [
                        {
                            "start_time": "8: 30 AM",
                            "end_time": "10: 00 AM",
                            "activity": "Breakfast at Hyatt Regency Tokyo's Café du Parc",
                            "description": "Enjoy an elegant breakfast with city views...",
                        },
                        {
                            "start_time": "10: 00 AM",
                            "end_time": "12: 30 PM",
                            "activity": "Explore Akihabara",
                            "description": "Discover Japan's electronics and anime culture center...",
                        },
                        {
                            "start_time": "1: 00 PM",
                            "end_time": "3: 00 PM",
                            "activity": "Lunch at Yakiniku Jumbo Hanare",
                            "description": "Experience premium Japanese BBQ...",
                        },
                        {
                            "start_time": "4: 00 PM",
                            "end_time": "6: 00 PM",
                            "activity": "Night views at Roppongi Hills Mori Tower",
                            "description": "Enjoy panoramic views of Tokyo from the observation deck...",
                        },
                        {
                            "start_time": "7: 30 PM",
                            "end_time": "9: 30 PM",
                            "activity": "Dinner at Tempura Kondo",
                            "description": "Savor exquisite tempura at this Michelin-starred restaurant...",
                        },
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
                {
                    "date": "2025-04-26",
                    "schedule": [
                        {
                            "start_time": "8: 30 AM",
                            "end_time": "10: 00 AM",
                            "activity": "Breakfast at Blue Bottle Coffee Kyoto Café",
                            "description": "Start your day with artisanal coffee and pastries...",
                        },
                        {
                            "start_time": "10: 00 AM",
                            "end_time": "12: 00 PM",
                            "activity": "Visit Tokyo National Museum",
                            "description": "Explore Japan's oldest and largest art museum...",
                        },
                        {
                            "start_time": "12: 30 PM",
                            "end_time": "2: 30 PM",
                            "activity": "Lunch at Tapas Molecular Bar",
                            "description": "Experience innovative molecular gastronomy...",
                        },
                        {
                            "start_time": "5: 00 PM",
                            "end_time": "8: 00 PM",
                            "activity": "Dinner cruise on yakatabune boat",
                            "description": "Enjoy traditional Japanese cuisine while cruising Tokyo Bay...",
                        },
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
                        {
                            "start_time": "8: 00 AM",
                            "end_time": "10: 00 AM",
                            "activity": "Breakfast at Café Kitsuné Aoyama",
                            "description": "Start your day at this trendy French-Japanese café...",
                        },
                        {
                            "start_time": "10: 00 AM",
                            "end_time": "12: 00 PM",
                            "activity": "Tour Imperial Palace East Gardens",
                            "description": "Explore the beautiful gardens of Japan's Imperial Palace...",
                        },
                        {
                            "start_time": "12: 30 PM",
                            "end_time": "2: 30 PM",
                            "activity": "Lunch at Maisen Omotesando",
                            "description": "Enjoy Japan's best tonkatsu in a historic setting...",
                        },
                        {
                            "start_time": "3: 00 PM",
                            "end_time": "5: 00 PM",
                            "activity": "Browse Harajuku and Omotesando boutiques",
                            "description": "Explore Tokyo's fashion and design district...",
                        },
                        {
                            "start_time": "7: 00 PM",
                            "end_time": "9: 00 PM",
                            "activity": "Dinner at Quintessence",
                            "description": "Experience French-Japanese fusion at this 3-Michelin starred restaurant...",
                        },
                    ],
                    "hotel": {"name": "Hotel Chinzanso Tokyo"},
                },
                {
                    "date": "2025-04-25",
                    "schedule": [
                        {
                            "start_time": "8: 30 AM",
                            "end_time": "10: 00 AM",
                            "activity": "Breakfast at Sarabeth's Shinjuku",
                            "description": "Enjoy classic American breakfast with a Japanese twist...",
                        },
                        {
                            "start_time": "10: 00 AM",
                            "end_time": "12: 30 PM",
                            "activity": "Explore Ryogoku and Sumo Museum",
                            "description": "Learn about Japan's national sport in its spiritual home...",
                        },
                        {
                            "start_time": "12: 30 PM",
                            "end_time": "2: 30 PM",
                            "activity": "Lunch at Irokawa (Unagi)",
                            "description": "Savor traditional grilled eel at this century-old restaurant...",
                        },
                        {
                            "start_time": "3: 00 PM",
                            "end_time": "5: 00 PM",
                            "activity": "Stroll through Yanaka Ginza",
                            "description": "Experience the atmosphere of old Tokyo in this historic shopping street...",
                        },
                        {
                            "start_time": "7: 30 PM",
                            "end_time": "9: 30 PM",
                            "activity": "Dinner at Ryugin",
                            "description": "Experience innovative Japanese cuisine at this 3-Michelin starred restaurant...",
                        },
                    ],
                    "hotel": {"name": "Hotel Chinzanso Tokyo"},
                },
                {
                    "date": "2025-04-26",
                    "schedule": [
                        {
                            "start_time": "8: 00 AM",
                            "end_time": "9: 00 AM",
                            "activity": "Breakfast at Grain Bar",
                            "description": "Start your day with healthy, grain-based breakfast...",
                        },
                        {
                            "start_time": "9: 00 AM",
                            "end_time": "1: 00 PM",
                            "activity": "Day trip and hike at Mt. Takao",
                            "description": "Enjoy a scenic hike with beautiful views of Mt. Fuji...",
                        },
                        {
                            "start_time": "1: 00 PM",
                            "end_time": "2: 30 PM",
                            "activity": "Lunch at Yakuo-In Temple",
                            "description": "Experience traditional Buddhist vegetarian cuisine...",
                        },
                        {
                            "start_time": "4: 00 PM",
                            "end_time": "6: 00 PM",
                            "activity": "Spa retreat at Mandarin Oriental Spa Tokyo",
                            "description": "Relax with traditional Japanese treatments and city views...",
                        },
                        {
                            "start_time": "7: 00 PM",
                            "end_time": "9: 00 PM",
                            "activity": "Dinner at Andaz Tokyo Rooftop Bar",
                            "description": "End your trip with cocktails and dinner with panoramic views...",
                        },
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

    # Random activity options with descriptions
    random_activities = [
        {
            "activity": "Visit Tokyo Skytree",
            "description": "Experience breathtaking views from Japan's tallest structure...",
        },
        {
            "activity": "Shopping at Shibuya 109",
            "description": "Explore the trendy fashion mecca of Tokyo...",
        },
        {
            "activity": "Explore Akihabara",
            "description": "Discover Japan's electronics and anime culture center...",
        },
        {
            "activity": "Visit Ueno Park",
            "description": "Stroll through one of Tokyo's largest public parks...",
        },
        {
            "activity": "Tea Ceremony Experience",
            "description": "Learn about traditional Japanese tea culture...",
        },
        {
            "activity": "Karaoke Session",
            "description": "Enjoy a fun karaoke session in the heart of Tokyo...",
        },
        {
            "activity": "Visit Ghibli Museum",
            "description": "Immerse yourself in the magical world of Studio Ghibli...",
        },
        {
            "activity": "Explore Tsutaya T-Site",
            "description": "Visit one of the most beautiful bookstores in the world...",
        },
        {
            "activity": "Relax at Onsen",
            "description": "Unwind in a traditional Japanese hot spring bath...",
        },
        {
            "activity": "Japanese Cooking Class",
            "description": "Learn to make authentic Japanese dishes...",
        },
        {
            "activity": "Visit Teamlab Borderless",
            "description": "Experience immersive digital art installations...",
        },
        {
            "activity": "Sushi Making Experience",
            "description": "Learn the art of sushi making from expert chefs...",
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
