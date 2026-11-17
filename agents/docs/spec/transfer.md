# 転送（sync / push / pull）

すべて `rsync -az` をローカルから実行する（`commands/sync.py` の `build_rsync_command`）。rsync には `-e "ssh -o StrictHostKeyChecking=no ..."` を渡している。

## 共通オプション

sync / push / pull の3コマンドに共通。`run --sync` から呼ぶ sync はデフォルトのまま。

- **partial（デフォルト有効、`--no-partial` で無効）**: `--partial-dir=.rsync-partial` を付ける。中断した転送の途中ファイルを転送先の各ディレクトリの `.rsync-partial/` に残し、次回の転送で続きから再開する。`--partial` 単体だと途中ファイルが本来の名前で転送先に置かれ、壊れたファイルが完成品と区別できなくなるので partial-dir を使っている。
- **`.rsync-partial/` の除外（常に付与）**: `--exclude=.rsync-partial/` を他のフィルタより前に置く。rsync は相対パスの partial-dir を自動で除外するが、その除外ルールはすべてのフィルタの末尾に追加されるため、push / pull の `--include=*/` に先にマッチしてしまう。これがないと、中断した pull の残りが次の push で送られる。
- **進捗表示（デフォルト有効、`-q/--quiet` で無効）**: 通常は `-v --progress` を付けてファイル一覧と進捗を表示する。`--quiet` ではこの2つを外し、msync 自身のメッセージ（`Syncing ...` など）も出さない。エラーは出る。`--verbose` によるコマンド表示は `--quiet` と併用できる。

## `msync sync`

ローカル → リモートの一方向同期。2段階で行う。

1. **通常同期**: プロジェクトルート → `remote_path`。除外リストは `excludes` + `data_includes`（data 項目もここでは除外）+ グローバル除外。一時ファイルに書き出し `--exclude-from` で渡す。
2. **データ同期**（`data_dir` と `data_includes` が両方あるときのみ）:
   1. リモートで `mkdir -p <data_dir>`
   2. `data_includes` だけを include するフィルタで、プロジェクトルート → `data_dir` を rsync（ディレクトリ構造は保たれる）。push と同じフィルタを使う
   3. 各 data 項目について、リモートで `rm -rf <remote_path>/<項目>` してから `ln -s <data_dir>/<項目> <remote_path>/<項目>`

`excludes` と `data_includes` はプロジェクトルートからのパスなので、先頭に `/` を付けた rsync パターンに変換して渡す（`sync_rules.py` の `anchor_rule`）。rsync は先頭 `/` のないパターンを任意の深さでマッチさせるので、変換しないと `data/` を外したときに `src/pkg/data/` も外れてしまう。グローバル除外はどの深さでも効かせたいので変換しない。

`--delete` を付けると通常同期に `rsync --delete` を付ける。除外対象（data 項目のシンボリックリンクを含む）は rsync の仕様上削除されない。データ同期側には `--delete` は付かない。

逆方向（リモート → ローカル）の同期は存在しない。サーバーで生成されたものは `pull` で個別に取ってくる設計。

## `msync push PATTERN...` / `msync pull PATTERN...`

指定パターンだけを転送する。`excludes` は参照しない。

フィルタは `--prune-empty-dirs --include=*/ --include=<P> --include=<P>/** ... --exclude=*`（`commands/sync.py` の `build_filtered_transfer_options`）。パターンは sync と同じく先頭に `/` を付けて、プロジェクトルートからのパスとして扱う（`msync pull data/` は直下の `data/` だけ）。ワイルドカードは rsync のフィルタ構文で解釈される。`*.pth` は直下だけにマッチし、`**/*.pth` はサブディレクトリ内だけにマッチする（直下の `model.pth` には当たらない）。全階層を対象にするには両方を指定する。

- `push`: プロジェクトルート → `remote_path`
- `pull`: `remote_path` → プロジェクトルート。`data_includes` の項目と一致するパターンは、前後の `/` の有無を無視して比較し、エラーで拒否する（リモート側はシンボリックリンクなので）。

## 関連コマンド

`msync run --sync` は実行前に `sync`（`--delete` なし）を呼ぶ。
