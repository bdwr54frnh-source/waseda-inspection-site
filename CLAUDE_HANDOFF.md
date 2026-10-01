# 早稲田インスペクション HP — Claude 制作引き渡し（社長 2026-09-30）

## 触るな

- **ドメイン名** `waseda-inspection.com` 固定（`.tokyo` 化・リネーム禁止）
- **WordPress / ロリポップ FTP** — 使わない
- **tandemair / aicode 用デザインに差し替えない** — 早稲田インスペクション会社のサイト

## 正本（成果物の置き場）

- このフォルダ: `AirQuick_Final_3/waseda-inspection/`
- 画像: `waseda-inspection/assets/`（新規作成して全ファイルここ）
- 入口: `index.html`（相対パス `./assets/...`）
- 公開: 社長 Mac で `./scripts/publish_homepages_to_github.sh` → GitHub `waseda-inspection-site`
- GitHub Pages Custom domain: **waseda-inspection.com**（設定済み）

## 社長が渡す素材

- 写真約10枚（用途メモがあるとよい。無くても可）
- 使ってよいチャットスクショ（個人情報・第三者はマスク）
- 現行ページの残すブロック: 啓発（詐欺グラフ）、SNS事件、公式X、TEAM KIYOSHI、リニューアル/ダウンロード待ちのトーン
- **必須（社長）**: **会社案内**（法人・代表・所在地・問い合わせ）／**振込先は口座確定次第 index に追記**／**特許出願中**の一文（出願番号・明細の全文公開はしない）

## 現行 HTML 参考

- `waseda-inspection/index.html`（リニューアル中・長文）
- 旧バックアップ: `waseda_inspection_update_v2/index.html`（同系）

## Claude が返すべきもの

1. 完成 `index.html`
2. `assets/` 内の jpg/png/webp（ファイル名は英数字）
3. 使った写真一覧（ファイル名 ↔ セクション）
4. **単体 HTML だけ渡して画像なし — 禁止**

## ローカル確認

```bash
cd waseda-inspection && python3 -m http.server 8765
# → http://127.0.0.1:8765/
```

## DNS（社長・お名前.com）

Web の A → GitHub 4 IP。MX（mx01.lolipop.jp 等）は**削除しない**。
