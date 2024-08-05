from typing import Type

from sqlalchemy.orm import Session
from database.models import User
from database.base import session


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        ...

    def get_by_name(self):
        ...

    def create(self):
        ...

    def delete(self):
        ...

    def update(self):
        ...
