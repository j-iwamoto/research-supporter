"""認証API テスト"""

import pytest

pytestmark = pytest.mark.asyncio(loop_scope="function")


async def test_verify_token(client):
    """POST /api/auth/verify - DEBUGモードでダミーユーザーを返す"""
    resp = await client.post("/api/auth/verify", json={"token": "any-token"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["uid"] == "dev-user-001"
    assert data["email"] == "dev@example.com"


async def test_get_me(client):
    """GET /api/auth/me - 認証済みユーザー情報を返す"""
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 200
    data = resp.json()
    assert data["uid"] == "dev-user-001"
    assert data["email"] == "dev@example.com"
