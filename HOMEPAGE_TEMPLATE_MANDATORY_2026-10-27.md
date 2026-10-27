# ホームページ制作 — 専用テンプレ正本（社長 2026-10-27）

**テンプレを使わない制作・修正は禁止。** 新レイアウトの独自作成も禁止。

## 正本ファイル（サイト別）

| サイト | テンプレ正本 | 試作（非公開） |
|--------|----------------|----------------|
| 早稲田ポータル | `waseda-inspection/index.html` | `waseda-inspection/preview/*.html` |
| ELEMENTARY CODE 8コマ | `preview/elementary-comic-live-confirm.html` ＋ `preview/css/ec-comic-fullbleed.css` | 同上（8766） |
| EC トップ（Pages） | `elementarycode-tokyo/index.html` | 社長 GO 前は preview 側で確認 |
| 世界時計ブロック | `index.html#world-clocks`（見出し → 3都市 LIVE → 代表ポスター） | `preview/world-time-3cities-live-confirm.html` |

素材分離: `HP_THREE_TOPS_ASSET_POLICY.md`  
写真枠・代表: `PHOTO_ASSET_MAP.md` · `assets/HP_CURATED_ASSETS.md`

## タイポグラフィ固定（ポータル `index.html`）

**勝手に変えない。** 子ども向けに「大きく」する場合も、下表 **より小さくしない**。画像内文字は PNG/Keynote 差し替え。

| 要素 | サイズ | 行間 |
|------|--------|------|
| body 基本 | 継承 · **line-height 1.85** | 固定 |
| `.top-bar h1` | `clamp(22px, 4.5vw, 32px)` | — |
| `.top-bar .tagline` | **14px** | — |
| `.nav a` | **11px**（ナビのみ小さめ可） | — |
| `.brand-ladder` | **13px** · line-height **1.65** | 固定 |
| `.portal-card h2` | テンプレ内既存値 | 触らない |
| `.lead` / セクション本文 | **14px 前後**（13px 未満にしない） | 1.85 系 |

新規セクションを足す場合: **既存 `section` の class と padding をコピー**する。ゼロから CSS を書かない。

## 写真スペース

- 代表: `#representative` · `team-kiyoshi-approved-20261020.jpg`（専用 `img` 枠）
- EC ポスター: `hp_promo_elementary_code_infographic.jpg`（リンク付き枠）
- AIR 実機: `.device-showcase` / `.shot-pair` 等 — **grid テンプレを維持**

## 漫画・時計・認証

- 8コマ: **1024×678 PNG 1枚** · 社長指示どおり **第2コマ LIVE あり/なし**（指示がない限り現状維持）
- `ec-live-clock.js`: **変更禁止**（世界時計欄で使用可）
- 公開用コード ▪ 逆配置等: アプリ／Policy 正本どおり · 漫画に内部ロジックを書かない

## 文字が薄くかすれたとき

1. ブラウザや CSS で **拡大しない**
2. Keynote 等で **同サイズ・太め** に文字を貼り直し
3. 正本 PNG を `preview/assets/originals/*_READONLY.png` に保存して差し替え

## 公開前チェック

- [ ] PC 幅（1024 前後）で全セクション
- [ ] iPhone 幅（390 前後）で折り返し・はみ出しなし
- [ ] 漫画・時計・認証は社長指定どおり変更のみ
- [ ] 本番 push は社長 GO

Cursor ルール: `.cursor/rules/homepage-mandatory-template-2026-10-27.mdc`
