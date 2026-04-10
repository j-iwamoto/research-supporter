"""ダッシュボードAPI"""

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
async def get_dashboard_summary(
    current_user: dict = Depends(get_current_user),
):
    """ダッシュボードのサマリー情報を返す。

    Returns:
        dict: 今週の日報数、アイデア統計、最新週報 等
    """
    # TODO: Firestore から集計データを取得
    raise NotImplementedError
