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
            "title": "Vibrant Tokyo Escape",
            "highlights": [
                "Shibuya Crossing Adventure",
                "Harajuku Shopping & Street Food",
                "Yoyogi Park Serenity",
            ],
            "total_cost": 1500,
            "avg_per_day": 500.0,
            "hotels": [
                {
                    "name": "The Tokyo Central Hotel",
                    "price": 300,
                    "rating": 4.8,
                    "start_date": "2025-05-28",
                    "end_date": "2025-05-31",
                    "booking_link": "https://example.com/tokyo-central-hotel",
                }
            ],
            "flights": [
                {
                    "start_date": "2025-05-28",
                    "from": "Taipei",
                    "to": "Tokyo",
                    "airline": "Japan Airlines",
                    "class": "Economy",
                    "check-in luggage": True,
                    "price": 900,
                    "booking_link": "https://example.com/japan-airlines",
                }
            ],
            "details": [
                {
                    "date": "2025-05-28",
                    "schedule": [
                        {
                            "start_time": "09:00 AM",
                            "end_time": "10:30 AM",
                            "activity": "Check into Hotel",
                            "description": "Arrive in Tokyo and check into The Tokyo Central Hotel, known for its prime location and excellent service.",
                        },
                        {
                            "start_time": "10:30 AM",
                            "end_time": "12:00 PM",
                            "activity": "Explore Shibuya Crossing",
                            "description": "Immerse yourself in the bustling energy of Shibuya Crossing, a must-see Tokyo landmark.",
                        },
                        {
                            "start_time": "12:00 PM",
                            "end_time": "02:00 PM",
                            "activity": "Lunch at Sushi Restaurant",
                            "description": "Enjoy fresh sushi at a local restaurant; try the chef\u2019s special for an authentic Japanese experience.",
                        },
                        {
                            "start_time": "02:00 PM",
                            "end_time": "05:00 PM",
                            "activity": "Discover Harajuku",
                            "description": "Shop trendy outfits and savor famous Japanese crepes in Harajuku.",
                        },
                        {
                            "start_time": "05:00 PM",
                            "end_time": "07:00 PM",
                            "activity": "Relax at Yoyogi Park",
                            "description": "A peaceful walk through Yoyogi Park amidst lush greenery is perfect for unwinding.",
                        },
                        {
                            "start_time": "07:00 PM",
                            "end_time": "09:00 PM",
                            "activity": "Dinner at Izakaya",
                            "description": "Experience authentic Japanese pub culture with delicious dishes and an assortment of drinks.",
                        },
                    ],
                    "hotel": {"name": "The Tokyo Central Hotel"},
                },
                {
                    "date": "2025-05-29",
                    "schedule": [
                        {
                            "start_time": "09:00 AM",
                            "end_time": "10:30 AM",
                            "activity": "Breakfast at Local Caf\u00e9",
                            "description": "Enjoy Japanese-style breakfast at a charming caf\u00e9, famous for their fluffy pancakes.",
                        },
                        {
                            "start_time": "10:30 AM",
                            "end_time": "12:00 PM",
                            "activity": "Visit Meiji Shrine",
                            "description": "Explore the tranquility of Meiji Shrine surrounded by dense woods.",
                        },
                        {
                            "start_time": "12:00 PM",
                            "end_time": "02:00 PM",
                            "activity": "Lunch at Ramen Shop",
                            "description": "Savor traditional ramen at a cozy shop; try miso or tonkotsu ramen for authentic flavors.",
                        },
                        {
                            "start_time": "02:00 PM",
                            "end_time": "05:00 PM",
                            "activity": "Explore Shimokitazawa and Nakameguro",
                            "description": "Roam unique shops and cafes in Shimokitazawa, then stroll through Nakameguro's serene streets.",
                        },
                        {
                            "start_time": "05:00 PM",
                            "end_time": "07:00 PM",
                            "activity": "Walk Along Meguro River",
                            "description": "Enjoy scenic views while walking the river lined with sakura trees.",
                        },
                        {
                            "start_time": "07:00 PM",
                            "end_time": "09:00 PM",
                            "activity": "Dinner at Kaiseki Restaurant",
                            "description": "Experience a Japanese multi-course meal with elegant presentation.",
                        },
                    ],
                    "hotel": {"name": "The Tokyo Central Hotel"},
                },
                {
                    "date": "2025-05-30",
                    "schedule": [
                        {
                            "start_time": "09:00 AM",
                            "end_time": "10:30 AM",
                            "activity": "Breakfast at Hotel",
                            "description": "Relish a continental or Japanese breakfast at the hotel before heading out.",
                        },
                        {
                            "start_time": "10:30 AM",
                            "end_time": "12:00 PM",
                            "activity": "Visit Tokyo National Museum",
                            "description": "Discover Japanese history and art with fascinating exhibits.",
                        },
                        {
                            "start_time": "12:00 PM",
                            "end_time": "02:00 PM",
                            "activity": "Lunch at Tempura Restaurant",
                            "description": "Enjoy crispy tempura dishes at one of the best spots in Tokyo.",
                        },
                        {
                            "start_time": "02:00 PM",
                            "end_time": "05:00 PM",
                            "activity": "Akihabara Shopping",
                            "description": "Find electronics and anime merchandise in the vibrant Akihabara district.",
                        },
                        {
                            "start_time": "05:00 PM",
                            "end_time": "07:00 PM",
                            "activity": "Departure to Airport",
                            "description": "Head to the airport to conclude your Tokyo adventure.",
                        },
                    ],
                    "hotel": {"name": "The Tokyo Central Hotel"},
                },
            ],
        },
        {
            "title": "Hidden Gems in Tokyo",
            "highlights": [
                "Shimokitazawa Treasure Hunt",
                "Peaceful Meiji Shrine",
                "Meguro River Walk",
            ],
            "total_cost": 1200,
            "avg_per_day": 400.0,
            "hotels": [
                {
                    "name": "Tokyo Boutique Stay",
                    "price": 250,
                    "rating": 4.5,
                    "start_date": "2025-05-28",
                    "end_date": "2025-05-31",
                    "booking_link": "https://example.com/tokyo-boutique-stay",
                }
            ],
            "flights": [
                {
                    "start_date": "2025-05-28",
                    "from": "Taipei",
                    "to": "Tokyo",
                    "airline": "ANA",
                    "class": "Economy",
                    "check-in luggage": True,
                    "price": 800,
                    "booking_link": "https://example.com/ana-flights",
                }
            ],
            "details": [
                {
                    "date": "2025-05-28",
                    "schedule": [
                        {
                            "start_time": "09:00 AM",
                            "end_time": "10:30 AM",
                            "activity": "Hotel Check-in at Boutique Stay",
                            "description": "Arrive and settle into Tokyo Boutique Stay, offering artistic interiors and cozy vibes.",
                        },
                        {
                            "start_time": "10:30 AM",
                            "end_time": "12:00 PM",
                            "activity": "Wander Shibuya Crossing",
                            "description": "Dive into Tokyo\u2019s fast-paced lifestyle at the iconic crossing.",
                        },
                        {
                            "start_time": "12:00 PM",
                            "end_time": "02:00 PM",
                            "activity": "Sushi Tasting Lunch",
                            "description": "Experience sushi artistry and flavors at a renowned specialty restaurant.",
                        },
                        {
                            "start_time": "02:00 PM",
                            "end_time": "05:00 PM",
                            "activity": "Explore Shimokitazawa",
                            "description": "Discover vintage shops and unique cafes in this bohemian neighborhood.",
                        },
                        {
                            "start_time": "05:00 PM",
                            "end_time": "07:00 PM",
                            "activity": "Dinner at Local Izakaya",
                            "description": "Enjoy a casual dining experience with a variety of Japanese dishes.",
                        },
                    ],
                    "hotel": {"name": "Tokyo Boutique Stay"},
                },
                {
                    "date": "2025-05-29",
                    "schedule": [
                        {
                            "start_time": "09:00 AM",
                            "end_time": "10:30 AM",
                            "activity": "Breakfast at Local Caf\u00e9",
                            "description": "Start your day with a delicious breakfast at a nearby caf\u00e9.",
                        },
                        {
                            "start_time": "10:30 AM",
                            "end_time": "12:00 PM",
                            "activity": "Visit Meiji Shrine",
                            "description": "Experience the serene atmosphere of this historic shrine.",
                        },
                        {
                            "start_time": "12:00 PM",
                            "end_time": "02:00 PM",
                            "activity": "Lunch at Ramen Shop",
                            "description": "Savor a bowl of authentic ramen at a popular local spot.",
                        },
                        {
                            "start_time": "02:00 PM",
                            "end_time": "05:00 PM",
                            "activity": "Stroll Along Meguro River",
                            "description": "Enjoy a leisurely walk along the picturesque river.",
                        },
                        {
                            "start_time": "05:00 PM",
                            "end_time": "07:00 PM",
                            "activity": "Dinner at Kaiseki Restaurant",
                            "description": "Indulge in a traditional multi-course Japanese meal.",
                        },
                    ],
                    "hotel": {"name": "Tokyo Boutique Stay"},
                },
                {
                    "date": "2025-05-30",
                    "schedule": [
                        {
                            "start_time": "09:00 AM",
                            "end_time": "10:30 AM",
                            "activity": "Breakfast at Hotel",
                            "description": "Enjoy a relaxing breakfast at your hotel.",
                        },
                        {
                            "start_time": "10:30 AM",
                            "end_time": "12:00 PM",
                            "activity": "Visit Tokyo National Museum",
                            "description": "Explore the rich history and culture of Japan.",
                        },
                        {
                            "start_time": "12:00 PM",
                            "end_time": "02:00 PM",
                            "activity": "Lunch at Tempura Restaurant",
                            "description": "Delight in crispy tempura dishes at a well-known restaurant.",
                        },
                        {
                            "start_time": "02:00 PM",
                            "end_time": "05:00 PM",
                            "activity": "Shopping in Akihabara",
                            "description": "Find unique electronics and anime merchandise in this vibrant district.",
                        },
                        {
                            "start_time": "05:00 PM",
                            "end_time": "07:00 PM",
                            "activity": "Departure to Airport",
                            "description": "Conclude your trip and head to the airport.",
                        },
                    ],
                    "hotel": {"name": "Tokyo Boutique Stay"},
                },
            ],
        },
        {
            "title": "Traditional Tokyo Journey",
            "highlights": [
                "Meiji Shrine Serenity",
                "Kaiseki Dining Experience",
                "Tokyo National Museum",
            ],
            "total_cost": 1600,
            "avg_per_day": 533.33,
            "hotels": [
                {
                    "name": "Tokyo Imperial Hotel",
                    "price": 350,
                    "rating": 5.0,
                    "start_date": "2025-05-28",
                    "end_date": "2025-05-31",
                    "booking_link": "https://example.com/tokyo-imperial-hotel",
                }
            ],
            "flights": [
                {
                    "start_date": "2025-05-28",
                    "from": "Taipei",
                    "to": "Tokyo",
                    "airline": "Delta Airlines",
                    "class": "Business",
                    "check-in luggage": True,
                    "price": 1200,
                    "booking_link": "https://example.com/delta-flights",
                }
            ],
            "details": [
                {
                    "date": "2025-05-28",
                    "schedule": [
                        {
                            "start_time": "09:00 AM",
                            "end_time": "10:30 AM",
                            "activity": "Check into Hotel",
                            "description": "Arrive at the luxurious Tokyo Imperial Hotel.",
                        },
                        {
                            "start_time": "10:30 AM",
                            "end_time": "12:00 PM",
                            "activity": "Visit Meiji Shrine",
                            "description": "Experience the tranquility of this historic shrine.",
                        },
                        {
                            "start_time": "12:00 PM",
                            "end_time": "02:00 PM",
                            "activity": "Lunch at Kaiseki Restaurant",
                            "description": "Indulge in a traditional multi-course meal.",
                        },
                        {
                            "start_time": "02:00 PM",
                            "end_time": "05:00 PM",
                            "activity": "Explore Ueno Park",
                            "description": "Stroll through the beautiful park and visit museums.",
                        },
                        {
                            "start_time": "05:00 PM",
                            "end_time": "07:00 PM",
                            "activity": "Dinner at a Local Izakaya",
                            "description": "Enjoy a casual dining experience with a variety of Japanese dishes.",
                        },
                    ],
                    "hotel": {"name": "Tokyo Imperial Hotel"},
                },
                {
                    "date": "2025-05-29",
                    "schedule": [
                        {
                            "start_time": "09:00 AM",
                            "end_time": "10:30 AM",
                            "activity": "Breakfast at Hotel",
                            "description": "Enjoy a luxurious breakfast at the hotel.",
                        },
                        {
                            "start_time": "10:30 AM",
                            "end_time": "12:00 PM",
                            "activity": "Visit Tokyo National Museum",
                            "description": "Explore the rich history and culture of Japan.",
                        },
                        {
                            "start_time": "12:00 PM",
                            "end_time": "02:00 PM",
                            "activity": "Lunch at Tempura Restaurant",
                            "description": "Delight in crispy tempura dishes.",
                        },
                        {
                            "start_time": "02:00 PM",
                            "end_time": "05:00 PM",
                            "activity": "Shopping in Ginza",
                            "description": "Explore high-end shops and boutiques.",
                        },
                        {
                            "start_time": "05:00 PM",
                            "end_time": "07:00 PM",
                            "activity": "Dinner at a Traditional Restaurant",
                            "description": "Experience authentic Japanese cuisine.",
                        },
                    ],
                    "hotel": {"name": "Tokyo Imperial Hotel"},
                },
                {
                    "date": "2025-05-30",
                    "schedule": [
                        {
                            "start_time": "09:00 AM",
                            "end_time": "10:30 AM",
                            "activity": "Breakfast at Hotel",
                            "description": "Enjoy a relaxing breakfast at your hotel.",
                        },
                        {
                            "start_time": "10:30 AM",
                            "end_time": "12:00 PM",
                            "activity": "Visit Asakusa and Senso-ji Temple",
                            "description": "Explore the historic temple and surrounding area.",
                        },
                        {
                            "start_time": "12:00 PM",
                            "end_time": "02:00 PM",
                            "activity": "Lunch at a Local Restaurant",
                            "description": "Savor local dishes in Asakusa.",
                        },
                        {
                            "start_time": "02:00 PM",
                            "end_time": "05:00 PM",
                            "activity": "Departure to Airport",
                            "description": "Conclude your trip and head to the airport.",
                        },
                    ],
                    "hotel": {"name": "Tokyo Imperial Hotel"},
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
