# リモート操作（connect / build / run / info）

リモートでのコマンドはすべて `ssh user@hostname '<cd remote_path && ...>'` の形で実行する（`commands/compose.py` の `build_ssh_command`）。`--verbose` / `-v` を付けると実行する ssh / rsync コマンドを表示する。

## `msync build`

`cd <remote_path> && docker compose [--file F] build [SERVICE]`。終了コードはそのまま返す。

## `msync run [OPTIONS] [COMMAND [ARGS]...]`

`cd <remote_path> && docker compose [--file F] run --service-ports --rm SERVICE [COMMAND...]`。

- 最初の位置引数以降はすべてコンテナ側のコマンドとして扱う（`docker compose run` と同じ）。`msync run python train.py -v` の `-v` は msync ではなくコンテナに渡る。
- コマンド省略時は compose ファイルに書かれた `command` が走る。
- `--service` 省略時は、リモートで `docker compose config --services` を実行し、先頭のサービスを使う（ssh が1往復増える）。
- オプション: `--build`（同じ ssh 内で `build SERVICE &&` を前置）、`--sync`（実行前にローカルで `msync sync`）、`--no-rm`、`--detach`、`--name`、`--file`。
- `--file` は、ローカルのカレントディレクトリかプロジェクトルートに存在するかだけ確認し、パスは加工せずリモートに渡す（リモートでは `remote_path` からの相対になる）。

## `msync connect`

`ssh -t` で入り、`mkdir -p <remote_path> && cd <remote_path> && exec $SHELL`。

## `msync info`

`msync.json` の接続先と SSH 情報（HostName, User, Port, IdentityFile）、`remote_path` を表示する。
