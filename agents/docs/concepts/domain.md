# ドメインモデル

## 設定の2層構造

| 層 | 保存先 | 作成コマンド | 役割 |
| --- | --- | --- | --- |
| デフォルト設定 | `$XDG_CONFIG_HOME/mudsync/config.json`（未設定時 `~/.config/mudsync/config.json`） | `msync default` | ユーザー単位の初期値。`msync set` の入力初期値としてのみ使われる |
| プロジェクト設定 | プロジェクトルートの `msync.json` | `msync set` / `msync manage` | 実際の動作はすべてこちらを参照する |

デフォルト設定は「プロジェクトごとに毎回同じ値を打たなくて済む」ための補助でしかない。`set` 以外のコマンドはデフォルト設定を読まない。

プロジェクトルートは、カレントディレクトリから親方向に `msync.json` を探して決まる（git と同じ探索方式）。ただし `msync set` だけはカレントディレクトリに `msync.json` を作る。

スキーマの詳細は [spec/config.md](../spec/config.md)。

## サーバー上の2つの置き場所

- **リモートパス（`remote_path`）**: プロジェクトの同期先。サーバー上のホームディレクトリ配下（例: `/home/<lab>/<user>/<project>`）。容量が小さい。
- **データディレクトリ（`data_dir`）**: 大きなファイルの置き場。大容量ストレージ配下（例: `/raid/data/<lab>/<user>/<project>`）。省略可能。

`set` 時の初期値は、どちらもデフォルト設定の値にプロジェクトディレクトリ名を付けたもの。

## 同期ルール

プロジェクト内の各ファイル・ディレクトリは、同期上で次の3状態のいずれかを持つ。

| 状態 | 意味 | `msync.json` での表現 |
| --- | --- | --- |
| include | リモートパスへ同期する（既定） | どのリストにも載らない |
| exclude | 同期しない | `excludes` に載る |
| data | 実体をデータディレクトリへ同期し、リモートパス側には同名のシンボリックリンクを置く | `data_includes` に載る |

- 既定は「すべて同期」で、除外したいものを選ぶ方式（ホワイトリストではなくブラックリスト）。
- エントリはプロジェクトルートからの相対パス。ディレクトリは末尾 `/` 付きで表し、配下すべてに効く。
- data は exclude より優先される。
- **グローバル除外**（`.git/`, `.venv/`, `__pycache__/`, `msync.json` など。`sync_rules.py` の `DEFAULT_GLOBAL_EXCLUDES`）は常に除外され、ユーザーは変更できない。`manage` の画面にも表示されない。

ルールの編集は `msync manage`（TUI）で行う。挙動は [spec/manage.md](../spec/manage.md)。ルールが転送にどう効くかは [spec/transfer.md](../spec/transfer.md)。
