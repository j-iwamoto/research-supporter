"""Firebase Auth JWT検証ミドルウェア"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Firebase Auth のIDトークンを検証し、ユーザー情報を返す依存関数。

    Returns:
        dict: uid, email 等を含むユーザー情報
    """
    # TODO: firebase_admin.auth.verify_id_token を使った検証を実装
    # token = credentials.credentials
    # try:
    #     decoded = firebase_admin.auth.verify_id_token(token)
    #     return {"uid": decoded["uid"], "email": decoded.get("email", "")}
    # except Exception:
    #     raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 開発用: トークン検証をスキップしてダミーユーザーを返す
    return {"uid": "dev-user-001", "email": "dev@example.com"}
