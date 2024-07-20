from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from .routes import main_router
import logging


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

app = FastAPI()
app.include_router(main_router)
app.add_middleware(SessionMiddleware, secret_key='test')
