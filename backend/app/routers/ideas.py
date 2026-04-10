"""アイデアAPI"""

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.auth import get_current_user
from app.models.idea import IdeaCreate, IdeaListResponse, IdeaResponse, IdeaUpdate
from app.services.ai_service import ai_service
from app.services.firestore_service import firestore_service

router = APIRouter(prefix="/api/ideas", tags=["ideas"])


@router.post("", response_model=IdeaResponse, status_code=201)
async def create_idea(
    idea_in: IdeaCreate,
    current_user: dict = Depends(get_current_user),
):
    """アイデアを作成する（AIでタグ自動付与 + 関連アイデア提案）"""
    user_id: str = current_user["uid"]

    # AIでタグを自動分類
    tags = await ai_service.classify_idea(idea_in.title, idea_in.description)

    # Firestoreに保存
    data = {
        "title": idea_in.title,
        "description": idea_in.description,
        "tags": tags,
        "status": "未着手",
        "related_ideas": [],
    }
    doc = await firestore_service.create_idea(user_id, data)

    # 関連アイデアを提案
    all_ideas = await firestore_service.get_ideas(user_id)
    related_ids = await ai_service.suggest_related_ideas(doc, all_ideas)
    if related_ids:
        doc["related_ideas"] = related_ids
        await firestore_service.update_idea(user_id, doc["id"], {"related_ideas": related_ids})

    return IdeaResponse(**doc)


@router.get("", response_model=IdeaListResponse)
async def list_ideas(
    status: str | None = Query(None, description="ステータスでフィルタ"),
    tag: str | None = Query(None, description="タグでフィルタ"),
    current_user: dict = Depends(get_current_user),
):
    """アイデア一覧を取得する (status, tag でフィルタ可)"""
    user_id: str = current_user["uid"]
    ideas = await firestore_service.get_ideas(user_id, status=status, tag=tag)
    return IdeaListResponse(
        ideas=[IdeaResponse(**idea) for idea in ideas],
        total=len(ideas),
    )


@router.get("/{idea_id}", response_model=IdeaResponse)
async def get_idea(
    idea_id: str,
    current_user: dict = Depends(get_current_user),
):
    """アイデアを1件取得する"""
    user_id: str = current_user["uid"]
    doc = await firestore_service.get_idea(user_id, idea_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Idea not found")
    return IdeaResponse(**doc)


@router.put("/{idea_id}", response_model=IdeaResponse)
async def update_idea(
    idea_id: str,
    idea_in: IdeaUpdate,
    current_user: dict = Depends(get_current_user),
):
    """アイデアを更新する"""
    user_id: str = current_user["uid"]
    data = idea_in.model_dump(exclude_none=True)
    doc = await firestore_service.update_idea(user_id, idea_id, data)
    if doc is None:
        raise HTTPException(status_code=404, detail="Idea not found")
    return IdeaResponse(**doc)


@router.delete("/{idea_id}", status_code=204)
async def delete_idea(
    idea_id: str,
    current_user: dict = Depends(get_current_user),
) -> None:
    """アイデアを削除する"""
    user_id: str = current_user["uid"]
    deleted = await firestore_service.delete_idea(user_id, idea_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Idea not found")
