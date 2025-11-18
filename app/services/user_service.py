from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def create_user_service(db: Session, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        nombre=user_in.nombre,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session) -> list[User]:
    return db.query(User).all()
