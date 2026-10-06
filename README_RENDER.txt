工事日報 Web テスト版 - Render用

GitHubへアップロードするもの:
- app.py
- requirements.txt
- Procfile
- templates フォルダ
- data フォルダ（空でも可）

Render設定:
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app --bind 0.0.0.0:$PORT

注意:
この版のCSV保存はRenderのローカルファイルです。
Renderの再デプロイ・再起動などでデータが消える可能性があるため、
本番データの保存には使用しないでください。
まずはiPad -> Web -> 会社PCで画面が見えることを確認するテスト用です。
