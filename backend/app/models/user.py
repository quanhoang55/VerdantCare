# ==========================================================================
# PURPOSE: USER MODELS
# ==========================================================================
# IMPORTS & MODULE LOADING
# ==========================================================================
from typing import Any

from pydantic import BaseModel

# ==========================================================================
# CLASSES / DATA STRUCTURE: AuthenticatedUser
# ==========================================================================


class AuthenticatedUser(BaseModel):
    id: str
    email: str | None = None
    role: str = "authenticated"
    # ==========================================================================
    # Config this part base on services i use
    # Add provider-specific fields here if needed (e.g., email_verified,
    # provider, custom_claims) when adapting to Supabase, Firebase, etc.
    # ==========================================================================
    raw_claims: dict[str, Any] | None = None
    # ==========================================================================
    # ==========================================================================
