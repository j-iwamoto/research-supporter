"""週報API テスト"""

import pytest

from app.services.firestore_service import firestore_service, _calc_week_of
from datetime import datetime, timezone

pytestmark = pytest.mark.asyncio(loop_scope="function")


async def test_generate_weekly_report(client):
    """POST /api/logs で日報作成後、POST /api/weekly/generate で週報生成"""
    # 日報を数件作成
    await client.post("/api/logs", json={"content": "実験データの測定を行った"})
    await client.post("/api/logs", json={"content": "論文をサーベイした"})
    await client.post("/api/logs", json={"content": "コードを実装した"})

    # 今週の week_of を取得
    now = datetime.now(timezone.utc)
    week_of = _calc_week_of(now)

    # 週報を生成
    resp = await client.post("/api/weekly/generate", json={"week_of": week_of})
    assert resp.status_code == 201
    data = resp.json()
    assert data["week_of"] == week_of
    assert data["this_week"] != ""
    assert data["next_week"] != ""
    assert "id" in data
    assert "generated_at" in data


async def test_get_weekly_report(client):
    """GET /api/weekly/{week_of} - 取得"""
    now = datetime.now(timezone.utc)
    week_of = _calc_week_of(now)

    # まず日報作成 + 週報生成
    await client.post("/api/logs", json={"content": "実験を行った"})
    await client.post("/api/weekly/generate", json={"week_of": week_of})

    # 週報を取得
    resp = await client.get(f"/api/weekly/{week_of}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["week_of"] == week_of


async def test_update_weekly_report(client):
    """PUT /api/weekly/{week_of} - 編集"""
    now = datetime.now(timezone.utc)
    week_of = _calc_week_of(now)

    # 日報作成 + 週報生成
    await client.post("/api/logs", json={"content": "データ解析した"})
    await client.post("/api/weekly/generate", json={"week_of": week_of})

    # 週報を編集
    resp = await client.put(
        f"/api/weekly/{week_of}",
        json={"this_week": "手動で編集した内容", "next_week": "来週の計画を更新"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["this_week"] == "手動で編集した内容"
    assert data["next_week"] == "来週の計画を更新"
    assert data["edited_at"] is not None


async def test_get_weekly_report_not_found(client):
    """GET /api/weekly/{week_of} - 存在しない週は404"""
    resp = await client.get("/api/weekly/2000-W01")
    assert resp.status_code == 404
