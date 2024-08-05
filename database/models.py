from database.base import base
import sqlalchemy as db


class User(base):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(length=100), unique=True, nullable=False)
    score = db.Column("score", db.Integer, default=0, nullable=False)
