import os
import requests
from dotenv import load_dotenv
import google.genai as genai
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OW_API_KEY = os.getenv("OPENWEATHER_API_KEY")

client = genai.Client()

# prompt = "hey google ! how are you ?"

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents=prompt,
# )

# print(response.text)

def fetch_weather(city:str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OW_API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def final_output(user_message: str,weather_json: dict)-> str:
    prompt = f"""
    user said: "{user_message}"
    Raw weather data: "{weather_json}"

    write a natural friendly human answer.
    Use temperature in celsius from the JSON.
    Don not show JSON. 3-4 short sentences.
    """
    response = client.models.generate_content(model="gemini-3-flash-preview",
         contents=prompt,)
    return response.text


def extract_city_from_user_question(user_question: str) -> str:
    prompt = f"""
User said: "{user_question}"         
Your Job: extract only the city name if user is asking weather.
If not waether related or city is not mentioned, return "None".
Return only the city name. NO punctuation, NO extra text.
"""
    response = client.models.generate_content(model="gemini-3-flash-preview",
     contents=prompt,)
    city = response.text.strip()
    return city

user_message = input("User: ")
city=extract_city_from_user_question(user_message)
fetched_weather = fetch_weather(city)

print(final_output(user_message,fetched_weather)
      )






                               