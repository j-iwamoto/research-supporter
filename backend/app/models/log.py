"""日報 (Log) の Pydantic モデル定義"""

from datetime import datetime

from pydantic import BaseModel, Field


class LogBase(BaseModel):
    """日報の基本フィールド"""

    content: str = Field(..., description="日報の本文")
    category: str = Field(default="", description="カテゴリ (例: 実験, 論文読み, MTG)")
    tags: list[str] = Field(default_factory=list, description="タグ一覧")


class LogCreate(BaseModel):
    """日報作成リクエスト（category/tagsはAIが自動付与）"""

    content: str = Field(..., description="日報の本文")


class LogResponse(LogBase):
    """日報レスポンス"""

    id: str = Field(..., description="ドキュメントID")
    user_id: str = Field(..., description="ユーザーID")
    week_of: str = Field(default="", description="対象週 (例: 2026-W15)")
    created_at: datetime = Field(..., description="作成日時")

    model_config = {"from_attributes": True}


class LogListResponse(BaseModel):
    """日報一覧レスポンス"""

    logs: list[LogResponse]
    total: int
