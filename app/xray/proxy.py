from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas


def get_user_connections(username: str) -> int:
    """
    This function simulates getting the number of active connections for a user.
    In a real application, this would likely involve querying a database or other
    connection tracking mechanism.  For this example, it returns a placeholder value.
    """
    # Replace this with actual connection counting logic
    return 0


def validate_user(db: Session, username: str) -> schemas.UserResponse:
    dbuser = crud.get_user(db, username=username)
    if not dbuser:
        raise HTTPException(status_code=404, detail="User not found")

    # Check concurrent connections
    active_connections = get_user_connections(username)
    if dbuser.concurrent_connections and active_connections >= dbuser.concurrent_connections:
        raise HTTPException(status_code=429, detail="Maximum concurrent connections reached")

    return schemas.UserResponse(id=dbuser.id, username=dbuser.username)