import json

from resto_finder import core


def parse_query(query):
    res = core.call_llm(query)
    q = json.loads(res.choices[0].message.content)
    params = q["parameters"]
    params["min_price"] = params["price"]
    return params


def get_from_fsq(params):
    places = core.get_places(params)
    target_place_id = places["results"][0]["fsq_place_id"]
    place = core.get_place(place_id=target_place_id)

    res = {
        "name": place["name"],
        "address": place["location"]["formatted_address"],
    }

    return res
