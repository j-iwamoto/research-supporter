"""FastAPI アプリケーションのエントリーポイント"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, dashboard, ideas, logs, weekly

app = FastAPI(
    title=settings.APP_NAME,
    description="研究タスク管理AIツールのバックエンドAPI",
    version="0.1.0",
)

# CORS ミドルウェア
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router)
app.include_router(logs.router)
app.include_router(weekly.router)
app.include_router(ideas.router)
app.include_router(dashboard.router)


@app.get("/")
async def root():
    """ヘルスチェック"""
    return {"status": "ok", "app": settings.APP_NAME}
