import json
import logging

from resto_finder import core, exceptions

logger = logging.getLogger(__name__)


def parse_query(query):
    try:
        res = core.call_llm(query)
        q = json.loads(res.choices[0].message.content)
        params = q["parameters"]
        params["min_price"] = params["price"]
    except json.JSONDecodeError:
        msg = "Error decoding a JSON-formatted string."
        logger.exception(msg)
        raise exceptions.ParseQueryError(msg) from None
    else:
        return params


def get_from_fsq(params):
    try:
        places = core.get_places(params)
        target_place_id = places["results"][0]["fsq_place_id"]
        place = core.get_place(place_id=target_place_id)

        res = {
            "name": place["name"],
            "address": place["location"]["formatted_address"],
        }
    except IndexError:
        msg = "No place found."
        raise exceptions.GetPlaceFromFSQError(msg) from None
    else:
        return res
