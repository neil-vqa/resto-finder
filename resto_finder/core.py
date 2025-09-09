import os

import openai
import requests
from dotenv import load_dotenv

load_dotenv()

llm_server_url = os.getenv("LLM_SERVER_URL")
llm_api_key = os.getenv("LLM_API_KEY")
foursquare_key = os.getenv("FOURSQUARE_API_KEY")


llm_client = openai.OpenAI(base_url=llm_server_url, api_key=llm_api_key)


def call_llm(query):
    res_schema = {
        "title": "Restaurant Search",
        "type": "object",
        "properties": {
            "action": {"type": "string", "const": "restaurant_search"},
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "type of place or category of the place to look for",
                    },
                    "near": {
                        "type": "string",
                        "description": "possible location of the place hinted from the query",
                    },
                    "price": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 4,
                        "description": "Valid price range between 1 (most affordable) to 4 (most expensive). The price is possibly hinted in the query by keywords. This is different from rating which is from 0 to 10.",
                    },
                    "open_now": {
                        "type": "boolean",
                        "description": "The value is possibly hinted in the query by keywords.",
                    },
                },
                "required": ["query", "near", "price"],
            },
        },
        "required": ["action", "open_now", "parameters"],
    }

    prompt = """
    Given a user's query, extract the needed information according to the JSON schema provided. Output format should be according to the JSON schema.

<query>
{query}
</query>

<json-schema>
{target_schema}
</json-schema>
"""

    res = llm_client.chat.completions.create(
        model="local_llm",
        messages=[
            {
                "role": "system",
                "content": "You are an information extraction agent. You ALWAYS respond in JSON.",
            },
            {
                "role": "user",
                "content": prompt.format(query=query, target_schema=res_schema),
            },
        ],
        max_tokens=2048,
        temperature=0.2,
        response_format={"type": "json_object", "schema": res_schema},
    )

    return res


def get_places(params):
    url = "https://places-api.foursquare.com/places/search"

    headers = {
        "accept": "application/json",
        "X-Places-Api-Version": "2025-06-17",
        "authorization": f"Bearer {foursquare_key}",
    }

    params["sort"] = "RELEVANCE"

    response = requests.get(url, headers=headers, params=params)

    return response.json()


def get_place(place_id):
    url = f"https://places-api.foursquare.com/places/{place_id}"

    headers = {
        "accept": "application/json",
        "X-Places-Api-Version": "2025-06-17",
        "authorization": f"Bearer {foursquare_key}",
    }

    response = requests.get(url, headers=headers)

    return response.json()
