import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
import webbrowser

from main import control_router, mail_router
import config


def configure():
    # create instance of the app
    app = FastAPI(title="multi_sender")

    # create the instance for the routes
    main_api_router = APIRouter()

    # set routes to the app instance
    main_api_router.include_router(mail_router, prefix="/mail", tags=["mails"])
    main_api_router.include_router(control_router, prefix="/control", tags=["ui", "controls"])

    app.include_router(main_api_router)
    app.mount("/static", config.static_files, name="static")


    origins = [
        config.get_server_url(),
        f"ws://{config.server_host}:{config.server_port}",
    ]

    app = CORSMiddleware(
        app=app,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


def open_control_page():
    url = f"{config.get_server_url()}/control"
    webbrowser.open(url)


def main(name=None, port=None):
    config.server_port = port or config.server_port
    config.name = name or config.anme
    app = configure()
    open_control_page()
    uvicorn.run(app, host=config.server_host, port=config.server_port)


if __name__ == "__main__":
    # run app on the host and port
    main()