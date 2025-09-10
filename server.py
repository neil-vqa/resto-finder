import logging
import logging.config

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from resto_finder import exceptions, logging_config, services

logger = logging.getLogger(__name__)

middleware = [
    Middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )
]


async def getting_place_error(request: Request, exc: exceptions.GetPlaceFromFSQError):
    return JSONResponse({"result": str(exc)}, status_code=200)


async def call_llm_error(request: Request, exc: exceptions.LLMCallError):
    return JSONResponse({"detail": str(exc)}, status_code=500)


async def parsing_error(request: Request, exc: exceptions.ParseQueryError):
    return JSONResponse({"detail": "Error parsing LLM response."}, status_code=500)


exception_handlers = {
    exceptions.GetPlaceFromFSQError: getting_place_error,
    exceptions.LLMCallError: call_llm_error,
    exceptions.ParseQueryError: parsing_error,
}

app = Starlette(middleware=middleware, exception_handlers=exception_handlers)


@app.route("/api/execute", methods=["GET"])
async def exec_request(request: Request):
    message = request.query_params["message"]
    auth_code = request.query_params.get("code", None)

    if auth_code != "pioneerdevai":
        return JSONResponse({"results": "You are not allowed here."}, status_code=401)

    p = services.parse_query(query=message)
    place = services.get_from_fsq(params=p)
    return JSONResponse({"result": place})


if __name__ == "__main__":
    import uvicorn

    logging.config.dictConfig(logging_config.logging_conf)

    uvicorn.run(app, host="0.0.0.0", port=8000)
