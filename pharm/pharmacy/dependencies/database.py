from typing_extensions import Annotated

from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from pharmacy.database.core import SessionMaker
from pharmacy.database.models.users import User


def database_connection():
    with SessionMaker() as db_connection:
        yield db_connection


Database = Annotated[Session, Depends(database_connection)]


def get_user_or_404(db: Database, user_id: int) -> User:
    user: User | None = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


AnnotatedUser = Annotated[User, Depends(get_user_or_404)]
