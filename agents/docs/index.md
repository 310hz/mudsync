# Index

| ドキュメント | 内容 | 読むタイミング |
| --- | --- | --- |
| `README.md`（リポジトリ直下） | ユーザー向けの使い方とチュートリアル。編集禁止 | 最初に一度 |
| [concepts/domain.md](concepts/domain.md) | 設定の2層構造、リモートパスとデータディレクトリ、同期ルール（include / exclude / data） | 機能に手を入れる前に必ず |
| [spec/config.md](spec/config.md) | `config.json` / `msync.json` のスキーマ、SSH 接続情報の扱い | 設定まわりを触るとき |
| [spec/transfer.md](spec/transfer.md) | sync / push / pull の rsync の組み立てとデータディレクトリの同期手順 | 転送まわりを触るとき |
| [spec/manage.md](spec/manage.md) | `manage` TUI のキー操作、表示、トグルの意味論、性能上の注意 | `manage.py` を触るとき |
| [spec/remote.md](spec/remote.md) | connect / build / run / info のリモートコマンドの組み立て | リモート実行まわりを触るとき |
| [todo/known-issues.md](todo/known-issues.md) | 既知のバグ・要確認事項・改善候補 | 作業を選ぶとき |

## コード配置

- `src/mudsync/cli.py`: typer のコマンド定義（引数・オプションのみ）。処理は `commands/<name>.py` の `command()` に委譲する。
- `src/mudsync/commands/compose.py`: ssh / docker compose コマンドの組み立てと compose サービス解決。build と run が共有。
- `src/mudsync/config.py`: デフォルト設定、`sync_rules.py`: プロジェクト設定と同期ルール、`project.py`: プロジェクトルート探索、`ssh_config.py`: `~/.ssh/config` のパース。
