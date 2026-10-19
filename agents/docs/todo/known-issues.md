# 既知の問題・改善候補

コードを読んで見つけたもの。未着手。

## 改善候補

- `msync info` が `data_dir` を表示しない。
- ruff の lint エラー（未使用 import 1件）とフォーマット差分（4ファイル）が残っている。ruff の設定ファイルはなく、デフォルト設定で動かしている。
- 自動テストがない。コマンド組み立て関数（`build_remote_run_command`, `build_filtered_transfer_options`, `get_exclude_rules` など）や `manage` の状態計算はサーバーなしでテストできる。rsync のフィルタはローカルのディレクトリ間で rsync を実行すれば確認できる。
