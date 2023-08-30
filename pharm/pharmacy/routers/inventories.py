from typing import Sequence

from fastapi import APIRouter, status
from fastapi import HTTPException
from sqlalchemy import exc, select

from pharmacy.database.models.inventories import Inventory
from pharmacy.dependencies.database import AnnotatedInventory, Database
from pharmacy.schema.inventories import InventoryCreate, InventorySchema

router = APIRouter()


@router.post("/inventories", response_model=InventorySchema)
def create_inventory(inventory_data: InventoryCreate, db: Database) -> Inventory:
    inventory = Inventory(**inventory_data.model_dump())
    try:
        db.add(inventory)
        db.commit()
        db.refresh(inventory)

        return inventory
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inventory already exists"
        )


@router.get("/inventories", response_model=list[InventorySchema])
def get_list_of_inventories(db: Database) -> Sequence[Inventory]:
    return db.scalars(select(Inventory)).all()


@router.get("/inventories/{inventory_id}", response_model=InventorySchema)
def get_inventory(inventory: AnnotatedInventory) -> Inventory:
    return inventory


@router.delete("/inventories/{inventory_id}")
def delete_inventory(inventory: AnnotatedInventory, db: Database) -> None:
    db.delete(inventory)
    db.commit()
