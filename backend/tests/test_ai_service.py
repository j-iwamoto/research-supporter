"""AIサービス テスト（ルールベース分類 + 週報フォールバック）"""

import pytest

from app.services.ai_service import _classify_by_rules, ai_service


# ---- ルールベース分類テスト ----


def test_classify_experiment():
    """実験カテゴリのキーワードで分類"""
    result = _classify_by_rules("今日は実験データの測定を行い、結果を解析した")
    assert result["category"] == "実験"
    assert isinstance(result["tags"], list)
    assert len(result["tags"]) > 0


def test_classify_paper_reading():
    """論文読みカテゴリのキーワードで分類"""
    result = _classify_by_rules("先行研究の論文をサーベイして文献を整理した")
    assert result["category"] == "論文読み"


def test_classify_coding():
    """コーディングカテゴリのキーワードで分類"""
    result = _classify_by_rules("新機能のコードを実装してデバッグした")
    assert result["category"] == "コーディング"


def test_classify_meeting():
    """ミーティングカテゴリのキーワードで分類"""
    result = _classify_by_rules("ゼミで研究の進捗を発表して議論した")
    assert result["category"] == "ミーティング"


def test_classify_writing():
    """執筆カテゴリのキーワードで分類"""
    result = _classify_by_rules("論文のドラフトを執筆して原稿を修正した")
    assert result["category"] == "執筆"


def test_classify_other():
    """該当なしの場合は「その他」"""
    result = _classify_by_rules("今日は特になし")
    assert result["category"] == "その他"
    assert result["tags"] == ["その他"]


# ---- 週報フォールバック生成テスト ----


async def test_weekly_report_fallback_with_logs():
    """ログありの場合、カテゴリ別にグルーピングされた週報を生成"""
    logs = [
        {"content": "実験データを取得", "category": "実験"},
        {"content": "論文を3本読んだ", "category": "論文読み"},
        {"content": "バグを修正した", "category": "コーディング"},
    ]
    result = await ai_service.generate_weekly_report(logs, "2026-W15")
    assert "this_week" in result
    assert "next_week" in result
    # カテゴリ名が含まれていること
    assert "実験" in result["this_week"]
    assert "論文読み" in result["this_week"]
    assert "コーディング" in result["this_week"]


async def test_weekly_report_fallback_empty_logs():
    """ログなしの場合のフォールバック"""
    result = await ai_service.generate_weekly_report([], "2026-W15")
    assert result["this_week"] == "該当週の活動記録がありません。"
    assert "記録" in result["next_week"]
