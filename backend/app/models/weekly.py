"""週報 (WeeklyReport) の Pydantic モデル定義"""

from datetime import datetime

from pydantic import BaseModel, Field


class WeeklyReportBase(BaseModel):
    """週報の基本フィールド"""

    week_of: str = Field(..., description="対象週 (例: 2026-W15)")
    this_week: str = Field(default="", description="今週の内容")
    next_week: str = Field(default="", description="来週の予定")


class WeeklyGenerateRequest(BaseModel):
    """週報AI生成リクエスト"""

    week_of: str = Field(..., description="対象週 (例: 2026-W15)")


class WeeklyUpdateRequest(BaseModel):
    """週報更新リクエスト"""

    this_week: str | None = None
    next_week: str | None = None


class WeeklyReportResponse(WeeklyReportBase):
    """週報レスポンス"""

    id: str = Field(..., description="ドキュメントID")
    user_id: str = Field(..., description="ユーザーID")
    generated_at: datetime = Field(..., description="AI生成日時")
    edited_at: datetime | None = Field(default=None, description="最終編集日時")

    model_config = {"from_attributes": True}


class WeeklyListResponse(BaseModel):
    """週報一覧レスポンス"""

    reports: list[WeeklyReportResponse]
    total: int
