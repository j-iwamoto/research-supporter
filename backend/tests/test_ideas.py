"""アイデアAPI テスト"""

import pytest

pytestmark = pytest.mark.asyncio(loop_scope="function")


async def test_create_idea(client):
    """POST /api/ideas - アイデア作成（tagsが自動付与）"""
    resp = await client.post(
        "/api/ideas",
        json={"title": "新しい実験手法", "description": "深層学習を使った解析"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "新しい実験手法"
    assert data["description"] == "深層学習を使った解析"
    assert isinstance(data["tags"], list)
    assert len(data["tags"]) > 0
    assert data["status"] == "未着手"
    assert "id" in data
    assert "created_at" in data


async def test_list_ideas(client):
    """GET /api/ideas - 一覧取得"""
    await client.post("/api/ideas", json={"title": "アイデアA", "description": "説明A"})
    await client.post("/api/ideas", json={"title": "アイデアB", "description": "説明B"})

    resp = await client.get("/api/ideas")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["ideas"]) == 2


async def test_update_idea_status(client):
    """PUT /api/ideas/{id} - ステータス更新"""
    create_resp = await client.post(
        "/api/ideas", json={"title": "ステータス変更テスト", "description": ""}
    )
    idea_id = create_resp.json()["id"]

    resp = await client.put(f"/api/ideas/{idea_id}", json={"status": "検討中"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "検討中"


async def test_delete_idea(client):
    """DELETE /api/ideas/{id} - 削除"""
    create_resp = await client.post(
        "/api/ideas", json={"title": "削除テスト", "description": ""}
    )
    idea_id = create_resp.json()["id"]

    resp = await client.delete(f"/api/ideas/{idea_id}")
    assert resp.status_code == 204

    # 削除後は404
    resp = await client.get(f"/api/ideas/{idea_id}")
    assert resp.status_code == 404


async def test_filter_ideas_by_status(client):
    """GET /api/ideas?status=未着手 - フィルタ"""
    # 2件作成（両方とも初期ステータスは「未着手」）
    await client.post("/api/ideas", json={"title": "アイデア1", "description": ""})
    resp2 = await client.post("/api/ideas", json={"title": "アイデア2", "description": ""})
    idea_id = resp2.json()["id"]

    # 1件のステータスを変更
    await client.put(f"/api/ideas/{idea_id}", json={"status": "採用"})

    # 「未着手」でフィルタ
    resp = await client.get("/api/ideas", params={"status": "未着手"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["ideas"][0]["status"] == "未着手"
