from fastapi import APIRouter, status
from fastapi import HTTPException
from sqlalchemy import exc, select

from pharmacy.database.core import SessionMaker
from pharmacy.database.models.users import User
from pharmacy.schema.users import UserCreate, UserSchema
from pharmacy.dependencies.database import AnnotatedUser, Database


router = APIRouter()


@router.post("/users/", response_model=UserSchema)
def create_user(user_data: UserCreate, db: Database) -> User:
    user = User(**user_data.model_dump())
    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )


@router.get("/users/", response_model=list[UserSchema])
def get_list_of_users(db: Database) -> list[User]:
    return db.scalars(select(User)).all()


@router.get("/users/{user_id}", response_model=UserSchema)
def get_user(user: AnnotatedUser) -> User:
    return user


@router.delete("/users/{user_id}")
def delete_user(user: AnnotatedUser, db: Database) -> None:
    db.delete(user)
    db.commit()
