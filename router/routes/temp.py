from flask.wrappers import Response as FlaskResponse
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # type: ignore
from typing import List, cast, Any

from ..types import Route


def route_temp(app: Flask, db: SQLAlchemy) -> Route: 

    @app.get("/temp")
    def temp() -> FlaskResponse:
        #VALIDATE BODY
    

        return "Hej, du har gjort något!"
    
    return temp # type: ignore