# ==========================================================================
# PURPOSE: USER HANDLER ENDPOINT
# ==========================================================================
# IMPORTS & MODULE LOADING
# ==========================================================================


from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_optional_user
from app.models.user import AuthenticatedUser

router = APIRouter(prefix="/users", tags=["Users & Auth"])


# Public: anyone (stranger or logged-in user) can access
@router.get("/public-info")
async def public_info(
    user: Annotated[AuthenticatedUser | None, Depends(get_optional_user)],
) -> dict:
    return {
        "message": "Public endpoint",
        "authenticated": user is not None,
        "user_id": user.id if user else None,
    }


# Protected: strangers get 401 Unauthorized; signed-in users get 200 OK
@router.get("/me", response_model=AuthenticatedUser)
async def read_current_user(
    current_user: Annotated[AuthenticatedUser, Depends(get_current_user)],
) -> AuthenticatedUser:
    # ==========================================================================
    # Config this part base on services i use
    # Add provider-specific profile enrichment or response fields here if needed
    # (e.g., syncing a user profile row in Supabase/Firebase on first login).
    # ==========================================================================
    return current_user
    # ==========================================================================
    # ==========================================================================
