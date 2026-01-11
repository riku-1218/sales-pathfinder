# Sales-Pathfinder 開発ガイド

このドキュメントでは、Sales-Pathfinder プロジェクトの開発、設定手順について詳細に解説します。

## 1. 環境構築 (Environment Setup)

本プロジェクトは **Dify** と **Make** を中心に構成されており、ローカルの開発環境構築は基本的に不要です。
リポジトリに含まれる設定ファイルを参照しながら、クラウド上の各サービスを設定します。

### 必須サービス
- **Dify**: AIワークフローの実行環境
- **Make**: 外部連携オートメーション
- **Slack**: 通知受け取り用
- **Google Docs**: レポート生成用

## 2. Dify設定 (Dify Setup)

Dify上でワークフローを再現・編集する手順です。

1.  **DSLのインポート**: 
    *   Difyにログインし、「DSLファイルをインポート」を選択します。
    *   リポジトリ内の `src/dify-workflows/Sales-Pathfinder.yml` をアップロードします。

2.  **ナレッジベース連携**:
    *   `config/sample_products.json` 等の製品情報を Dify ナレッジベースにアップロードします。
    *   ワークフロー内の「知識検索」ノードで、作成したナレッジベースを選択・紐付けます。

3.  **Webhook URL設定**: 
    *   ワークフロー最下部の「HTTP Request」ノードを開きます。
    *   後述するMakeで発行したWebhook URLに書き換えます。

## 3. Make設定 (Make Integration)

Difyの出力を受け取り、Slack / Google Docs へ連携するシナリオを構築します。

1.  **シナリオ作成**: Makeにて新規シナリオを作成します。
2.  **Webhook設定**: 
    *   `Custom Webhook` モジュールを追加し、Webhook URLを発行します。
    *   Dify側でテキストを出力させ、データ構造を認識させます。
3.  **Google Docs連携**:
    *   `Create a Document from Template` モジュールを追加します。
    *   `docs/templates/meeting_prep_sheet.md` の内容を参考に、Google Docsテンプレートを作成しておきます。
    *   Difyからの変数をテンプレートの `{{variable}}` にマッピングします。
4.  **Slack連携**:
    *   `Send a Message` モジュールでSlackチャンネルへの通知を設定します。
    *   作成されたGoogle DocsのURLをメッセージに含めます。

---
開発に関する質問や問題報告は、Issue トラッカーを使用してください。
