"""週報API"""

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.models.weekly import (
    WeeklyGenerateRequest,
    WeeklyListResponse,
    WeeklyReportResponse,
    WeeklyUpdateRequest,
)
from app.services.ai_service import ai_service
from app.services.firestore_service import firestore_service

router = APIRouter(prefix="/api/weekly", tags=["weekly"])


@router.post("/generate", response_model=WeeklyReportResponse, status_code=201)
async def generate_weekly_report(
    req: WeeklyGenerateRequest,
    current_user: dict = Depends(get_current_user),
):
    """対象週の日報からAIで週報を自動生成する"""
    user_id: str = current_user["uid"]

    # 対象週のログを取得
    logs = await firestore_service.get_logs(user_id, week_of=req.week_of)

    # AIで週報を生成
    report_content = await ai_service.generate_weekly_report(logs, req.week_of)

    # Firestoreに保存
    data = {
        "week_of": req.week_of,
        "this_week": report_content["this_week"],
        "next_week": report_content["next_week"],
    }
    doc = await firestore_service.save_weekly_report(user_id, data)
    return WeeklyReportResponse(**doc)


@router.get("", response_model=WeeklyListResponse)
async def list_weekly_reports(
    current_user: dict = Depends(get_current_user),
):
    """週報一覧を取得する（week_of降順）"""
    user_id: str = current_user["uid"]
    reports = await firestore_service.get_weekly_reports(user_id)
    return WeeklyListResponse(
        reports=[WeeklyReportResponse(**r) for r in reports],
        total=len(reports),
    )


@router.get("/{week_of}", response_model=WeeklyReportResponse)
async def get_weekly_report(
    week_of: str,
    current_user: dict = Depends(get_current_user),
):
    """指定週の週報を取得する"""
    user_id: str = current_user["uid"]
    doc = await firestore_service.get_weekly_report(user_id, week_of)
    if doc is None:
        raise HTTPException(status_code=404, detail="Weekly report not found")
    return WeeklyReportResponse(**doc)


@router.put("/{week_of}", response_model=WeeklyReportResponse)
async def update_weekly_report(
    week_of: str,
    req: WeeklyUpdateRequest,
    current_user: dict = Depends(get_current_user),
):
    """週報を手動で編集する"""
    user_id: str = current_user["uid"]
    data = {}
    if req.this_week is not None:
        data["this_week"] = req.this_week
    if req.next_week is not None:
        data["next_week"] = req.next_week

    doc = await firestore_service.update_weekly_report(user_id, week_of, data)
    if doc is None:
        raise HTTPException(status_code=404, detail="Weekly report not found")
    return WeeklyReportResponse(**doc)
