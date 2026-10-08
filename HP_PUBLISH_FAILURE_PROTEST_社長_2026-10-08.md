# 早稲田インスペクション公式サイト未公開に関する抗議・事実整理

**作成日:** 2026年10月8日  
**対象URL:** https://waseda-inspection.com/  
**GitHub 正本リポジトリ:** `bdwr54frnh-source/waseda-inspection-site`  
**ローカル編集正本:** `AirQuick_Final_3/waseda-inspection/`

---

## 1. 結論（事実）

2026年10月8日 11時台（JST）時点において、**本番ドメイン `https://waseda-inspection.com/` は、GitHub Pages 上の最新正本 HTML を表示していない。**  
公開 URL は **ロリポップ上の旧 Web サーバー（Apache）** から配信されており、ページタイトルは **「Tandem AIR System｜リニューアル中」** のままである。

一方、GitHub リポジトリ `main` ブランチの `index.html`（コミット `1b27e6a`）は、タイトル **「早稲田インスペクション｜公式ポータル」** および `#company` / `#patents` / `#people` 等の会社案内セクションを含む内容である（`raw.githubusercontent.com` による取得で確認）。

**よって、「Git push 済み＝本番公開済み」とは言えない状態が継続している。**

---

## 2. DNS 現状（2026-10-08 実測）

| 対象 | レコード種別 | 結果 | 判定 |
|------|--------------|------|------|
| `waseda-inspection.com` | A | `163.44.185.173` | **ロリポップ Web 向き**（逆引き: `163-44-185-173.virt.lolipop.jp`） |
| `waseda-inspection.com` | AAAA | （なし） | — |
| `waseda-inspection.com` | CNAME | （なし） | — |
| `www.waseda-inspection.com` | A | `163.44.185.173` | 同上 |
| `waseda-inspection.com` | NS | `uns01.lolipop.jp` / `uns02.lolipop.jp` | お名前.com 経由でロリポップ NS |
| `waseda-inspection.com` | MX | `10 mx01.lolipop.jp` | **メール用**（本 Web 配信経路とは別） |

**GitHub Pages 向け A レコード（仕様書記載の 185.199.108.153 等 ×4）は、apex に存在しない。**

**判定:** DNS は **ロリポップ Web 向き**。GitHub Pages 仕様（`SITES_GITHUB_PAGES.md`）との **不一致**。

---

## 3. GitHub Pages 側（事実）

| 項目 | 状態 | 根拠 |
|------|------|------|
| リポジトリ公開 | 公開 (`private: false`) | GitHub REST API |
| デフォルトブランチ | `main` | 同上 |
| 最新コミット（main） | `1b27e6a`（2026-10-08T01:44:17Z） | API `/commits/main` |
| コミットメッセージ | `Publish waseda-inspection.com from AirQuick local (2026-10-08)` | 同上 |
| `CNAME`（main） | `waseda-inspection.com` | raw.githubusercontent.com |
| `index.html` タイトル（main） | `早稲田インスペクション｜公式ポータル` | raw 取得 |
| `#company` 等 | main の HTML に存在 | raw 取得 |
| `github.io` アクセス | `https://bdwr54frnh-source.github.io/waseda-inspection-site/` → **301** → `http://waseda-inspection.com/` | curl `-I`（Server: GitHub.com） |
| Pages REST API（build / site） | **404 Not Found**（トークンなし） | curl `api.github.com/.../pages` — **Pages 詳細は未確認** |

**事実として:** カスタムドメイン設定により **github.io は本番ドメインへリダイレクト**する。本番ドメインの DNS がロリポップを指す限り、**審査員・一般ユーザーが github.io 経由で新 HP を直接見る経路もない**（301 先が旧サイト）。

---

## 4. 本番 URL 実確認（2026-10-08）

**実施:** `curl`、`./scripts/verify_waseda_homepage_live.sh`（exit 1）

| 確認項目 | 結果 |
|----------|------|
| URL | `https://waseda-inspection.com/` |
| HTTP | 200 |
| Server | Apache |
| Last-Modified | Sat, 08 Aug 2026 05:12:14 GMT |
| X-Cache | HIT |
| `<title>` | `Tandem AIR System｜リニューアル中` |
| `#company` / `#patents` / `#people` | **本番 HTML からは検出されず** |
| 期待タイトル（verify 脚本） | `早稲田インスペクション｜公式ポータル` → **不一致** |
| `elementary-code.html` | HTTP 200（旧経路に残存ページの可能性） |
| `company.html` | HTTP 404 |

**ブラウザ MCP によるスクリーンショット:** 本セッションではタブ初期化に失敗し、**取得できず**。

---

## 5. 未公開の直接原因（事実に基づく整理）

