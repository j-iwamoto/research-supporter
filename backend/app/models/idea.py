"""アイデア (Idea) の Pydantic モデル定義"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class IdeaStatus(str, Enum):
    """アイデアのステータス"""

    NOT_STARTED = "未着手"
    CONSIDERING = "検討中"
    ADOPTED = "採用"
    REJECTED = "却下"


class IdeaBase(BaseModel):
    """アイデアの基本フィールド"""

    title: str = Field(..., description="タイトル")
    description: str = Field(default="", description="説明")
    tags: list[str] = Field(default_factory=list, description="タグ一覧")
    status: IdeaStatus = Field(default=IdeaStatus.NOT_STARTED, description="ステータス")
    related_ideas: list[str] = Field(
        default_factory=list, description="関連アイデアのID一覧"
    )


class IdeaCreate(BaseModel):
    """アイデア作成リクエスト"""

    title: str = Field(..., description="タイトル")
    description: str = Field(default="", description="説明")


class IdeaUpdate(BaseModel):
    """アイデア更新リクエスト (部分更新)"""

    title: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    status: IdeaStatus | None = None
    related_ideas: list[str] | None = None


class IdeaResponse(IdeaBase):
    """アイデアレスポンス"""

    id: str = Field(..., description="ドキュメントID")
    user_id: str = Field(..., description="ユーザーID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")

    model_config = {"from_attributes": True}


class IdeaListResponse(BaseModel):
    """アイデア一覧レスポンス"""

    ideas: list[IdeaResponse]
    total: int
