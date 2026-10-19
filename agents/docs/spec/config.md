# 設定ファイル

概念は [concepts/domain.md](../concepts/domain.md) を参照。

## デフォルト設定 `config.json`

```json
{
  "ssh_host": "muds-gpu-1",
  "remote_path": "/home/<lab>/<user>",
  "data_dir": "/raid/data/<lab>/<user>"
}
```

- `ssh_host`: `~/.ssh/config` の Host 名。
- `data_dir`: 省略可（`null`）。
- 旧キー `remote_home` は読み込み時に `remote_path` へ読み替え、旧キー `global_excludes` は捨てる（`config.py`）。過去バージョンとの互換のために残っている。

## プロジェクト設定 `msync.json`

```json
{
  "server": "muds-gpu-1",
  "remote_path": "/home/<lab>/<user>/<project>",
  "excludes": ["dummy.txt", "outputs/"],
  "data_dir": "/raid/data/<lab>/<user>/<project>",
  "data_includes": ["dataset/"]
}
```

- `server`: `~/.ssh/config` の Host 名。キー名がデフォルト設定（`ssh_host`）と異なる点に注意。
- `excludes` / `data_includes`: 同期ルール。`msync manage` が書き換える。手で編集してもよい。
- `data_dir` / `data_includes` は欠けていても読み込める（後から追加されたキー）。

`msync set` を再実行すると、既存の `msync.json` の値が入力の初期値になり、`excludes` と `data_includes` は保持される。

`msync.json` は個人のサーバーパスを含むため、リポジトリにはコミットしない運用（本リポジトリではユーザーのグローバル gitignore で除外されている）。また同期対象からは常に除外される。

## SSH 接続情報

`~/.ssh/config` から `HostName` / `User` / `Port` / `IdentityFile` を読み、`ssh` / `rsync` のコマンドライン引数に展開して渡す（`ssh_config.py`）。接続先は Host 名ではなく `user@<HostName>` で指定している。ssh の `Host` ブロックはコマンドラインに渡した名前でマッチするため、Host 名のブロックに書いた上記4項目以外の設定（`ProxyJump` など）は適用されない。
