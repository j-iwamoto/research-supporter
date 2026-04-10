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
    "コーディング": [
        "コード", "実装", "プログラム", "バグ", "デバッグ", "リファクタ", "開発", "コーディング",
    ],
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
                self.model = genai.GenerativeModel("gemini-2.0-flash-lite")
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
        if not logs:
            return {
                "this_week": "該当週の活動記録がありません。",
                "next_week": "- 活動を記録してください",
            }

        # Gemini API が使える場合
        if self.model:
            logs_text = "\n".join(
                f"- [{log.get('category', 'その他')}] {log['content']}" for log in logs
            )
            prompt = (
                "あなたは研究活動の週報を作成するアシスタントです。\n"
                f"以下は {week_of} の研究活動ログです:\n{logs_text}\n\n"
                "これらの活動を元に週報を作成してください。\n"
                "【今週の成果】カテゴリごとにまとめて記述\n"
                "【来週の予定】今週の進捗を踏まえた次のアクション\n"
                '【出力形式】JSON: {{"this_week": "今週の成果テキスト", '
                '"next_week": "来週の予定テキスト"}}'
            )
            try:
                response = await self.model.generate_content_async(prompt)
                text = response.text.strip()
                json_match = re.search(r"\{[^}]+\}", text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    if "this_week" in result and "next_week" in result:
                        return result
                logger.warning("Gemini returned unexpected format for weekly report: %s", text)
            except Exception as e:
                logger.warning("Gemini API call failed for weekly report: %s", e)

        # フォールバック: カテゴリ別にグルーピングして簡易テキスト生成
        categories: dict[str, list[str]] = {}
        for log in logs:
            cat = log.get("category", "その他")
            categories.setdefault(cat, []).append(log["content"])

        this_week_parts: list[str] = []
        for cat, contents in categories.items():
            lines = "\n".join(f"- {c}" for c in contents)
            this_week_parts.append(f"【{cat}】\n{lines}")
        this_week = "\n\n".join(this_week_parts)

        next_week = "- 引き続き実験を進める\n- 結果を整理する"

        return {"this_week": this_week, "next_week": next_week}

    async def suggest_related_ideas(self, idea: dict, all_ideas: list[dict]) -> list[str]:
        """指定アイデアに関連するアイデアIDを提案する。

        Args:
            idea: 対象のアイデア
            all_ideas: 全アイデアリスト

        Returns:
            list[str]: 関連アイデアのID一覧（最大3件）
        """
        # 自分自身を除外
        others = [a for a in all_ideas if a["id"] != idea.get("id")]
        if not others:
            return []

        # Gemini API が使える場合
        if self.model:
            idea_text = (
                f"タイトル: {idea.get('title', '')}\n"
                f"説明: {idea.get('description', '')}\n"
                f"タグ: {', '.join(idea.get('tags', []))}"
            )
            others_text = "\n".join(
                f"ID:{a['id']} タイトル:{a.get('title','')} タグ:{','.join(a.get('tags',[]))}"
                for a in others[:20]
            )
            prompt = (
                "以下の新しいアイデアに関連する既存アイデアを最大3件選んでください。\n"
                f"【新アイデア】\n{idea_text}\n\n"
                f"【既存アイデア一覧】\n{others_text}\n\n"
                '【出力形式】JSON: {{"related_ids": ["id1", "id2"]}}'
            )
            try:
                response = await self.model.generate_content_async(prompt)
                text = response.text.strip()
                json_match = re.search(r"\{[^}]+\}", text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    if "related_ids" in result:
                        valid_ids = {a["id"] for a in others}
                        return [rid for rid in result["related_ids"] if rid in valid_ids][:3]
            except Exception as e:
                logger.warning("Gemini API call failed for related ideas: %s", e)

        # フォールバック: タグの共通部分があるアイデアを関連として返す
        idea_tags = set(idea.get("tags", []))
        if not idea_tags:
            return []

        scored: list[tuple[int, str]] = []
        for other in others:
            other_tags = set(other.get("tags", []))
            common = len(idea_tags & other_tags)
            if common > 0:
                scored.append((common, other["id"]))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [sid for _, sid in scored[:3]]

    async def classify_idea(self, title: str, description: str = "") -> list[str]:
        """アイデアのタイトルと説明からタグを自動抽出する。

        Args:
            title: アイデアのタイトル
            description: アイデアの説明

        Returns:
            list[str]: 自動抽出されたタグ（2〜4個）
        """
        if self.model:
            prompt = (
                "以下の研究アイデアから重要なキーワードタグを2〜4個抽出してください。\n"
                f"タイトル: {title}\n説明: {description}\n"
                '【出力形式】JSON: {{"tags": ["タグ1", "タグ2", "タグ3"]}}'
            )
            try:
                response = await self.model.generate_content_async(prompt)
                resp_text = response.text.strip()
                json_match = re.search(r"\{[^}]+\}", resp_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    if "tags" in result and len(result["tags"]) >= 1:
                        return result["tags"][:4]
            except Exception as e:
                logger.warning("Gemini API call failed for classify_idea: %s", e)

        # フォールバック: タイトルの単語をそのままタグに
        # 日本語は文字列として、英語はスペース区切りで分割
        words: list[str] = []
        for word in title.split():
            cleaned = word.strip("、。,.!?()（）「」")
            if cleaned and len(cleaned) >= 2:
                words.append(cleaned)
        if not words:
            words = [title[:10]] if title else ["その他"]
        return words[:4]

    async def generate_suggestion(self, dashboard_data: dict) -> str:
        """活動サマリーからアドバイスを生成する。

        Args:
            dashboard_data: ダッシュボードの集計データ

        Returns:
            str: アドバイステキスト
        """
        if self.model:
            prompt = (
                "あなたは研究活動のアドバイザーです。\n"
                f"今週のログ数: {dashboard_data.get('this_week_log_count', 0)}\n"
                f"カテゴリ別: {dashboard_data.get('category_counts', {})}\n"
                f"アイデア総数: {dashboard_data.get('idea_total', 0)}\n"
                "上記の活動状況を踏まえ、研究を進めるためのアドバイスを1つ、簡潔に日本語で述べてください。"
            )
            try:
                response = await self.model.generate_content_async(prompt)
                return response.text.strip()
            except Exception as e:
                logger.warning("Gemini API call failed for suggestion: %s", e)

        # フォールバック: カテゴリの偏りを見て固定メッセージ
        category_counts = dashboard_data.get("category_counts", {})
        log_count = dashboard_data.get("this_week_log_count", 0)

        if log_count == 0:
            return "今週はまだ活動記録がありません。日々の研究活動を記録してみましょう。"

        if "論文読み" not in category_counts or category_counts.get("論文読み", 0) == 0:
            return "今週は論文読みが少なめです。関連研究のサーベイも進めてみましょう。"

        if "実験" not in category_counts or category_counts.get("実験", 0) == 0:
            return "今週は実験が少なめです。仮説の検証を進めてみましょう。"

        return "バランスよく研究活動ができています。この調子で進めましょう。"


ai_service = AIService()
