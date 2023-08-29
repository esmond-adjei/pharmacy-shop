from fastapi import APIRouter, status
from fastapi import HTTPException
import sqlalchemy.exc

from pharamcy.database.models.users import User
from pharmacy.database.core import SessionMaker
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
