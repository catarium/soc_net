from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from .routes import main_router
import logging


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

app = FastAPI(root_path='/api')
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.add_middleware(SessionMiddleware, secret_key='test')

app.include_router(main_router)
