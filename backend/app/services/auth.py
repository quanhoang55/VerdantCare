# ==========================================================================
# PURPOSE: AUTHENTICATION SERVICE
# ==========================================================================
# IMPORTS & MODULE LOADING
# ==========================================================================

import jwt

from app.core.config import settings
from app.core.error import UnauthorizedError
from app.core.logging import get_logger
from app.models.user import AuthenticatedUser

# Logger
logger = get_logger(__name__)


# ==========================================================================
# CLASSES / DATA STRUCTURE: AuthService
# ==========================================================================


class AuthService:
    def verify_token(self, token: str) -> AuthenticatedUser:
        # Local development bypass only when explicitly enabled in dev env
        if (
            settings.AUTH_DEV_BYPASS
            and settings.ENV == "development"
            and token == "dev-token"
        ):
            return AuthenticatedUser(
                id=settings.AUTH_DEV_USER_ID,
                email=settings.AUTH_DEV_USER_EMAIL,
                role="authenticated",
            )

        # ==========================================================================
        # Config this part base on services i use
        # Change token verification & claim mapping here according to your auth
        # provider's docs (e.g., Supabase JWT secret/JWKS vs. Firebase Admin /
        # Google certs).
        # ==========================================================================
        if not settings.SUPABASE_JWT_SECRET:
            logger.error("SUPABASE_JWT_SECRET is not configured")
            raise UnauthorizedError("Authentication is not configured on the server")

        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
            )
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token has expired")
        except jwt.PyJWTError as exc:
            logger.warning("JWT verification failed: %s", exc)
            raise UnauthorizedError("Invalid authentication token")

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("Token is missing subject (user id)")

        return AuthenticatedUser(
            id=str(user_id),
            email=payload.get("email"),
            role=str(payload.get("role", "authenticated")),
            raw_claims=payload,
        )
        # ==========================================================================
        # ==========================================================================


auth_service = AuthService()
