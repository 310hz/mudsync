# 既知の問題・改善候補

コードを読んで見つけたもの。未着手。

## バグ

- **`msync default` でデータディレクトリ入力を Esc/Ctrl-C でキャンセルすると例外で落ちる。** `default.py` が `None.strip()` を呼ぶ。`set.py` 側は対処済みなので同じ扱いにすればよい。
- **`msync connect` が `remote_path` をシェルクォートしていない。** パスに空白などがあると壊れる。他のコマンドは `shlex.quote` 済み。

## 要確認（仕様か不具合か不明）

- **`msync manage` の起動時自動除外が毎回かかる。** 大きなファイル・ディレクトリを意図的に include に戻しても、次回 `manage` を開いて Enter で保存すると再び exclude に戻る。初回だけにすべきかはユーザー判断。

## 改善候補

- `msync info` が `data_dir` を表示しない。
- ruff の lint エラー（未使用 import 2件）とフォーマット差分（4ファイル）が残っている。ruff の設定ファイルはなく、デフォルト設定で動かしている。
- 自動テストがない。コマンド組み立て関数（`build_remote_run_command`, `build_filtered_transfer_options` など）や `manage` の状態計算はサーバーなしでテストできる。
