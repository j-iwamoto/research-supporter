"""日報API"""

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.core.auth import get_current_user
from app.models.log import LogCreate, LogListResponse, LogResponse
from app.services.ai_service import ai_service
from app.services.firestore_service import firestore_service

router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.post("", response_model=LogResponse, status_code=201)
async def create_log(
    log_in: LogCreate,
    current_user: dict = Depends(get_current_user),
) -> LogResponse:
    """日報を作成する

    1. AIで日報を自動分類（category, tags）
    2. Firestoreに保存
    """
    user_id: str = current_user["uid"]

    # AI分類
    classification = await ai_service.classify_log(log_in.content)

    # Firestoreに保存
    data = {
        "content": log_in.content,
        "category": classification["category"],
        "tags": classification["tags"],
    }
    doc = await firestore_service.create_log(user_id, data)
    return LogResponse(**doc)


@router.get("", response_model=LogListResponse)
async def list_logs(
    week_of: str | None = Query(None, description="対象週 (例: 2026-W15)"),
    category: str | None = Query(None, description="カテゴリでフィルタ"),
    limit: int = Query(50, ge=1, le=200, description="最大取得件数"),
    current_user: dict = Depends(get_current_user),
) -> LogListResponse:
    """日報一覧を取得する (week_of, category でフィルタ可)"""
    user_id: str = current_user["uid"]
    logs = await firestore_service.get_logs(
        user_id, week_of=week_of, category=category, limit=limit
    )
    return LogListResponse(
        logs=[LogResponse(**log) for log in logs],
        total=len(logs),
    )


@router.get("/{log_id}", response_model=LogResponse)
async def get_log(
    log_id: str,
    current_user: dict = Depends(get_current_user),
) -> LogResponse:
    """日報を1件取得する"""
    user_id: str = current_user["uid"]
    doc = await firestore_service.get_log(user_id, log_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return LogResponse(**doc)


@router.put("/{log_id}", response_model=LogResponse)
async def update_log(
    log_id: str,
    log_in: LogCreate,
    current_user: dict = Depends(get_current_user),
) -> LogResponse:
    """日報を編集する（content更新→再分類）

    1. 既存ログの存在を確認
    2. AIで再分類
    3. Firestoreを更新
    """
    user_id: str = current_user["uid"]

    # 存在チェック
    existing = await firestore_service.get_log(user_id, log_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Log not found")

    # 新しいcontentでAI再分類
    classification = await ai_service.classify_log(log_in.content)

    # 更新データ
    update_data = {
        "content": log_in.content,
        "category": classification["category"],
        "tags": classification["tags"],
    }
    updated = await firestore_service.update_log(user_id, log_id, update_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return LogResponse(**updated)


@router.delete("/{log_id}", status_code=204)
async def delete_log(
    log_id: str,
    current_user: dict = Depends(get_current_user),
) -> Response:
    """日報を削除する"""
    user_id: str = current_user["uid"]
    deleted = await firestore_service.delete_log(user_id, log_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Log not found")
    return Response(status_code=204)
