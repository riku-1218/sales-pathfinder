# Sales-Pathfinder 開発ガイド

このドキュメントでは、Sales-Pathfinder プロジェクトの開発、テスト、デプロイの手順について詳細に解説します。

## 1. 環境構築 (Environment Setup)

開発に必要なツールと環境変数の設定を行います。

### 必須ツール
- **Python 3.11+**: ランタイム環境
- **Google Cloud SDK (gcloud)**: Cloud Functions デプロイ用
- **Direnv** (推奨): 環境変数の自動読み込み

### セットアップ手順

1.  **リポジトリのクローン**
    ```bash
    git clone <repository-url>
    cd sales-pathfinder
    ```

2.  **環境変数の設定**
    `.env.example` をコピーして `.env` を作成し、必要なAPIキーを設定します。
    ```bash
    cp .env.example .env
    ```
    
    `.env` の内容を編集してください：
    ```bash
    # Tavily Search API (検索用)
    TAVILY_API_KEY=tvly-xxxxxxxxxxxx
    
    # Google Cloud Project ID
    GCP_PROJECT_ID=your-project-id
    ```

## 2. ローカル開発 (Local Development)

Python Cloud Functions のローカル開発とテストの手順です。

### 仮想環境の作成

推奨: `venv` を使用してプロジェクト直下または `src/functions/html_parser` 内で仮想環境を作成します。

```bash
# プロジェクトルートで作業する場合
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows
```

### 依存関係のインストール

Cloud Functions の依存関係をインストールします。

```bash
cd src/functions/html_parser
pip install -r requirements.txt
```

### テストの実行

`test_main.py` を使用してパーサーの動作を検証します。

```bash
# src/functions/html_parser ディレクトリで実行
python test_main.py
```

## 3. デプロイ手順 (Deployment)

Google Cloud Functions (第2世代) へのデプロイ手順です。

### 前提条件
- `gcloud` コマンドがインストールされ、認証済みであること (`gcloud auth login`)
- 対象の GCP プロジェクトが設定されていること (`gcloud config set project [PROJECT_ID]`)

### デプロイコマンド

```bash
cd src/functions/html_parser

gcloud functions deploy parse-job-posting \
  --gen2 \
  --runtime=python311 \
  --region=asia-northeast1 \
  --source=. \
  --entry-point=parse_job_posting \
  --trigger-http \
  --allow-unauthenticated
```
*注: 本番運用では `--allow-unauthenticated` の代わりに適切な認証設定を行ってください。*

## 4. 連携設定 (Integration)

システムの全体動作に必要な Dify と Make の設定手順です。

### Dify (Orchestration)
1.  **DSLのインポート**: `src/dify-workflows/main_workflow.md` (またはエクスポートされたDSLファイル) を参照し、Dify上でワークフローを作成・インポートします。
2.  **環境変数設定**: Dify の環境変数設定で、デプロイした Cloud Function の URL (`GCF_URL`) を登録します。
3.  **ナレッジベース連携**: `config/sample_products.json` 等の製品情報を Dify ナレッジベースにアップロードします。

### Make (Integration)
1.  **Webhook設定**: `docs/make_integration.md` を参照し、Make で新規シナリオを作成します。
2.  **Webhook URL取得**: 発行された Custom Webhook URL を Dify ワークフローの出力ノードに設定します。
3.  **出力先連携**: Slack, Google Docs, CRM 等のモジュールを接続して設定します。

---
開発に関する質問や問題報告は、Issue トラッカーを使用してください。
