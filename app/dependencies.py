

from .routes import UserRepository


async def provide_db(db_session) -> "UserRepository":
    return UserRepository(session=db_session)