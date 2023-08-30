from fastapi import APIRouter, status
from fastapi import HTTPException
from sqlalchemy import exc, select

from pharmacy.database.core import SessionMaker
from pharmacy.database.models.users import User
from pharmacy.schema.users import UserCreate, UserSchema


router = APIRouter()


@router.post("/users/", response_model=UserSchema)
def create_user(user_data: UserCreate):
    user = User(
        username=user_data.username,
        password=user_data.password,
        email=user_data.email,
        address=user_data.address,
        date_of_birth=user_data.date_of_birth
    )

    with SessionMaker() as db:
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
def get_list_of_users() -> list[User]:
    with SessionMaker() as db:
        return db.scalars(select(User)).all()


@router.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int) -> User:
    with SessionMaker() as db:
        user: User | None = db.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user