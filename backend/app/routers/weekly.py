"""週報API"""

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.models.weekly import (
    WeeklyGenerateRequest,
    WeeklyReportResponse,
    WeeklyUpdateRequest,
)

router = APIRouter(prefix="/api/weekly", tags=["weekly"])


@router.post("/generate", response_model=WeeklyReportResponse, status_code=201)
async def generate_weekly_report(
    req: WeeklyGenerateRequest,
    current_user: dict = Depends(get_current_user),
):
    """対象週の日報からAIで週報を自動生成する"""
    # TODO: ai_service を使って週報生成 -> Firestore に保存
    raise NotImplementedError


@router.get("/{week_of}", response_model=WeeklyReportResponse)
async def get_weekly_report(
    week_of: str,
    current_user: dict = Depends(get_current_user),
):
    """指定週の週報を取得する"""
    # TODO: Firestore から取得
    raise NotImplementedError


@router.put("/{week_of}", response_model=WeeklyReportResponse)
async def update_weekly_report(
    week_of: str,
    req: WeeklyUpdateRequest,
    current_user: dict = Depends(get_current_user),
):
    """週報を手動で編集する"""
    # TODO: Firestore を更新
    raise NotImplementedError
