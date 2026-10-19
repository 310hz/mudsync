# 転送（sync / push / pull）

すべて `rsync -avz` をローカルから実行する（`commands/sync.py` の `build_rsync_command`）。rsync には `-e "ssh -o StrictHostKeyChecking=no ..."` を渡している。

## `msync sync`

ローカル → リモートの一方向同期。2段階で行う。

1. **通常同期**: プロジェクトルート → `remote_path`。除外リストは `excludes` + グローバル除外 + `data_includes`（data 項目もここでは除外）。一時ファイルに書き出し `--exclude-from` で渡す。
2. **データ同期**（`data_dir` と `data_includes` が両方あるときのみ）:
   1. リモートで `mkdir -p <data_dir>`
   2. `data_includes` だけを include するフィルタで、プロジェクトルート → `data_dir` を rsync（ディレクトリ構造は保たれる）
   3. 各 data 項目について、リモートで `rm -rf <remote_path>/<項目>` してから `ln -s <data_dir>/<項目> <remote_path>/<項目>`

`--delete` を付けると通常同期に `rsync --delete` を付ける。除外対象（data 項目のシンボリックリンクを含む）は rsync の仕様上削除されない。データ同期側には `--delete` は付かない。

逆方向（リモート → ローカル）の同期は存在しない。サーバーで生成されたものは `pull` で個別に取ってくる設計。

## `msync push PATTERN...` / `msync pull PATTERN...`

指定パターンだけを転送する。`excludes` は参照しない。

フィルタは `--prune-empty-dirs --include=*/ --include=<P> --include=<P>/** ... --exclude=*`（`commands/push.py` の `build_filtered_transfer_options`）。パターンは rsync のフィルタ構文としてそのまま解釈される。

- `push`: プロジェクトルート → `remote_path`
- `pull`: `remote_path` → プロジェクトルート。`data_includes` と一致するパターンはエラーで拒否する（リモート側はシンボリックリンクなので）。

## 関連コマンド

`msync run --sync` は実行前に `sync`（`--delete` なし）を呼ぶ。
