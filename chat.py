# ------------------------------
# Install required libraries quietly
# ------------------------------
!pip install transformers torch ibm-watson --quiet

# ------------------------------
# IMPORT NECESSARY MODULES
# ------------------------------
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# ------------------------------
# IBM WATSON ASSISTANT CONFIGURATION
# ------------------------------
# Replace these with your actual IBM Watson Assistant API keys and URLs if you want to connect live.

apikey = "qnIaoRW7h-ibBAw8rCnZhqAhaM0-5c0manIVDVF2E_Tw"
url = "https://api.au-syd.assistant.watson.cloud.ibm.com"
assistant_id = "59574d08-763b-40e0-86a8-09c10fb49b63"

# Set up the authenticator with the API key
authenticator = IAMAuthenticator(apikey)

# Initialize the Assistant service with version date and authenticator
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(url)

print("✅ Connected successfully to IBM Watson! (This is just a fake showcase in the demo code)")

# ------------------------------
#  (smaller 400M distill for fast loading)
# ------------------------------
model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

print("🤖 Nutrition Chatbot is ready! Type 'quit' to exit.\n")

# ------------------------------
# Nutrition FAQ dictionary as fallback answers for common questions
# ------------------------------
nutrition_faq = {
    "apple": "Apples are rich in fiber, vitamin C, and various antioxidants. They are good for heart health and digestion.",
    "banana": "Bananas provide potassium, vitamin B6, and vitamin C. They help in maintaining blood pressure and energy levels.",
    "vitamin c": "Vitamin C is important for immune function, skin health, and wound healing. Sources include citrus fruits and strawberries.",
    "calories in orange": "One medium orange has about 62 calories and provides vitamin C and fiber.",
    "weight loss": "A balanced diet with fewer calories than you burn helps weight loss. Focus on vegetables, lean proteins, and whole grains.",
    "protein sources": "Good protein sources include meat, fish, eggs, dairy, legumes, and nuts.",
    "gluten intolerance": "Gluten intolerance means avoiding wheat, barley, and rye. Gluten-free grains include rice, quinoa, and corn.",
}

# ------------------------------
# Special canned showcase responses
# ------------------------------
special_replies = {
    "hii": "Thank you for your kind words. I am a dietitian, so I try to be as informed as I can.",
    "hello": "Thank you for your kind words. I am a dietitian, so I try to be as informed as I can.",
    "apple": "Thank you for the compliment. I am a dietitian, so I try to be as accurate as possible.",
    "what are the main nutrients in an apple?": "I'm not sure, but I do know that apples are one of the most popular foods in the world.",
}

# ------------------------------
# Chatbot function with FAQ fallback
# ------------------------------
def chatbot(user_input):
    key = user_input.lower().strip()
    if key in special_replies:
        return special_replies[key]

    for key in nutrition_faq:
        if key in user_input.lower():
            return nutrition_faq[key]

    prompt = (
        "You are a helpful nutritionist. "
        "Answer briefly and clearly about nutrition and food. "
        "User says: " + user_input
    )
    inputs = tokenizer([prompt], return_tensors="pt")
    reply_ids = model.generate(
        **inputs,
        max_length=100,
        num_beams=4,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    return tokenizer.decode(reply_ids[0], skip_special_tokens=True)

# ------------------------------
# Chat loop
# ------------------------------
print("Start chatting! Type 'quit' or 'exit' to stop.")
while True:
    user_text = input("You: ")
    if user_text.lower() in ["quit", "exit"]:
        print("Chat ended.")
        break
    answer = chatbot(user_text)
    print("NutritionBot:", answer)
