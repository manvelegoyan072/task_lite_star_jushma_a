from litestar import Router, get, post, put, delete, Response
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from litestar.dto import MsgspecDTO
from .models import User
from msgspec import Struct
from typing import List
from litestar.exceptions import NotFoundException

class UserCreateDTO(Struct):
    name: str
    surname: str
    password: str

class UserUpdateDTO(Struct):
    name: str | None = None
    surname: str | None = None
    password: str | None = None

class UserRepository(SQLAlchemyAsyncRepository):
    model_type = User

@post("/users", dto=MsgspecDTO[UserCreateDTO])
async def create_user(data: UserCreateDTO, repo: UserRepository) -> User:
    user = User(**data.__dict__)
    await repo.add(user)
    await repo.session.commit()
    return user

@get("/users")
async def get_users(repo: UserRepository) -> List[User]:
    return await repo.list()

@get("/users/{user_id:int}")
async def get_user(user_id: int, repo: UserRepository) -> User:
    user = await repo.get_one_or_none(id=user_id)
    if not user:
        raise NotFoundException(detail=f"User with id {user_id} not found")
    return user

@put("/users/{user_id:int}", dto=MsgspecDTO[UserUpdateDTO])
async def update_user(user_id: int, data: UserUpdateDTO, repo: UserRepository) -> User:
    user = await repo.get_one_or_none(id=user_id)
    if not user:
        raise NotFoundException(detail=f"User with id {user_id} not found")
    user_data = {k: v for k, v in data.__dict__.items() if v is not None}
    for key, value in user_data.items():
        setattr(user, key, value)
    await repo.add(user)
    await repo.session.commit()
    return user

@delete("/users/{user_id:int}")
async def delete_user(user_id: int, repo: UserRepository) -> Response:
    user = await repo.get_one_or_none(id=user_id)
    if not user:
        raise NotFoundException(detail=f"User with id {user_id} not found")
    await repo.delete(user)
    await repo.session.commit()
    return Response(status_code=204)

router = Router(path="/", route_handlers=[create_user, get_users, get_user, update_user, delete_user])