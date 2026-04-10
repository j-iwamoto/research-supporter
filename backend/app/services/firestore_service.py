"""Firestore CRUD サービス"""

from app.core.config import settings


class FirestoreService:
    """Firestore データベース操作"""

    def __init__(self):
        self.project_id = settings.FIREBASE_PROJECT_ID
        # TODO: Firestore クライアントを初期化
        # from google.cloud import firestore
        # self.db = firestore.AsyncClient(project=self.project_id)

    # ---- Logs ----

    async def create_log(self, user_id: str, data: dict) -> dict:
        """日報を作成する"""
        # TODO: logs コレクションにドキュメントを追加
        raise NotImplementedError

    async def get_logs(self, user_id: str, week_of: str | None = None) -> list[dict]:
        """日報一覧を取得する"""
        # TODO: user_id でフィルタ、week_of があれば追加フィルタ
        raise NotImplementedError

    async def get_log(self, user_id: str, log_id: str) -> dict | None:
        """日報を1件取得する"""
        raise NotImplementedError

    async def delete_log(self, user_id: str, log_id: str) -> bool:
        """日報を削除する"""
        raise NotImplementedError

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
