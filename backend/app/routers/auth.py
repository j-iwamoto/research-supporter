"""認証API"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.auth import get_current_user, verify_firebase_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class VerifyRequest(BaseModel):
    """トークン検証リクエスト"""

    token: str = Field(..., description="Firebase IDトークン")


@router.post("/verify")
async def verify_token(body: VerifyRequest):
    """Firebase IDトークンを検証してユーザー情報を返す。

    フロントエンドからのログイン確認に使用。
    開発モード（DEBUG=True）ではダミーユーザーを返す。
    """
    user = verify_firebase_token(body.token)
    return user


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """認証済みユーザー情報を返す"""
    return current_user
