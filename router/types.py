from flask_sqlalchemy import SQLAlchemy
from typing import Callable, Any
from flask import Flask

Route = Callable[[Flask, SQLAlchemy, Any], None]

ErrorHandler = Callable[[Flask], None]
