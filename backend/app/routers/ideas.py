"""アイデアAPI"""

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.models.idea import IdeaCreate, IdeaListResponse, IdeaResponse, IdeaUpdate

router = APIRouter(prefix="/api/ideas", tags=["ideas"])


@router.post("", response_model=IdeaResponse, status_code=201)
async def create_idea(
    idea_in: IdeaCreate,
    current_user: dict = Depends(get_current_user),
):
    """アイデアを作成する"""
    # TODO: Firestore に保存
    raise NotImplementedError


@router.get("", response_model=IdeaListResponse)
async def list_ideas(
    status: str | None = None,
    tag: str | None = None,
    current_user: dict = Depends(get_current_user),
):
    """アイデア一覧を取得する (status, tag でフィルタ可)"""
    # TODO: Firestore から取得
    raise NotImplementedError


@router.get("/{idea_id}", response_model=IdeaResponse)
async def get_idea(
    idea_id: str,
    current_user: dict = Depends(get_current_user),
):
    """アイデアを1件取得する"""
    # TODO: Firestore から取得
    raise NotImplementedError


@router.put("/{idea_id}", response_model=IdeaResponse)
async def update_idea(
    idea_id: str,
    idea_in: IdeaUpdate,
    current_user: dict = Depends(get_current_user),
):
    """アイデアを更新する"""
    # TODO: Firestore を更新
    raise NotImplementedError


@router.delete("/{idea_id}", status_code=204)
async def delete_idea(
    idea_id: str,
    current_user: dict = Depends(get_current_user),
):
    """アイデアを削除する"""
    # TODO: Firestore から削除
    raise NotImplementedError
