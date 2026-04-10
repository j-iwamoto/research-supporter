# 🎓 研究タスク管理AI (Research Supporter)

**AIを活用した研究活動の記録・管理・可視化ツール**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-6.0-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)

---

## 📸 機能ハイライト

| 機能 | 説明 |
|:---:|:---|
| 📝 **日報記録** | 自然言語で入力するだけでAIが自動分類・タグ付け |
| 📊 **週報自動生成** | 1週間の日報をAIが要約しレポート化 |
| 💡 **アイデアメモ** | AIがタグ自動付与＆関連アイデアを提案 |
| 📈 **ダッシュボード** | 活動量の可視化とAIからの改善提案 |
| 🌙 **ダークテーマ** | 目に優しいダークモード対応 |

---

## ✨ 主な機能

### 📝 日報記録
自然言語で研究活動を入力すると、AIが自動でカテゴリ（実験・論文読み・コーディング・ミーティング・執筆・その他）に分類し、関連タグを付与します。

### 📊 週報自動生成
1週間分の日報をAIが集約・要約し、フォーマット済みの週報を自動生成します。生成後の手動編集にも対応。

### 💡 アイデアメモ
研究アイデアを記録すると、AIがタグを自動付与。類似度計算により関連するアイデアを提案し、新たな着想を支援します。

### 📈 ダッシュボード
研究活動の統計を可視化し、活動バランスに基づいたAIからの改善提案を表示します。

---

## 🛠 技術スタック

| カテゴリ | 技術 |
|:---|:---|
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7 |
| **Backend** | Python, FastAPI, Pydantic |
| **AI / LLM** | Google Gemini API (`gemini-2.0-flash-lite`) |
| **Database** | Cloud Firestore（開発時はインメモリ） |
| **Infrastructure** | GCP（Cloud Run, Firebase Auth, Cloud Build） |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest, httpx, pytest-asyncio |

---

## 🏗 アーキテクチャ

```
[ユーザー]
    │
    ▼
[Frontend - React SPA]  ──  Firebase Auth（認証）
    │
    ▼  REST API (JWT Bearer)
[Backend - FastAPI on Cloud Run]
    ├── Gemini API（AI分類・要約・提案）
    └── Cloud Firestore（データ永続化）
```

| レイヤー | 役割 | 主な技術 |
|:---|:---|:---|
| プレゼンテーション層 | UI描画・ルーティング | React, React Router, Tailwind CSS |
| API層 | エンドポイント・認証 | FastAPI, Firebase Auth (JWT) |
| ビジネスロジック層 | AI処理・データ加工 | Gemini API, Python |
| データ層 | データ永続化 | Cloud Firestore |

---

## 🚀 セットアップ

### 前提条件

- Python 3.12+
- Node.js 20+
- Google Cloud プロジェクト（Gemini API キー）

### クローン

```bash
git clone https://github.com/j-iwamoto/research-supporter.git
cd research-supporter
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .env に GEMINI_API_KEY 等を記入

# 起動
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install

# 起動
npm run dev
```

ブラウザで `http://localhost:5173` にアクセスしてください。

---

## 📁 プロジェクト構成

```
research-supporter/
├── frontend/
│   └── src/
│       ├── components/     # UIコンポーネント
│       ├── pages/          # ページコンポーネント
│       ├── hooks/          # カスタムフック (useAuth, useLogs, useIdeas)
│       ├── contexts/       # React Context (AuthContext)
│       ├── services/       # API・Firebaseクライアント
│       └── types/          # TypeScript 型定義
├── backend/
│   ├── app/
│   │   ├── routers/        # APIエンドポイント
│   │   ├── services/       # ビジネスロジック (AI, Firestore)
│   │   ├── models/         # Pydantic データモデル
│   │   └── core/           # 設定・認証
│   └── tests/              # pytest テスト
├── cloudbuild.yaml         # Cloud Build 設定
└── .github/workflows/      # GitHub Actions
```

---

## 🔌 API一覧

| メソッド | エンドポイント | 説明 |
|:---|:---|:---|
| `POST` | `/api/logs` | 日報作成（AI分類付き） |
| `GET` | `/api/logs` | 日報一覧取得 |
| `DELETE` | `/api/logs/{id}` | 日報削除 |
| `POST` | `/api/weekly/generate` | 週報自動生成 |
| `GET` | `/api/weekly` | 週報一覧取得 |
| `PUT` | `/api/weekly/{id}` | 週報編集 |
| `POST` | `/api/ideas` | アイデア作成 |
| `GET` | `/api/ideas` | アイデア一覧取得 |
| `PUT` | `/api/ideas/{id}` | アイデア更新 |
| `DELETE` | `/api/ideas/{id}` | アイデア削除 |
| `GET` | `/api/dashboard/summary` | ダッシュボードサマリー |

全エンドポイントは Firebase Auth の JWT トークンによる認証が必要です。

---

## 👨‍💻 開発者

**j-iwamoto** - [GitHub](https://github.com/j-iwamoto)
