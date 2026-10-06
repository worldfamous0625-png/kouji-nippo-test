工事日報 v2 - PostgreSQL版

追加機能:
・送信済み日報一覧 /reports
・Render PostgreSQLへ永続保存
・再デプロイでCSVが消える問題を回避

Render側で必要な設定:
1. PostgreSQLデータベースを作成
2. Web Serviceの Environment に DATABASE_URL を追加
3. 値にはPostgreSQLの Internal Database URLを設定

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app --bind 0.0.0.0:$PORT

注意:
DATABASE_URL設定前にこの版をデプロイすると、意図的に起動エラーになります。
先にDBを作ってDATABASE_URLを設定してください。
