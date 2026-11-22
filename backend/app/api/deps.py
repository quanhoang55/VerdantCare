# ==========================================================================
# PURPOSE: DEPENDENCY
# ==========================================================================
# IMPORTS & MODULE LOADING
# ==========================================================================

from typing import Annotated

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.error import ForbiddenError, UnauthorizedError
from app.models.user import AuthenticatedUser
from app.services.auth import auth_service

# ==========================================================================
# Config this part base on services i use
# Change how credentials/tokens arrive if your provider uses cookies, custom
# headers, or a different scheme instead of `Authorization: Bearer <token>`.
# ==========================================================================
bearer_scheme = HTTPBearer(auto_error=False)


async def _extract_bearer_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> str | None:
    if credentials is None or credentials.scheme.lower() != "bearer":
        return None
    return credentials.credentials


# ==========================================================================
# ==========================================================================


async def get_current_user(
    token: Annotated[str | None, Depends(_extract_bearer_token)],
) -> AuthenticatedUser:
    if not token:
        raise UnauthorizedError("Missing or malformed Bearer token")

    return auth_service.verify_token(token)


async def get_optional_user(
    token: Annotated[str | None, Depends(_extract_bearer_token)],
) -> AuthenticatedUser | None:
    """For routes that work for strangers, but personalize behavior if logged in."""
    if not token:
        return None
    return auth_service.verify_token(token)


def require_role(*allowed_roles: str):
    """Optional role guard on top of an authenticated user."""

    # ==========================================================================
    # Config this part base on services i use
    # Adjust role/claim checking here if your provider stores roles in custom
    # claims, app_metadata, or a separate database table.
    # ==========================================================================
    async def _role_guard(
        current_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    ) -> AuthenticatedUser:
        if current_user.role not in allowed_roles:
            raise ForbiddenError("Insufficient permissions")
        return current_user

    # ==========================================================================
    # ==========================================================================

    return _role_guard
