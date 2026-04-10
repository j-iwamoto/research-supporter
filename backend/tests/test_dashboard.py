"""ダッシュボードAPI テスト"""

import pytest

pytestmark = pytest.mark.asyncio(loop_scope="function")


async def test_dashboard_summary_empty(client):
    """GET /api/dashboard/summary - データ無しの場合"""
    resp = await client.get("/api/dashboard/summary")
    assert resp.status_code == 200
    data = resp.json()

    # ログがない状態
    assert data["totalLogsThisWeek"] == 0
    assert data["totalIdeas"] == 0
    assert isinstance(data["categoryCounts"], dict)
    assert isinstance(data["ideaStatusCounts"], dict)
    assert isinstance(data["weeklyTrend"], list)
    assert len(data["weeklyTrend"]) == 4
    # AIアドバイスが返る（フォールバック）
    assert isinstance(data["aiSuggestion"], str)
    assert len(data["aiSuggestion"]) > 0


async def test_dashboard_summary_with_logs(client):
    """GET /api/dashboard/summary - 日報追加後のデータ"""
    # 日報を3件作成
    await client.post("/api/logs", json={"content": "実験データの測定を行った"})
    await client.post("/api/logs", json={"content": "論文をサーベイした"})
    await client.post("/api/logs", json={"content": "コードを実装した"})

    resp = await client.get("/api/dashboard/summary")
    assert resp.status_code == 200
    data = resp.json()

    # 今週のログが3件
    assert data["totalLogsThisWeek"] == 3
    # カテゴリカウントに値がある
    total_category = sum(data["categoryCounts"].values())
    assert total_category == 3
    # weeklyTrendの今週に3件が反映されている
    assert data["weeklyTrend"][0]["count"] == 3


async def test_dashboard_summary_with_ideas(client):
    """GET /api/dashboard/summary - アイデア追加後の統計"""
    # アイデアを2件作成
    await client.post(
        "/api/ideas", json={"title": "新しい実験手法", "description": "手法の提案"}
    )
    await client.post(
        "/api/ideas", json={"title": "データ可視化ツール", "description": "ツール開発"}
    )

    resp = await client.get("/api/dashboard/summary")
    assert resp.status_code == 200
    data = resp.json()

    assert data["totalIdeas"] == 2
    assert isinstance(data["ideaStatusCounts"], dict)
