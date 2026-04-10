# 研究タスク管理AIツール (Research Task Manager)

## プロジェクト概要
修士研究の活動記録・管理を支援するAIツール。日報記録、週報自動生成、アイデアメモ、ダッシュボードの4機能を提供する。

## 技術スタック
- **Frontend**: React + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Backend**: Python + FastAPI
- **Database**: Cloud Firestore (Native mode, asia-northeast1)
- **AI/LLM**: Gemini API (gemini-1.5-pro)
- **Infrastructure**: GCP (Cloud Run, Firebase Auth, Cloud Build, Artifact Registry, Secret Manager)
- **CI/CD**: Cloud Build + GitHub トリガー

## ディレクトリ構成
```
research-task-ai/
├── frontend/          # React + Vite アプリ
│   └── src/
│       ├── components/  # UI コンポーネント (layout/, logs/, weekly/, ideas/, dashboard/)
│       ├── hooks/       # カスタムフック (useAuth, useLogs, useIdeas)
│       ├── contexts/    # React Context (AuthContext)
│       ├── services/    # API・Firebase クライアント
│       ├── types/       # TypeScript 型定義
│       └── pages/       # ページコンポーネント
├── backend/           # FastAPI サーバー
│   └── app/
│       ├── routers/     # APIエンドポイント (auth, logs, weekly, ideas, dashboard)
│       ├── services/    # ビジネスロジック (ai_service, firestore_service)
│       ├── models/      # データモデル (log, idea, weekly)
│       └── core/        # 設定・認証 (config, auth)
├── docs/              # ドキュメント
└── .github/workflows/ # CI/CD
```

## 開発ルール

### コーディング規約
- Frontend: TypeScript strict mode、関数コンポーネント、React Hook Form でフォーム管理
- Backend: Python 型ヒント必須、Pydantic モデルでバリデーション
- API: RESTful、Firebase JWT 認証（Authorization: Bearer ヘッダー）
- 日本語コメントOK

### データベース
- Firestore コレクション: users, logs, ideas, weeklyReports
- ユーザーは自身のデータのみアクセス可能（セキュリティルール必須）

### AI (Gemini API) 利用箇所
1. 日報分類: カテゴリ自動分類 + タグ抽出
2. 週報生成: 1週間分の日報を集約・要約
3. アイデア関連付け: 類似度計算で関連アイデア提案
4. AIサジェスト: 活動バランスのアドバイス

### API エンドポイント
- `POST /api/logs` - 日報作成（AI分類付き）
- `GET /api/logs` - 日報一覧（week, category, limit パラメータ）
- `DELETE /api/logs/{id}` - 日報削除
- `POST /api/weekly/generate` - 週報生成
- `PUT /api/weekly/{id}` - 週報編集
- `GET /api/weekly` - 週報一覧
- `POST /api/ideas` - アイデア作成
- `GET /api/ideas` - アイデア一覧（status, tag, search パラメータ）
- `PUT /api/ideas/{id}` - アイデア更新
- `DELETE /api/ideas/{id}` - アイデア削除
- `GET /api/dashboard/summary` - ダッシュボードサマリー

### カテゴリ一覧
実験 / 論文読み / コーディング / ミーティング / 執筆 / その他

### アイデアステータス
未着手 / 検討中 / 採用 / 却下

## エージェントチーム構成

本プロジェクトは以下のエージェントチームで開発を進める:

### 1. architect (設計・統括)
- 全体のアーキテクチャ判断
- エージェント間の作業調整
- 設計書との整合性チェック

### 2. frontend-dev (フロントエンド開発)
- React + TypeScript + Vite のセットアップと実装
- shadcn/ui コンポーネントの構築
- ページ・ルーティング実装
- Firebase Auth 連携（フロント側）

### 3. backend-dev (バックエンド開発)
- FastAPI サーバーのセットアップと実装
- Firestore CRUD操作
- Gemini API 連携
- 認証ミドルウェア実装

### 4. infra-devops (インフラ・デプロイ)
- GCP セットアップ (Cloud Run, Firestore, Firebase Auth)
- Dockerfile 作成
- Cloud Build CI/CD パイプライン構築
- Secret Manager 設定

### 5. qa-tester (テスト・品質管理)
- ユニットテスト・統合テスト作成
- API テスト
- フロントエンドテスト
- セキュリティルール検証

## 開発フェーズ
1. **Phase 1 (MVP基盤)**: 環境構築、認証、基本UI
2. **Phase 2 (日報機能)**: 日報CRUD、AI分類
3. **Phase 3 (週報機能)**: 週報生成、編集
4. **Phase 4 (アイデア機能)**: アイデアCRUD、関連付け
5. **Phase 5 (ダッシュボード)**: 可視化、AIサジェスト
6. **Phase 6 (仕上げ)**: テスト、デプロイ、ドキュメント
