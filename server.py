from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from resto_finder import services

middleware = [
    Middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )
]

app = Starlette(middleware=middleware)


@app.route("/api/execute", methods=["GET"])
async def exec_request(request: Request):
    message = request.query_params["message"]
    auth_code = request.query_params.get("code", None)

    if auth_code != "pioneerdevai":
        return JSONResponse({"results": "You are not allowed here."}, status_code=401)

    p = services.parse_query(query=message)
    place = services.get_from_fsq(params=p)
    return JSONResponse({"result": place})


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8111)
