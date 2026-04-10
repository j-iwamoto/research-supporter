"""日報API"""

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.models.log import LogCreate, LogListResponse, LogResponse

router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.post("", response_model=LogResponse, status_code=201)
async def create_log(
    log_in: LogCreate,
    current_user: dict = Depends(get_current_user),
):
    """日報を作成する"""
    # TODO: Firestore に保存
    raise NotImplementedError


@router.get("", response_model=LogListResponse)
async def list_logs(
    week_of: str | None = None,
    current_user: dict = Depends(get_current_user),
):
    """日報一覧を取得する (week_of でフィルタ可)"""
    # TODO: Firestore から取得
    raise NotImplementedError


@router.get("/{log_id}", response_model=LogResponse)
async def get_log(
    log_id: str,
    current_user: dict = Depends(get_current_user),
):
    """日報を1件取得する"""
    # TODO: Firestore から取得
    raise NotImplementedError


@router.delete("/{log_id}", status_code=204)
async def delete_log(
    log_id: str,
    current_user: dict = Depends(get_current_user),
):
    """日報を削除する"""
    # TODO: Firestore から削除
    raise NotImplementedError
