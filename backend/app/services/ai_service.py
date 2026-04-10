"""Gemini API 連携サービス"""

import json
import logging
import re

from app.core.config import settings

logger = logging.getLogger(__name__)

# ルールベース分類用キーワードマッピング
_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "実験": ["実験", "測定", "データ", "結果", "解析", "分析", "モデル", "学習", "訓練", "評価"],
    "論文読み": ["論文", "読んだ", "サーベイ", "レビュー", "文献", "先行研究", "調査"],
    "コーディング": ["コード", "実装", "プログラム", "バグ", "デバッグ", "リファクタ", "開発", "コーディング"],
    "ミーティング": ["ミーティング", "MTG", "打ち合わせ", "相談", "議論", "発表", "ゼミ", "会議"],
    "執筆": ["執筆", "書いた", "論文作成", "ドラフト", "原稿", "投稿", "修正"],
}


def _classify_by_rules(content: str) -> dict[str, str | list[str]]:
    """キーワードベースの簡易分類（フォールバック用）"""
    matched_category = "その他"
    max_hits = 0

    for category, keywords in _CATEGORY_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in content)
        if hits > max_hits:
            max_hits = hits
            matched_category = category

    # タグ: contentから重要そうなキーワードを抽出（マッチしたもの）
    tags: list[str] = []
    for keywords in _CATEGORY_KEYWORDS.values():
        for kw in keywords:
            if kw in content and kw not in tags:
                tags.append(kw)
                if len(tags) >= 4:
                    break
        if len(tags) >= 4:
            break

    if not tags:
        tags = ["その他"]

    return {"category": matched_category, "tags": tags}


class AIService:
    """Gemini API を使ったAI処理"""

    def __init__(self) -> None:
        self.api_key = settings.GEMINI_API_KEY
        self.model = None

        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-pro")
                logger.info("Gemini API initialized successfully")
            except Exception as e:
                logger.warning("Failed to initialize Gemini API: %s", e)
                self.model = None
        else:
            logger.info("GEMINI_API_KEY not set; using rule-based classification")

    async def classify_log(self, content: str) -> dict[str, str | list[str]]:
        """日報の内容を分類する

        Args:
            content: 日報の本文

        Returns:
            {"category": str, "tags": list[str]}
        """
        # Gemini APIが使えない場合はルールベース分類
        if not self.model:
            return _classify_by_rules(content)

        prompt = (
            "あなたは研究活動を分類するアシスタントです。\n"
            "以下の研究活動の記録を読み、適切なカテゴリとタグを付与してください。\n"
            "【カテゴリ】（1つ選択）\n"
            "- 実験, 論文読み, コーディング, ミーティング, 執筆, その他\n"
            "【タグ】記録から重要なキーワードを2〜4個抽出\n"
            f"【入力】{content}\n"
            '【出力形式】JSON: {{"category": "カテゴリ名", "tags": ["タグ1", "タグ2"]}}'
        )

        try:
            response = await self.model.generate_content_async(prompt)
            text = response.text.strip()
            # JSON部分を抽出（コードブロックで囲まれている場合にも対応）
            json_match = re.search(r"\{[^}]+\}", text)
            if json_match:
                result = json.loads(json_match.group())
                if "category" in result and "tags" in result:
                    return result
            logger.warning("Gemini returned unexpected format: %s", text)
        except Exception as e:
            logger.warning("Gemini API call failed: %s. Falling back to rules.", e)

        return _classify_by_rules(content)

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
