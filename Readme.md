# How to setup?

## Setup

```sh
git clone https://github.com/username/Walmart-AI-Seller.git
```

```sh
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

### Walmart Chatbot

#### Prerequisites

- Python 3.9+

- Google API credentials (for Calendar, Contacts, and Gmail access)

- Tavily API key (for web search)

- Groq API key (for Llama3)

- Google Gemini API key (for using the Gemini model)

- Deepgram API key (for voice processing)

- Necessary Python libraries (listed in `requirements.txt`)


```sh
cd walmart chatbot
pip install -r requirements.txt
```

```sh
pip install -r requirements.txt
```

Create a `.env` file in the root directory of the project and add your API keys:

```env
GOOGLE_API_KEY=your_google_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

Follow Google's documentation to set up credentials for Calendar, Contacts, and Gmail APIs. Save the credentials file in a secure location and update the path in the configuration file.


```sh
python main.py
```

The assistant is programmed to stop the conversation when the user says "goodbye".


### Walmart Voice

#### Prerequisites

- Python 3.9+
- Calendly API key
- Stripe API key
- Groq API key
- Necessary Python libraries (listed in `requirements.txt`)


```sh
cd walmart voice
pip install -r requirements.txt
```

Create a `.env` file in the root directory of the project and add your API keys:

```env
CALENDLY_API_KEY=your_calendly_api_key
CALENDLY_EVENT_TYPE_UUID=your_calendly_event_id
STRIPE_API_KEY=your_stripe_api_key
GROQ_API_KEY=your_stripe_api_key
```

```sh
python /srcipts/create_database.py
```

```sh
python main.py
```