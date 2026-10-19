# Status

## 現状

README に書かれた機能（default / set / info / connect / manage / sync / push / pull / build / run）はすべて実装済み。進行中の大きな作業はない。

## 開発環境

- `uv run msync ...` でローカル実行できる。
- lint / format は ruff（dev 依存）: `uv run ruff check src`, `uv run ruff format src`。justfile はまだない。
- 自動テストなし。サーバー接続が必要な動作確認はユーザーに依頼する。

## 未解決事項

見つかっている問題・改善候補は [todo/known-issues.md](todo/known-issues.md)。
