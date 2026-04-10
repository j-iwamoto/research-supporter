"""日報API テスト"""

import pytest

pytestmark = pytest.mark.asyncio(loop_scope="function")


async def test_create_log(client):
    """POST /api/logs - 日報作成（category/tagsが自動付与される）"""
    resp = await client.post("/api/logs", json={"content": "今日は実験データの解析を行った"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["content"] == "今日は実験データの解析を行った"
    assert data["category"] != ""
    assert isinstance(data["tags"], list)
    assert len(data["tags"]) > 0
    assert "id" in data
    assert "user_id" in data
    assert "week_of" in data
    assert "created_at" in data


async def test_list_logs(client):
    """GET /api/logs - 一覧取得（作成した日報が返る）"""
    # まず2件作成
    await client.post("/api/logs", json={"content": "論文を読んだ"})
    await client.post("/api/logs", json={"content": "コードを実装した"})

    resp = await client.get("/api/logs")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["logs"]) == 2


async def test_get_log_by_id(client):
    """GET /api/logs/{id} - 1件取得"""
    create_resp = await client.post("/api/logs", json={"content": "ゼミで発表した"})
    log_id = create_resp.json()["id"]

    resp = await client.get(f"/api/logs/{log_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == log_id
    assert resp.json()["content"] == "ゼミで発表した"


async def test_delete_log(client):
    """DELETE /api/logs/{id} - 削除成功"""
    create_resp = await client.post("/api/logs", json={"content": "削除テスト"})
    log_id = create_resp.json()["id"]

    resp = await client.delete(f"/api/logs/{log_id}")
    assert resp.status_code == 204

    # 削除後は404
    resp = await client.get(f"/api/logs/{log_id}")
    assert resp.status_code == 404


async def test_get_log_not_found(client):
    """GET /api/logs/{不正ID} - 404"""
    resp = await client.get("/api/logs/nonexistent-id")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Log not found"
