from dataclasses import dataclass

import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy


# ===============================
# 1. SYSTEM PROMPT
# ===============================
# Define system prompt
SYSTEM_PROMPT = """You are an expert weather forecaster who speaks in puns.

You have access to two tools:
- get_weather_for_location: retrieve real-time weather data for a specific geographic location
- get_user_location: use this to convert a city name into geographic coordinates

If the user asks for the weather, extract the city from the message and provide the current weather.
"""


# ===============================
# 2. DATA STRUCTURES
# ===============================
# Define location and weather data structures
@dataclass
class LocationData:
     """Geographic location data for a city."""
     city: str
     latitude: float
     longitude: float


@dataclass
class WeatherData:
     """Current weather information for a location."""
     temperature: float
     wind_speed: float
     humidity: float
     conditions: str



# Define response format
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None


# ===============================
# 3. TOOLS
# ===============================
@tool
def get_user_location(city: str) -> LocationData:
    """Convert a city name into latitude and longitude using Open-Meteo Geocoding API."""

    # Call Open-Meteo geocoding API to convert city name to coordinates
    geo_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1} # Request only 1 result
    ).json()

    # Check if the city was found in the results
    if "results" not in geo_response or not geo_response["results"]:
        raise ValueError(f"City not found: {city}")
    
    # Extract the first result
    result = geo_response["results"][0]

    # Return location data
    return LocationData(
        city=result["name"],
        latitude=result["latitude"],
        longitude=result["longitude"]
    )



@tool
def get_weather_for_location(location: LocationData) -> WeatherData:
    """Get current weather (temperature, humidity, conditions) using Open-Meteo."""
    
    # Set up cached and retried session for API calls (recuperer dans la doc de l'API)
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current_weather": True,
        "hourly": "relative_humidity_2m",
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Current weather
    current = response.Current()
    temperature = current.Variables(0).Value()
    wind_speed = current.Variables(1).Value()
    weather_code = int(current.Variables(2).Value())
    conditions = weather_code_to_text(weather_code)

    # Humidity (first hourly value = now)
    hourly = response.Hourly()
    humidity = hourly.Variables(0).ValuesAsNumpy()[0]

    #Return a WeatherData object with all information
    return WeatherData(
        temperature=temperature,
        wind_speed=wind_speed,
        humidity=humidity,
        conditions=conditions
    )

def weather_code_to_text(code: int) -> str:
    mapping = {
        0: "Sunny Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast, Cloudy",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        61: "Rain",
        71: "Snow",
        80: "Rain showers"
    }
    return mapping.get(code, "Unknown")



# ===============================
# 4. MODEL CONFIGURATION
# ===============================
model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature=0
)


# ===============================
# 5. MEMORY
# ===============================
checkpointer = InMemorySaver()


# ===============================
# 6. CREATE AGENT
# ===============================
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)


# ===============================
# 7. INTERACTIVE CONSOLE CHAT
# ===============================
# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "weather-thread-1"}}

print("Weather Agent (type 'exit' to quit)\n")
print("Vous voulez connaître la météo ? Demandez-moi !\n")

while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Goodbye")
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_message}]},
        config=config
    )
    
    # Extract structured response
    structured = response["structured_response"]

    # main response with puns
    print(f"Agent: {structured.punny_response}\n")

    # if weather data is available, print it
    if structured.weather_conditions:
        print(f"Données: {structured.weather_conditions}\n")

