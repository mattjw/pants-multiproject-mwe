import logging
import os
import sys
from subprocess import run

import uvicorn
from fastapi import FastAPI
from numerics.pi import monte_carlo

LOGGER = logging.getLogger(__name__)
APP = FastAPI()


@APP.get("/")
async def root():
    return {"monte-carlo-pie": monte_carlo()}


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", "8096"))
    HOST = "127.0.0.1"

    SERVER = f"http://{HOST}:{PORT}"
    LOGGER.info(f"Server: {SERVER}/")
    LOGGER.info(f"API documentation: {SERVER}/docs or {SERVER}/redoc")

    if len(sys.argv) > 1 and sys.argv[1] == "--reload":
        run(
            [
                "uvicorn",
                "--debug",
                "--reload",
                "--host",
                HOST,
                "--port",
                str(PORT),
                "main:APP",
            ],
            check=False,
        )
    else:
        uvicorn.run(APP, host=HOST, port=PORT, debug=True)
