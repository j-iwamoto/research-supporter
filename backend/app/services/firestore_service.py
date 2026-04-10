"""Firestore CRUD サービス"""

import uuid
from datetime import datetime, timezone

from app.core.config import settings

# 全カテゴリ定義（AIサービスの分類カテゴリと一致させる）
ALL_CATEGORIES = ["実験", "論文読み", "コーディング", "ミーティング", "執筆", "その他"]


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
        # key: "{user_id}:{week_of}", value: dict
        self._weekly_reports: dict[str, dict] = {}
        # key: idea_id, value: dict
        self._ideas: dict[str, dict] = {}

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

    async def update_log(self, user_id: str, log_id: str, data: dict) -> dict | None:
        """日報を更新する（所有者チェック付き）

        Args:
            user_id: ユーザーID
            log_id: ログID
            data: 更新する内容（content, category, tags など）

        Returns:
            更新後のログ、見つからない or 所有者不一致の場合 None
        """
        # --- 本番用 Firestore ---
        # doc_ref = self.db.collection("logs").document(log_id)
        # doc = await doc_ref.get()
        # if not doc.exists:
        #     return None
        # existing = doc.to_dict()
        # if existing.get("user_id") != user_id:
        #     return None
        # await doc_ref.update(data)
        # updated = await doc_ref.get()
        # return updated.to_dict()

        doc = self._logs.get(log_id)
        if doc is None or doc["user_id"] != user_id:
            return None
        for key, value in data.items():
            if value is not None:
                doc[key] = value
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
        now = datetime.now(timezone.utc)
        idea_id = str(uuid.uuid4())
        doc: dict = {
            "id": idea_id,
            "user_id": user_id,
            "title": data["title"],
            "description": data.get("description", ""),
            "tags": data.get("tags", []),
            "status": data.get("status", "未着手"),
            "related_ideas": data.get("related_ideas", []),
            "created_at": now,
            "updated_at": now,
        }
        self._ideas[idea_id] = doc
        return doc

    async def get_ideas(
        self, user_id: str, status: str | None = None, tag: str | None = None
    ) -> list[dict]:
        """アイデア一覧を取得する"""
        results = [
            idea for idea in self._ideas.values()
            if idea["user_id"] == user_id
        ]
        if status:
            results = [idea for idea in results if idea["status"] == status]
        if tag:
            results = [idea for idea in results if tag in idea.get("tags", [])]
        results.sort(key=lambda x: x["created_at"], reverse=True)
        return results

    async def get_idea(self, user_id: str, idea_id: str) -> dict | None:
        """アイデアを1件取得する"""
        doc = self._ideas.get(idea_id)
        if doc is None or doc["user_id"] != user_id:
            return None
        return doc

    async def update_idea(self, user_id: str, idea_id: str, data: dict) -> dict | None:
        """アイデアを更新する（部分更新）"""
        doc = self._ideas.get(idea_id)
        if doc is None or doc["user_id"] != user_id:
            return None
        for key, value in data.items():
            if value is not None:
                doc[key] = value
        doc["updated_at"] = datetime.now(timezone.utc)
        return doc

    async def delete_idea(self, user_id: str, idea_id: str) -> bool:
        """アイデアを削除する"""
        doc = self._ideas.get(idea_id)
        if doc is None or doc["user_id"] != user_id:
            return False
        del self._ideas[idea_id]
        return True

    # ---- Weekly Reports ----

    async def save_weekly_report(self, user_id: str, data: dict) -> dict:
        """週報を保存する (作成 or 上書き / upsert)"""
        week_of = data["week_of"]
        key = f"{user_id}:{week_of}"
        now = datetime.now(timezone.utc)

        existing = self._weekly_reports.get(key)
        if existing:
            existing["this_week"] = data.get("this_week", existing["this_week"])
            existing["next_week"] = data.get("next_week", existing["next_week"])
            existing["generated_at"] = now
            return existing
        else:
            report_id = str(uuid.uuid4())
            doc: dict = {
                "id": report_id,
                "user_id": user_id,
                "week_of": week_of,
                "this_week": data.get("this_week", ""),
                "next_week": data.get("next_week", ""),
                "generated_at": now,
                "edited_at": None,
            }
            self._weekly_reports[key] = doc
            return doc

    async def get_weekly_report(self, user_id: str, week_of: str) -> dict | None:
        """指定週の週報を取得する"""
        key = f"{user_id}:{week_of}"
        return self._weekly_reports.get(key)

    async def update_weekly_report(self, user_id: str, week_of: str, data: dict) -> dict | None:
        """週報を更新する（部分更新）"""
        key = f"{user_id}:{week_of}"
        doc = self._weekly_reports.get(key)
        if doc is None:
            return None
        if data.get("this_week") is not None:
            doc["this_week"] = data["this_week"]
        if data.get("next_week") is not None:
            doc["next_week"] = data["next_week"]
        doc["edited_at"] = datetime.now(timezone.utc)
        return doc

    async def get_weekly_reports(self, user_id: str) -> list[dict]:
        """ユーザーの全週報を取得する（week_of降順）"""
        results = [
            report for report in self._weekly_reports.values()
            if report["user_id"] == user_id
        ]
        results.sort(key=lambda x: x["week_of"], reverse=True)
        return results

    # ---- Dashboard ----

    async def get_dashboard_data(self, user_id: str) -> dict:
        """ダッシュボード用の集計データを取得する"""
        now = datetime.now(timezone.utc)
        current_week = _calc_week_of(now)

        # 今週のログ
        all_logs = [log for log in self._logs.values() if log["user_id"] == user_id]
        this_week_logs = [log for log in all_logs if log["week_of"] == current_week]

        # カテゴリ別カウント（全カテゴリを0で初期化）
        category_counts: dict[str, int] = {cat: 0 for cat in ALL_CATEGORIES}
        for log in this_week_logs:
            cat = log.get("category", "その他")
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # アイデア統計
        all_ideas = [idea for idea in self._ideas.values() if idea["user_id"] == user_id]
        status_counts: dict[str, int] = {}
        for idea in all_ideas:
            s = idea.get("status", "未着手")
            status_counts[s] = status_counts.get(s, 0) + 1

        # 過去4週間のトレンド
        iso_cal = now.isocalendar()
        weekly_trend: list[dict] = []
        for i in range(4):
            week_num = iso_cal[1] - i
            year = iso_cal[0]
            if week_num <= 0:
                year -= 1
                week_num += 52
            wk = f"{year}-W{week_num:02d}"
            count = sum(1 for log in all_logs if log["week_of"] == wk)
            weekly_trend.append({"week_of": wk, "log_count": count})

        return {
            "current_week": current_week,
            "this_week_log_count": len(this_week_logs),
            "category_counts": category_counts,
            "idea_total": len(all_ideas),
            "idea_status_counts": status_counts,
            "weekly_trend": weekly_trend,
        }


firestore_service = FirestoreService()
