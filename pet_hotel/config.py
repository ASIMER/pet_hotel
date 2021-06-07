import os


class Config:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.environ.get(
                "SQLALCHEMY_DATABASE_URI")
        self.SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
                "SQLALCHEMY_TRACK_MODIFICATIONS")
