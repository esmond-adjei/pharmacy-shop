from typing import Sequence

from fastapi import APIRouter, status
from fastapi import HTTPException
from sqlalchemy import exc, select

from pharmacy.database.models.admins import Admin
from pharmacy.schema.admins import AdminCreate, AdminSchema
from pharmacy.dependencies.database import AnnotatedAdmin, Database


router = APIRouter()


@router.post("/admins", response_model=AdminSchema)
def create_admin(user_data: AdminCreate, db: Database) -> Admin:
    user = Admin(**user_data.model_dump())
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


@router.get("/admins", response_model=list[AdminSchema])
def get_list_of_admins(db: Database) -> Sequence[Admin]:
    return db.scalars(select(Admin)).all()


@router.get("/admins/{user_id}", response_model=AdminSchema)
def get_admin(user: AnnotatedAdmin) -> Admin:
    return user


@router.delete("/admins/{user_id}")
def delete_admin(user: AnnotatedAdmin, db: Database) -> None:
    db.delete(user)
    db.commit()
