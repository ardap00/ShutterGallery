from flask import Blueprint

game = Blueprint('game', __name__)

from app.game import routes
