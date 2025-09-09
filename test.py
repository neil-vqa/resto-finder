import json

import resto_finder


def parse_query():
    query = "Find me a cheap sushi restaurant in downtown Los Angeles that's open now and has at least a 4-star rating."
    res = resto_finder.core.call_llm(query)
    return res.choices[0].message.content


def get_from_fsq(params):
    res = resto_finder.core.get_places(params)
    return res


if __name__ == "__main__":
    res = parse_query()
    q = json.loads(res)
    params = q["parameters"]
    params["min_price"] = params["price"]
    places = get_from_fsq(params)

    target_place_id = places["results"][0]["fsq_place_id"]
    place = resto_finder.core.get_place(place_id=target_place_id)
