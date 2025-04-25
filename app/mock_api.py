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
                            "start_time": "08:00",
                            "end_time": "10:00",
                            "activity": "Breakfast at Aman Tokyo Café",
                            "description": "Breakfast at Aman Tokyo Café, featuring a stunning blend of Western and Japanese breakfast options with panoramic city views. Enjoy fresh pastries, seasonal fruits, and traditional Japanese breakfast items in an elegant setting.",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "12:00",
                            "activity": "Visit Senso-ji Temple and Nakamise Street",
                            "description": "Visit Senso-ji Temple and Nakamise Street, Tokyo's oldest Buddhist temple and its traditional shopping street. Experience the rich history, architecture, and local culture while exploring various traditional Japanese shops and street food stalls.",
                        },
                        {
                            "start_time": "13:00",
                            "end_time": "15:00",
                            "activity": "Lunch at Sukiyabashi Jiro",
                            "description": "Experience world-famous sushi at Sukiyabashi Jiro, the legendary restaurant of sushi master Jiro Ono. Savor the finest quality sushi prepared with decades of expertise and the freshest ingredients from Tsukiji market.",
                        },
                        {
                            "start_time": "15:00",
                            "end_time": "17:00",
                            "activity": "Stroll through Sumida Park",
                            "description": "Enjoy a peaceful walk through the beautiful Sumida Park, famous for its cherry blossoms in spring and stunning views of Tokyo Skytree. The riverside park offers perfect photo opportunities and a chance to experience local life.",
                        },
                        {
                            "start_time": "19:00",
                            "end_time": "21:00",
                            "activity": "Dinner at Ishikawa",
                            "description": "Savor traditional Japanese kaiseki at the prestigious Ishikawa, a three-Michelin-starred restaurant. Experience the epitome of Japanese haute cuisine with seasonal ingredients and impeccable presentation in an intimate setting.",
                        },
                    ],
                    "hotel": {"name": "The Ritz-Carlton Tokyo"},
                },
                {
                    "date": "2025-04-25",
                    "schedule": [
                        {
                            "start_time": "08:30",
                            "end_time": "10:00",
                            "activity": "Breakfast at Bills Omotesando",
                            "description": "Start your day with famous ricotta pancakes at Bills, known worldwide for their fluffy texture and fresh ingredients. Enjoy the stylish atmosphere of Omotesando while dining at this Australian breakfast institution.",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "12:30",
                            "activity": "Relax at Shinjuku Gyoen National Garden",
                            "description": "Explore one of Tokyo's largest and most beautiful gardens, featuring Japanese traditional, English landscape, and French formal gardens. A perfect spot for photography and peaceful contemplation away from the city bustle.",
                        },
                        {
                            "start_time": "13:00",
                            "end_time": "15:00",
                            "activity": "Lunch at Narisawa",
                            "description": "Experience innovative Japanese cuisine at this acclaimed two-Michelin-starred restaurant. Chef Yoshihiro Narisawa's unique 'Innovative Satoyama' cuisine combines Japanese ingredients with French techniques in sustainable and artistic presentations.",
                        },
                        {
                            "start_time": "15:00",
                            "end_time": "17:00",
                            "activity": "Explore Meiji Shrine",
                            "description": "Visit Tokyo's most important Shinto shrine surrounded by a lush forest of 120,000 trees. Experience the serenity of traditional Japanese spirituality and possibly witness a traditional wedding ceremony.",
                        },
                        {
                            "start_time": "19:00",
                            "end_time": "21:00",
                            "activity": "Dinner at Ginza Ukai Tei",
                            "description": "Enjoy premium teppanyaki in an elegant Art Nouveau setting. Watch master chefs prepare the finest Japanese beef and seasonal ingredients with precision and artistry right at your table.",
                        },
                    ],
                    "hotel": {"name": "The Ritz-Carlton Tokyo"},
                },
                {
                    "date": "2025-04-26",
                    "schedule": [
                        {
                            "start_time": "08:30",
                            "end_time": "10:00",
                            "activity": "Breakfast at Café de l'Ambre",
                            "description": "Experience one of Tokyo's oldest and most respected coffee shops, operating since 1948. Taste their signature aged coffee beans and classic brewing methods in a nostalgic atmosphere.",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "12:30",
                            "activity": "Day trip to Odaiba",
                            "description": "Explore the futuristic artificial island with shopping and entertainment complexes. Visit TeamLab Borderless, Joypolis amusement park, and the life-sized Gundam statue while enjoying spectacular views of Tokyo Bay.",
                        },
                        {
                            "start_time": "12:30",
                            "end_time": "14:30",
                            "activity": "Lunch at Kua Aina",
                            "description": "Enjoy gourmet burgers with a view of Tokyo Bay at this Hawaiian-inspired restaurant. Known for their perfectly grilled patties and fresh ingredients, it's a perfect casual dining spot in Odaiba.",
                        },
                        {
                            "start_time": "14:30",
                            "end_time": "16:30",
                            "activity": "Relax at Oedo-Onsen Monogatari",
                            "description": "Experience a traditional Japanese hot spring theme park with various baths, saunas, and relaxation areas. Wear yukata robes while enjoying traditional games and foods in the Edo-period themed complex.",
                        },
                        {
                            "start_time": "19:00",
                            "end_time": "21:00",
                            "activity": "Dinner at The Peninsula Tokyo's Peter Restaurant",
                            "description": "Dine with spectacular views of the Imperial Palace and Tokyo skyline from the 24th floor. Enjoy modern European cuisine with Japanese influences while watching the city lights sparkle below.",
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
                            "start_time": "08:00",
                            "end_time": "10:00",
                            "activity": "Breakfast at Le Pain Quotidien Shibuya",
                            "description": "Start your day with fresh pastries and organic coffee at this beloved Belgian bakery chain. Enjoy artisanal bread, organic eggs, and healthy breakfast options in a cozy, rustic setting in the heart of Shibuya.",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "12:00",
                            "activity": "Explore Tsukiji Outer Market",
                            "description": "Discover Japan's largest fish market and food street, featuring hundreds of shops selling fresh seafood, produce, and kitchen tools. Sample fresh sushi, grilled seafood, and local specialties while exploring the historic market area.",
                        },
                        {
                            "start_time": "12:30",
                            "end_time": "14:30",
                            "activity": "Lunch at Sushi Dai",
                            "description": "Experience some of Tokyo's finest sushi at this renowned establishment, famous for its expert preparation and premium quality fish. Enjoy an omakase course featuring the day's best catches in an intimate counter setting.",
                        },
                        {
                            "start_time": "15:00",
                            "end_time": "17:00",
                            "activity": "Visit Tokyo Tower",
                            "description": "Visit the iconic Tokyo Tower and its observation decks for stunning city views. Explore the various attractions including the One Piece Tower theme park and the tower's aquarium, while photographing this symbol of Tokyo's post-war rebirth.",
                        },
                        {
                            "start_time": "19:00",
                            "end_time": "21:00",
                            "activity": "Dinner at Seryna Honten",
                            "description": "Enjoy premium Kobe beef in the heart of Ginza at this established sukiyaki and shabu-shabu restaurant. Experience the highest quality Japanese beef prepared at your table in traditional style with impeccable service.",
                        },
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
                {
                    "date": "2025-04-25",
                    "schedule": [
                        {
                            "start_time": "08:30",
                            "end_time": "10:00",
                            "activity": "Breakfast at Hyatt Regency Tokyo's Café du Parc",
                            "description": "Enjoy an elegant breakfast with city views at this sophisticated hotel restaurant. Choose from an extensive international buffet featuring both Western and Japanese dishes, fresh pastries, and made-to-order eggs.",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "12:30",
                            "activity": "Explore Akihabara",
                            "description": "Discover Japan's electronics and anime culture center, exploring multi-story electronics stores, anime shops, and maid cafes. Experience the unique atmosphere of this otaku culture mecca and hunt for rare collectibles.",
                        },
                        {
                            "start_time": "13:00",
                            "end_time": "15:00",
                            "activity": "Lunch at Yakiniku Jumbo Hanare",
                            "description": "Experience premium Japanese BBQ at this acclaimed yakiniku restaurant. Savor the finest cuts of Japanese beef grilled at your table, accompanied by fresh vegetables and signature dipping sauces.",
                        },
                        {
                            "start_time": "16:00",
                            "end_time": "18:00",
                            "activity": "Night views at Roppongi Hills Mori Tower",
                            "description": "Enjoy panoramic views of Tokyo from the observation deck of this 54-story landmark. Visit the Mori Art Museum and the Sky Deck for unobstructed views of Tokyo Tower and Mount Fuji on clear days.",
                        },
                        {
                            "start_time": "19:30",
                            "end_time": "21:30",
                            "activity": "Dinner at Tempura Kondo",
                            "description": "Savor exquisite tempura at this Michelin-starred restaurant where master chefs prepare each piece with precision timing and temperature control. Watch as seasonal ingredients are transformed into perfectly crispy morsels.",
                        },
                    ],
                    "hotel": {"name": "Park Hyatt Tokyo"},
                },
                {
                    "date": "2025-04-26",
                    "schedule": [
                        {
                            "start_time": "08:30",
                            "end_time": "10:00",
                            "activity": "Breakfast at Blue Bottle Coffee Kyoto Café",
                            "description": "Start your day with artisanal coffee and pastries at this renowned American coffee roaster's Japanese outpost. Enjoy carefully crafted pour-over coffee and fresh pastries in a minimalist, contemporary setting.",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "12:00",
                            "activity": "Visit Tokyo National Museum",
                            "description": "Explore Japan's oldest and largest art museum, housing an extensive collection of Japanese art and antiquities. Discover national treasures, archaeological artifacts, and seasonal special exhibitions in the historic Ueno Park.",
                        },
                        {
                            "start_time": "12:30",
                            "end_time": "14:30",
                            "activity": "Lunch at Tapas Molecular Bar",
                            "description": "Experience innovative molecular gastronomy at this unique counter restaurant. Watch as chefs create avant-garde dishes using scientific techniques, presenting a multi-course menu that engages all your senses.",
                        },
                        {
                            "start_time": "17:00",
                            "end_time": "20:00",
                            "activity": "Dinner cruise on yakatabune boat",
                            "description": "Enjoy traditional Japanese cuisine while cruising Tokyo Bay on a traditional wooden boat. Take in the illuminated skyline while savoring seasonal kaiseki dishes and unlimited drinks in this uniquely Japanese dining experience.",
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
                            "start_time": "08:00",
                            "end_time": "10:00",
                            "activity": "Breakfast at Café Kitsuné Aoyama",
                            "description": "Start your day at this trendy French-Japanese café, known for its fashion brand connection and excellent coffee. Enjoy specialty coffee drinks and French-inspired pastries in a stylish setting in the fashionable Aoyama district.",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "12:00",
                            "activity": "Tour Imperial Palace East Gardens",
                            "description": "Explore the beautiful gardens of Japan's Imperial Palace, featuring meticulously maintained Japanese gardens, historic guard houses, and ancient castle ruins. Learn about Japan's imperial history while enjoying seasonal flowers and architecture.",
                        },
                        {
                            "start_time": "12:30",
                            "end_time": "14:30",
                            "activity": "Lunch at Maisen Omotesando",
                            "description": "Enjoy Japan's best tonkatsu in a historic setting, housed in a former public bathhouse. Savor perfectly crispy breaded pork cutlets served with unlimited cabbage, rice, and their famous tonkatsu sauce.",
                        },
                        {
                            "start_time": "15:00",
                            "end_time": "17:00",
                            "activity": "Browse Harajuku and Omotesando boutiques",
                            "description": "Explore Tokyo's fashion and design district, from avant-garde designer boutiques on Omotesando to youth fashion on Takeshita Street. Experience the contrast between high fashion and street culture in this vibrant area.",
                        },
                        {
                            "start_time": "19:00",
                            "end_time": "21:00",
                            "activity": "Dinner at Quintessence",
                            "description": "Experience French-Japanese fusion at this 3-Michelin starred restaurant led by Chef Shuzo Kishida. Enjoy innovative cuisine that combines French techniques with Japanese ingredients and aesthetics in an intimate setting.",
                        },
                    ],
                    "hotel": {"name": "Hotel Chinzanso Tokyo"},
                },
                {
                    "date": "2025-04-25",
                    "schedule": [
                        {
                            "start_time": "08:30",
                            "end_time": "10:00",
                            "activity": "Breakfast at Sarabeth's Shinjuku",
                            "description": "Enjoy classic American breakfast with a Japanese twist...",
                        },
                        {
                            "start_time": "10:00",
                            "end_time": "12:30",
                            "activity": "Explore Ryogoku and Sumo Museum",
                            "description": "Learn about Japan's national sport in its spiritual home...",
                        },
                        {
                            "start_time": "12:30",
                            "end_time": "14:30",
                            "activity": "Lunch at Irokawa (Unagi)",
                            "description": "Savor traditional grilled eel at this century-old restaurant...",
                        },
                        {
                            "start_time": "15:00",
                            "end_time": "17:00",
                            "activity": "Stroll through Yanaka Ginza",
                            "description": "Experience the atmosphere of old Tokyo in this historic shopping street...",
                        },
                        {
                            "start_time": "19:30",
                            "end_time": "21:30",
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
                            "start_time": "08:00",
                            "end_time": "09:00",
                            "activity": "Breakfast at Grain Bar",
                            "description": "Start your day with healthy, grain-based breakfast...",
                        },
                        {
                            "start_time": "09:00",
                            "end_time": "13:00",
                            "activity": "Day trip and hike at Mt. Takao",
                            "description": "Enjoy a scenic hike with beautiful views of Mt. Fuji...",
                        },
                        {
                            "start_time": "13:00",
                            "end_time": "14:30",
                            "activity": "Lunch at Yakuo-In Temple",
                            "description": "Experience traditional Buddhist vegetarian cuisine...",
                        },
                        {
                            "start_time": "16:00",
                            "end_time": "18:00",
                            "activity": "Spa retreat at Mandarin Oriental Spa Tokyo",
                            "description": "Relax with traditional Japanese treatments and city views...",
                        },
                        {
                            "start_time": "19:00",
                            "end_time": "21:00",
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
