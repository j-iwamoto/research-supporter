"""テスト共通フィクスチャ"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.firestore_service import firestore_service


@pytest.fixture(autouse=True)
def clear_storage():
    """各テスト実行前にインメモリストレージをクリアする"""
    firestore_service._logs.clear()
    firestore_service._ideas.clear()
    firestore_service._weekly_reports.clear()
    yield
    firestore_service._logs.clear()
    firestore_service._ideas.clear()
    firestore_service._weekly_reports.clear()


@pytest.fixture
async def client():
    """httpx AsyncClient (FastAPI テスト用)"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        ac.headers["Authorization"] = "Bearer test-token"
        yield ac
