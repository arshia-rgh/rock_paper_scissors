from typing import Type, List

from sqlalchemy.orm import Session
from database.models import User
from database.base import session
from utils.exception import UserNotExists


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Type[User]]:
        return self.db.query(User).all()

    def get_by_name(self, name: str) -> User | None:
        user = self.db.query(User).filter(User.name == name).first()
        return user if user else None

    def create(self, item: User) -> User | Exception:
        try:
            user = item
            self.db.add(item)
            self.db.commit(item)
            self.db.refresh(item)
            return user
        except Exception as e:
            return e

    def delete(self, id: int) -> bool:
        user = self.db.query(User).filter(User.id == id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        else:
            raise UserNotExists

    def update(self, item: User) -> User | Exception:
        user = self.db.query(User).filter(User.id == item.id).first()
        if user:
            try:
                user = item
                self.db.commit()
                self.db.refresh(item)
                return user
            except Exception as e:
                return e
        else:
            raise UserNotExists


user_repo = UserRepository(session)
