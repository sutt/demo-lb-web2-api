from fastapi import FastAPI

from .user import di_user


def setup_dependencies(app: FastAPI):
    di_user(app)