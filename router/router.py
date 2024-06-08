from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from typing import Any


from .types import Route, ErrorHandler

class Router():

    def __init__(self, app: Flask, db: SQLAlchemy):
        self.db = db
        self.app = app
        

    def register_route(self, route: Route) -> None:
        route(self.app, self.db) # type: ignore

    def register_error_handler(self, handler: ErrorHandler) -> None:
        handler(self.app)