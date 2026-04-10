"""AIサービス テスト（ルールベース分類 + 週報フォールバック）"""

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


# ---- classify_idea フォールバックテスト ----


async def test_classify_idea_fallback_basic():
    """Gemini無しでタイトルからタグを抽出"""
    tags = await ai_service.classify_idea("新しい実験手法の提案", "実験手法について")
    assert isinstance(tags, list)
    assert len(tags) >= 1
    assert len(tags) <= 4


async def test_classify_idea_fallback_english():
    """英語のタイトルでもタグが返る"""
    tags = await ai_service.classify_idea("Deep Learning approach", "Neural network method")
    assert isinstance(tags, list)
    assert len(tags) >= 1


async def test_classify_idea_fallback_short_title():
    """短いタイトルでもタグが返る（1単語）"""
    tags = await ai_service.classify_idea("AI", "")
    assert isinstance(tags, list)
    assert len(tags) >= 1


async def test_classify_idea_fallback_empty_title():
    """空タイトルの場合は 'その他' が返る"""
    tags = await ai_service.classify_idea("", "")
    assert isinstance(tags, list)
    assert len(tags) >= 1


# ---- generate_suggestion フォールバックテスト ----


async def test_generate_suggestion_no_logs():
    """ログ0件のフォールバック: 活動記録を促すメッセージ"""
    data = {
        "this_week_log_count": 0,
        "category_counts": {},
        "idea_total": 0,
    }
    result = await ai_service.generate_suggestion(data)
    assert isinstance(result, str)
    assert "活動記録" in result or "記録" in result


async def test_generate_suggestion_no_paper():
    """論文読みが無い場合のフォールバック"""
    data = {
        "this_week_log_count": 3,
        "category_counts": {"実験": 2, "コーディング": 1},
        "idea_total": 5,
    }
    result = await ai_service.generate_suggestion(data)
    assert isinstance(result, str)
    assert "論文" in result


async def test_generate_suggestion_no_experiment():
    """実験が無い場合のフォールバック"""
    data = {
        "this_week_log_count": 2,
        "category_counts": {"論文読み": 2},
        "idea_total": 3,
    }
    result = await ai_service.generate_suggestion(data)
    assert isinstance(result, str)
    assert "実験" in result


async def test_generate_suggestion_balanced():
    """バランス良い場合のフォールバック"""
    data = {
        "this_week_log_count": 4,
        "category_counts": {"実験": 2, "論文読み": 1, "コーディング": 1},
        "idea_total": 5,
    }
    result = await ai_service.generate_suggestion(data)
    assert isinstance(result, str)
    assert "バランス" in result or "調子" in result
