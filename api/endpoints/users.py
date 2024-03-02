from fastapi import APIRouter
from pydantic import BaseModel

from db.models import User
from db.session import SessionLocal

router = APIRouter()
db = SessionLocal()


class CreateUser(BaseModel):
    username: str
    name: str
    password: str


class GetUser(BaseModel):
    username: str


@router.post('/create')
async def create_user(user: CreateUser) -> dict:
    new_user = User(
        username=user.username,
        name=user.name,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'message': 'User created'}


@router.get('/{username}')
async def get_user_data(username: str) -> dict:
    user = db.query(User).filter(User.username == username).first()
    if user:
        return {'user_id': user.id, 'username': user.username, 'name': user.name}
    else:
        return {'message': 'User not found'}

