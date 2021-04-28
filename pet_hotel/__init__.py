from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from .config import Config
from .middleware import Middleware
from .models import db
from .routes import ActivityList, EmptyRooms, MainPage, PetsEviction, \
    PetsSettlement


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.wsgi_app = Middleware(app.wsgi_app)
    api = Api(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    api.add_resource(MainPage, "/")
    api.add_resource(EmptyRooms, "/empty_rooms")
    api.add_resource(PetsSettlement, "/pets_settlement")
    api.add_resource(PetsEviction, "/pets_eviction")
    api.add_resource(ActivityList, "/activity_list")

    return app
