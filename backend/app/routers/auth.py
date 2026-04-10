"""認証API"""

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """認証済みユーザー情報を返す"""
    return current_user
