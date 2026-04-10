"""Gemini API 連携サービス"""

from app.core.config import settings


class AIService:
    """Gemini API を使ったAI処理"""

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        # TODO: google.generativeai を初期化
        # import google.generativeai as genai
        # genai.configure(api_key=self.api_key)
        # self.model = genai.GenerativeModel("gemini-pro")

    async def generate_weekly_report(
        self, logs: list[dict], week_of: str
    ) -> dict:
        """日報一覧から週報を自動生成する。

        Args:
            logs: 対象週の日報リスト
            week_of: 対象週 (例: "2026-W15")

        Returns:
            dict: {"this_week": str, "next_week": str}
        """
        # TODO: Gemini API にプロンプトを送って週報を生成
        raise NotImplementedError

    async def suggest_related_ideas(self, idea: dict, all_ideas: list[dict]) -> list[str]:
        """指定アイデアに関連するアイデアIDを提案する。

        Args:
            idea: 対象のアイデア
            all_ideas: 全アイデアリスト

        Returns:
            list[str]: 関連アイデアのID一覧
        """
        # TODO: Gemini API で関連度を判定
        raise NotImplementedError


ai_service = AIService()
