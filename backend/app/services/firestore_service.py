"""Firestore CRUD サービス"""

import uuid
from datetime import datetime, timezone

from app.core.config import settings


def _calc_week_of(dt: datetime) -> str:
    """ISO週番号を YYYY-Www 形式で返す"""
    iso = dt.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


class FirestoreService:
    """Firestore データベース操作

    開発環境ではインメモリストレージ（dict）で動作する。
    本番環境では Firestore クライアントに切り替える。
    """

    def __init__(self) -> None:
        self.project_id = settings.FIREBASE_PROJECT_ID

        # --- 本番用 Firestore クライアント ---
        # from google.cloud import firestore
        # self.db = firestore.AsyncClient(project=self.project_id)

        # --- 開発用: インメモリストレージ ---
        # key: log_id, value: dict
        self._logs: dict[str, dict] = {}

    # ---- Logs ----

    async def create_log(self, user_id: str, data: dict) -> dict:
        """日報を作成する

        Args:
            user_id: ユーザーID
            data: content, category, tags を含む辞書

        Returns:
            作成されたログ（id, user_id, week_of, created_at 付き）
        """
        # --- 本番用 Firestore ---
        # doc_ref = self.db.collection("logs").document()
        # now = datetime.now(timezone.utc)
        # doc = {
        #     "id": doc_ref.id,
        #     "user_id": user_id,
        #     "content": data["content"],
        #     "category": data.get("category", ""),
        #     "tags": data.get("tags", []),
        #     "week_of": _calc_week_of(now),
        #     "created_at": now,
        # }
        # await doc_ref.set(doc)
        # return doc

        now = datetime.now(timezone.utc)
        log_id = str(uuid.uuid4())
        doc: dict = {
            "id": log_id,
            "user_id": user_id,
            "content": data["content"],
            "category": data.get("category", ""),
            "tags": data.get("tags", []),
            "week_of": _calc_week_of(now),
            "created_at": now,
        }
        self._logs[log_id] = doc
        return doc

    async def get_logs(
        self,
        user_id: str,
        week_of: str | None = None,
        category: str | None = None,
        limit: int = 50,
    ) -> list[dict]:
        """日報一覧を取得する

        Args:
            user_id: ユーザーID
            week_of: 対象週でフィルタ（例: "2026-W15"）
            category: カテゴリでフィルタ
            limit: 最大取得件数

        Returns:
            日報リスト（created_at 降順）
        """
        # --- 本番用 Firestore ---
        # query = self.db.collection("logs").where("user_id", "==", user_id)
        # if week_of:
        #     query = query.where("week_of", "==", week_of)
        # if category:
        #     query = query.where("category", "==", category)
        # query = query.order_by("created_at", direction=firestore.Query.DESCENDING)
        # query = query.limit(limit)
        # docs = await query.get()
        # return [doc.to_dict() for doc in docs]

        results = [
            log for log in self._logs.values()
            if log["user_id"] == user_id
        ]
        if week_of:
            results = [log for log in results if log["week_of"] == week_of]
        if category:
            results = [log for log in results if log["category"] == category]
        # created_at 降順
        results.sort(key=lambda x: x["created_at"], reverse=True)
        return results[:limit]

    async def get_log(self, user_id: str, log_id: str) -> dict | None:
        """日報を1件取得する（所有者チェック付き）

        Args:
            user_id: ユーザーID
            log_id: ログID

        Returns:
            該当ログ、見つからない or 所有者不一致の場合 None
        """
        # --- 本番用 Firestore ---
        # doc_ref = self.db.collection("logs").document(log_id)
        # doc = await doc_ref.get()
        # if not doc.exists:
        #     return None
        # data = doc.to_dict()
        # if data.get("user_id") != user_id:
        #     return None
        # return data

        doc = self._logs.get(log_id)
        if doc is None or doc["user_id"] != user_id:
            return None
        return doc

    async def delete_log(self, user_id: str, log_id: str) -> bool:
        """日報を削除する（所有者チェック付き）

        Args:
            user_id: ユーザーID
            log_id: ログID

        Returns:
            削除成功なら True、見つからない or 所有者不一致なら False
        """
        # --- 本番用 Firestore ---
        # doc_ref = self.db.collection("logs").document(log_id)
        # doc = await doc_ref.get()
        # if not doc.exists:
        #     return False
        # if doc.to_dict().get("user_id") != user_id:
        #     return False
        # await doc_ref.delete()
        # return True

        doc = self._logs.get(log_id)
        if doc is None or doc["user_id"] != user_id:
            return False
        del self._logs[log_id]
        return True

    # ---- Ideas ----

    async def create_idea(self, user_id: str, data: dict) -> dict:
        """アイデアを作成する"""
        raise NotImplementedError

    async def get_ideas(
        self, user_id: str, status: str | None = None, tag: str | None = None
    ) -> list[dict]:
        """アイデア一覧を取得する"""
        raise NotImplementedError

    async def get_idea(self, user_id: str, idea_id: str) -> dict | None:
        """アイデアを1件取得する"""
        raise NotImplementedError

    async def update_idea(self, user_id: str, idea_id: str, data: dict) -> dict:
        """アイデアを更新する"""
        raise NotImplementedError

    async def delete_idea(self, user_id: str, idea_id: str) -> bool:
        """アイデアを削除する"""
        raise NotImplementedError

    # ---- Weekly Reports ----

    async def save_weekly_report(self, user_id: str, data: dict) -> dict:
        """週報を保存する (作成 or 上書き)"""
        raise NotImplementedError

    async def get_weekly_report(self, user_id: str, week_of: str) -> dict | None:
        """指定週の週報を取得する"""
        raise NotImplementedError

    async def update_weekly_report(self, user_id: str, week_of: str, data: dict) -> dict:
        """週報を更新する"""
        raise NotImplementedError


firestore_service = FirestoreService()
