# 🤖 Weather Agent — LangChain + Claude

> **interview Technical Test** — An AI-powered weather agent built with LangChain and Claude (Anthropic). The agent answers real-time weather questions in natural language using the Open-Meteo API, with a punny personality.

---

## ✨ Features

- 🌦️ **Real-time weather data** — temperature, humidity, wind speed, sky conditions
- 🗺️ **City geocoding** — converts any city name to GPS coordinates via Open-Meteo Geocoding API
- 🧠 **Conversational memory** — remembers context across multiple questions in a session (`InMemorySaver`)
- 😄 **Punny responses** — the agent always answers with weather-themed puns
- 🔁 **Request caching + retry** — efficient and resilient API calls
- 🌍 **27 WMO weather codes** mapped to human-readable conditions
- 💬 **Interactive CLI** — chat loop until you type `exit`

---

## 🗂️ Project Structure

```
test-langchain/
├── PARTIE1-QUICKSTARTLANGCHAIN/
│   ├── basic agent.py          # LangChain official quickstart (mock data)
│   ├── Quickstart LangChain.pdf
│   └── Console-tuto.png        # Screenshot of Part 1 output
│
├── PARTIE2-ADAPTATIONETAMELIORATION/
│   └── OPTION-B/
│       ├── agentmeteo.py       # Full weather agent with real API data
│       ├── Console-B.png       # Screenshots of Part 2 output
│       ├── Console-B1.png
│       ├── Console-B2.png
│       └── Console-B3.png
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Python 3.10+](https://www.python.org/) | Primary language |
| [LangChain](https://www.langchain.com/) | Agent framework |
| [Claude (Anthropic)](https://www.anthropic.com/) | LLM — `claude-sonnet-4-5` |
| [LangGraph](https://www.langchain.com/langgraph) | Agent memory (`InMemorySaver`) |
| [Open-Meteo](https://open-meteo.com/) | Free weather & geocoding API |
| [openmeteo-requests](https://pypi.org/project/openmeteo-requests/) | Open-Meteo Python client |
| [requests-cache](https://pypi.org/project/requests-cache/) | HTTP response caching |
| [retry-requests](https://pypi.org/project/retry-requests/) | Automatic retry on failure |

---

## 🏗️ Architecture

### Two LangChain Tools

**`get_user_location(city)`**
- Calls the Open-Meteo Geocoding API
- Converts a city name → `LocationData(city, latitude, longitude)`
- Raises an error if the city is not found

**`get_weather_for_location(location)`**
- Calls the Open-Meteo Forecast API with cached + retried session
- Fetches `temperature_2m`, `wind_speed_10m`, `relative_humidity_2m`, `weather_code` in a single call
- Maps WMO weather codes (27 codes) to readable text
- Returns `WeatherData(temperature, wind_speed, humidity, conditions)`

### Data Structures (dataclasses)

```python
@dataclass
class LocationData:
    city: str
    latitude: float
    longitude: float

@dataclass
class WeatherData:
    temperature: float
    wind_speed: float
    humidity: float
    conditions: str

@dataclass
class ResponseFormat:
    punny_response: str               # Always present
    weather_conditions: str | None    # Structured weather info
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/aissouss/weather-agent-langchain.git
cd weather-agent-langchain

# 2. Install dependencies
pip install -r requirements.txt
```

### Configuration

Set your Anthropic API key as an environment variable:

**Windows:**
```cmd
setx ANTHROPIC_API_KEY "your-api-key-here"
```

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Run

```bash
# Part 1 — LangChain quickstart (mock data)
python "PARTIE1-QUICKSTARTLANGCHAIN/basic agent.py"

# Part 2 — Full weather agent with real data (Option B)
python PARTIE2-ADAPTATIONETAMELIORATION/OPTION-B/agentmeteo.py
```

---

## 💬 Example

```
Weather Agent (type 'exit' to quit)

You: What is the weather in Paris?

Agent: Paris is having a 'sun-sational' day — no need to be 'mist-erable'!

Données: City: Paris | Temperature: 22.3°C | Humidity: 61% | Wind: 14.2 km/h | Conditions: Partly cloudy

You: And in Tunis?

Agent: Tunis is 'clear-ly' on fire today — pun intended!

Données: City: Tunis | Temperature: 31.5°C | Humidity: 48% | Wind: 9.7 km/h | Conditions: Clear sky

You: exit
Goodbye
```

---

## ⚙️ Key Improvements (Option B)

- Migrated from `current_weather=True` + `hourly` (downloads 168h of data) to modern `current` format — fetches only what's needed in **one single API call**
- Extended WMO weather code mapping from 10 to **27 codes**
- Fixed a display bug when comparing multiple cities
- Improved system prompt for better multi-city handling
- Structured data with **dataclasses** instead of raw dictionaries

---

## 🎯 Context

This project was built as a **pre-interview technical test** assessing the ability to:
- Learn a new tool autonomously
- Follow a tutorial and get an example running
- Adapt and improve existing code

**Estimated duration:** 2–3 hours  
**Option chosen:** Option B — Enrich existing tools with real weather data

---

## 👤 Author

**Aissouss**  
[GitHub](https://github.com/aissouss)

---

## 📄 License

This project is for educational use only.