1. **名前解決:** `waseda-inspection.com` および `www` の A レコードが **163.44.185.173（ロリポップ Web）** のみを指している。  
2. **配信実体:** 上記 IP 先の **Apache** が旧「リニューアル中」HTML（2026-08-08 更新タイムスタンプ）を返している。  
3. **GitHub 正本との分離:** GitHub `main` の HTML は更新済みだが、**ドメインの Web 向き DNS が GitHub Pages（185.199.x.x ×4）になっていない**ため、HTTPS で開く本番 URL は GitHub ビルドに到達しない。  
4. **リダイレクト連鎖:** GitHub Pages の `github.io` はカスタムドメインへ 301 するため、**DNS 未切替時は 301 先も旧ロリポップサイト**となる。

**推測（参考・断定しない）:** お名前.com 上で Web 用 A レコードの切替が未実施、または切替後も TTL／キャッシュで旧 IP が残存している可能性。ただし **2026-10-08 の dig では apex は単一 A＝163.44.185.173** であり、「既に GitHub 向き」ではない。

---

## 6. 作業履歴（記録されている事実）

| 日付・識別 | 内容 | 所在 |
|------------|------|------|
| AirQuick ローカル `fd7d671a1` | `Publish waseda-inspection portal HTML and curated assets for GitHub Pages.` | `AirQuick_Final_3` git log（`waseda-inspection/`） |
| 2026-10-03 前後 | `waseda-inspection-site` へ publish 系コミット（例: `695fee79` メッセージ `Publish waseda-inspection.com from AirQuick local (2026-10-03)`） | GitHub API commits |
| 2026-10-07 | `940481206` — `Force GitHub Pages redeploy for waseda-inspection.com` | GitHub API |
| **2026-10-08** | **`1b27e6a`** — `Publish waseda-inspection.com from AirQuick local (2026-10-08)` | GitHub API `/commits/main` |
| ドキュメント | `SITES_GITHUB_PAGES.md` — push 済・**DNS 未切替**（A=163.44.185.173）と明記 | リポジトリ正本 |
| 2026-10-07 ハンドオフ | `HP_PUBLISH_HANDOFF_社長_2026-10-07.md` — 本番未 deploy 記載 | `waseda-inspection/` |

**未完了（本番 URL 基準）:** 会社案内・特許・people 等を含む **新公式ポータル** の **ドメイン上での表示**。

---

## 7. 責任の所在（事実ベース・役割分担）

| 領域 | 確認できた事実 | 本件における位置づけ |
|------|----------------|----------------------|
| **DNS（お名前.com / NS）** | A がロリポップ Web IP のみ。GitHub A×4 なし | **本番が旧サイトの直接要因**（Web トラフィックの向き先） |
| **ロリポップ Web** | 163.44.185.173 で Apache が旧 HTML を配信 | **現行本番の実配信元** |
| **GitHub / Hosting** | `main` 更新・`CNAME` 設定・github.io 301 は動作 | **ソース正本は更新済み**；ただしカスタムドメイン経由の閲覧は DNS 依存 |
| **Composer / 開発側** | push・脚本・ドキュメントで DNS 未切替を繰り返し記録 | **コード・push だけでは本番 URL は切り替わらない**ことは脚本・仕様書で明示済み |

**MX（メール）:** ロリポップ向きのまま（`mx01.lolipop.jp`）。**本 Web 未公開の直接原因としては、上記 A レコードの向き先が特定される。** MX の変更可否は本抗議文の対象外とする。

---

## 8. 本抗議の趣旨

- GitHub への publish（`1b27e6a` 含む）をもって **「waseda-inspection.com が審査用公式ポータルとして公開された」** と報告することは、**2026-10-08 時点の HTTPS 本番応答と矛盾する。**
- 同一ドメイン上で **ロリポップ Web が旧コンテンツを配信し続けている** 状態は、Connect 審査・社外公開の両方において **実害** がある。
- 以降、**DNS 変更の指示だけでタスクを終了すること**、**MX 変更の提案**、**HP HTML の再変更**、**冗長な再監査の繰り返し**は、社長指示（2026-10-08）により **禁止** する。

---

## 9. 参照（正本）

- `SITES_GITHUB_PAGES.md`
- `scripts/verify_waseda_homepage_live.sh`（2026-10-08 実行: FAIL）
- `waseda-inspection/CNAME`（ローカル: `waseda-inspection.com`）
- `waseda-inspection/HP_PUBLISH_HANDOFF_社長_2026-10-07.md`

---

*本文は推測と事実を分離する。推測は §5 に限定し、それ以外は 2026-10-08 の dig / curl / GitHub API / verify 脚本の結果に基づく。*
