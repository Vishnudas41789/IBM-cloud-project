import requests
import json

# Your credentials
api_key = 'aiM9vTjlgX6OUN64uykslQVcrDFlaCbx3yk9Pd1Ouu6H'
project_id = '17c387f1-7052-4af9-b8ee-886c8a6d86b9'
url = 'https://api.eu-gb.assistant.watson.cloud.ibm.com'  # Region URL (EU GB)

# IAM token endpoint
iam_url = 'https://iam.cloud.ibm.com/identity/token'

# Prepare headers and data
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = f'grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}'

# Get token
res = requests.post(iam_url, headers=headers, data=data)
iam_token = res.json().get('access_token')

if iam_token:
    print("✅ Token received")
else:
    print("❌ Token Error:", res.json())
import random

# Nutrition responses
nutrition_responses = [
    "Try oats, fruits, or paneer for dinner.",
    "How about grilled chicken with brown rice?",
    "Include leafy greens like spinach in your lunch.",
    "Snack on almonds or walnuts during the day.",
    "Drink plenty of water and avoid sugary drinks.",
    "A banana and peanut butter is a great pre-workout snack.",
    "Avoid heavy meals before bedtime.",
    "For breakfast, try eggs with whole grain toast.",
    "Have a bowl of dal and roti with veggies.",
    "Add more fiber to your diet using chia seeds and flaxseeds.",
    "Try tofu stir fry with broccoli and bell peppers.",
    "Greek yogurt with berries is a good post-dinner snack.",
    "Cut down on fried food and choose baked or steamed items.",
    "Avocados are great for healthy fats.",
    "Start your day with a fruit smoothie.",
    "Boiled eggs and sprouts make a protein-packed snack.",
    "Switch from white rice to quinoa or brown rice.",
    "Add carrots, cucumbers, and tomatoes to your lunch plate.",
    "Hydrate with coconut water after exercise.",
    "Limit salt and processed food intake."
]
# Extract keywords
nutrition_keywords = set()
for response in nutrition_responses:
    words = response.lower().replace(".", "").replace("?", "").split()
    nutrition_keywords.update(words)

# Chat input options
general_chats = [
    "Hi", "Hello", "What's your name?", "How are you?", "Tell me something",
    "Give me food", "oats", "brown rice", "protein", "healthy", "I’m tired", "Dinner?",
    "water", "I want food", "Suggest something", "paneer?", "banana", "toast", "fat",
    "morning", "evening", "try", "eat", "snack", "rice", "dal", "veggies", "help me",
    "hungry", "drink", "fruits", "meal", "eggs", "nuts", "fiber", "oil", "grill"
]

# Generate 10,000 messages and responses
for i in range(1, 10001):
    msg = random.choice(general_chats)
    msg_words = msg.lower().replace("?", "").replace(".", "").split()

    if any(word in nutrition_keywords for word in msg_words):
        response = random.choice(nutrition_responses)
        print(f"{i}. 🟢 You: {msg}")
        print(f"   🥗 NutritionBot: {response}")
    else:
        print(f"{i}. 🟢 You: {msg}")
        print("   🤖 NutritionBot: Hi there! How can I help you today?")