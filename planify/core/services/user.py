from planify.core.interfaces.dal.user import UserCreator
from planify.core.models import dto


async def create_user(user: dto.User, hashed_password: str, dao: UserCreator) -> dto.User:
    created_user = await dao.create(user.add_password(hashed_password))
    await dao.commit()
    return created_user
