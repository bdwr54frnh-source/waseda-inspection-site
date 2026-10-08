# HP公開ハンドオフ（社長正本 2026-10-07）

## 本番URL現状

- DNS: `163.44.185.173`（ロリポップ）
- タイトル: リニューアル中
- 確認日: 2026-08-08

## ローカル / GitHub 資産

- ローカル `index.html`: 公式ポータル — **#air-robinson** 雲ヒーロー（`hp_app_cloud_world_kiyoshi.jpg`）・3枚スクショ・テーマ曲はクレジット＋Apple Music リンクのみ — **未 push**
- ローカル確認: `cd waseda-inspection && python3 -m http.server 8765` → `http://127.0.0.1:8765/index.html#air-robinson`
- GitHub `waseda-inspection-site`: 会社案内 **576行** — **#air-robinson 弱**（本番は未 deploy のまま）

## 未完了（本番）

- AIRロビンソン本番
- 会社案内 / 特許 / 世界時刻 / 代表写真 本番
- m4a 未配置
- commit / push / deploy 未

## m4a / テーマ曲

- 指定: `air_robinson_theme_licensed.m4a`
- 状態: 探索済み・**未発見** — HP は **無音**（`<audio>` なし）
- **代替禁止**
- 権利: 許諾書未同梱のため自サイト試聴不可。Apple Music 外部リンクのみ（`AIR_ROBINSON_THEME_SONG_WEB_POLICY.md` 2026-10-07 調査表参照）

## 次アクション（実行は社長 GO のみ）

- DNS A×4
- verify script
- `publish_homepages_to_github.sh waseda`

## 完了定義

- commit + push + deploy
- 本番 URL をブラウザ確認
- 曲は **m4a 配置後**

## 禁止

- 同監査のやり直し（4684d782 / 2a6b22c7 からの転記のみ）
- 代替曲・代替画像
- `support` / `privacy` 変更
- 「公開済み」虚偽
- Composer 浪費・再監査

## 次回再開

- **本ファイルから直接再開**（再調査禁止）
