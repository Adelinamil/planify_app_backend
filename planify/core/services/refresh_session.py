from uuid import UUID

from planify.common import dt_utils
from planify.core.interfaces.dal.refresh_session import RefreshSessionCreator, RefreshSessionVerifier
from planify.core.models import dto
from planify.core.utils.exceptions import SessionExpired, InvalidRefreshSession


async def add_refresh_session(
    refresh_session: dto.RefreshSession,
    dao: RefreshSessionCreator,
    max_refresh_sessions_count: int,
) -> dto.RefreshSession:
    if await dao.count_by_user_id(refresh_session.user_id) >= max_refresh_sessions_count:
        await dao.remove_oldest_by_user_id(refresh_session.user_id)

    new_refresh_session = await dao.create(refresh_session)
    return new_refresh_session


async def verify_refresh_session(
    refresh_session_id: UUID,
    new_fingerprint: UUID,
    dao: RefreshSessionVerifier,
) -> dto.RefreshSession:
    old_refresh_session = await dao.get_by_id(refresh_session_id)
    if dt_utils.now() > old_refresh_session.expires_in:
        raise SessionExpired
    if old_refresh_session.fingerprint != new_fingerprint:
        raise InvalidRefreshSession

    await dao.remove_by_id(old_refresh_session.id)
    return old_refresh_session
