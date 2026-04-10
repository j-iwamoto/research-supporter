"""Firebase Auth JWT検証ミドルウェア"""

import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

logger = logging.getLogger(__name__)

security = HTTPBearer()

# ダミーユーザー（開発用）
_DUMMY_USER = {"uid": "dev-user-001", "email": "dev@example.com"}


def verify_firebase_token(token: str) -> dict:
    """Firebase IDトークンを検証してユーザー情報を返す。

    Args:
        token: Firebase IDトークン文字列

    Returns:
        dict: uid, email を含むユーザー情報

    Raises:
        HTTPException: トークンが無効または期限切れの場合
    """
    if settings.DEBUG:
        # 開発モード: トークン検証をスキップしてダミーユーザーを返す
        logger.debug("DEBUG mode: skipping token verification")
        return _DUMMY_USER

    # --- 本番用: Firebase Admin SDK でのトークン検証 ---
    # import firebase_admin
    # from firebase_admin import auth as firebase_auth
    #
    # # firebase_admin の初期化（アプリ起動時に1回だけ行う想定）
    # # firebase_admin.initialize_app()
    #
    # try:
    #     decoded = firebase_auth.verify_id_token(token)
    #     return {
    #         "uid": decoded["uid"],
    #         "email": decoded.get("email", ""),
    #     }
    # except firebase_auth.ExpiredIdTokenError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Token has expired",
    #     )
    # except firebase_auth.InvalidIdTokenError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid token",
    #     )
    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Token verification failed",
    #     )

    # Firebase Admin SDK が未導入の場合のフォールバック
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Firebase Admin SDK is not configured",
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Firebase Auth のIDトークンを検証し、ユーザー情報を返す依存関数。

    Returns:
        dict: uid, email 等を含むユーザー情報
    """
    token = credentials.credentials
    return verify_firebase_token(token)
