"""ダッシュボードAPI"""

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.services.ai_service import ai_service
from app.services.firestore_service import firestore_service

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
async def get_dashboard_summary(
    current_user: dict = Depends(get_current_user),
):
    """ダッシュボードのサマリー情報を返す。

    Returns:
        dict: 今週の日報数、アイデア統計、最新週報、AIアドバイス 等
    """
    user_id: str = current_user["uid"]

    # Firestoreから集計データを取得
    dashboard_data = await firestore_service.get_dashboard_data(user_id)

    # AIからアドバイスを生成
    suggestion = await ai_service.generate_suggestion(dashboard_data)

    # 最新の週報を取得
    reports = await firestore_service.get_weekly_reports(user_id)
    latest_report = reports[0] if reports else None

    return {
        "current_week": dashboard_data["current_week"],
        "this_week_log_count": dashboard_data["this_week_log_count"],
        "category_counts": dashboard_data["category_counts"],
        "idea_total": dashboard_data["idea_total"],
        "idea_status_counts": dashboard_data["idea_status_counts"],
        "weekly_trend": dashboard_data["weekly_trend"],
        "latest_report": latest_report,
        "suggestion": suggestion,
    }
