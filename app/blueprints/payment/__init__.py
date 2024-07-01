from flask import Blueprint

payment = Blueprint("payment", __name__)
from .create_route import *
from .callback_route import *
