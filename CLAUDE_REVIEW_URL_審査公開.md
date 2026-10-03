# クロード用 — waseda-inspection.com 審査公開（社長がそのまま貼る）

## 依頼（一言）

**App Store Connect が指している URL を、審査員が開いて会社案内・プライバシーが読める状態に公開してください。ローカル完成版はある。本番ドメインだけ古い。**

---

## 事実（2026-10-03 朝 — コンちゃん再計測）

| 追加確認 | 結果 |
|----------|------|
| GitHub `main` clone | タイトル **「早稲田インスペクション｜会社案内」**（push 済み・追加 push 不要） |
| `dig A` TTL 600 | 仍 **`163.44.185.173` のみ** → **唯一のブロッカー** |
| 振り分け正本 | `waseda-inspection/DNS_URGENT_振り分け_2026-10-03.md` |
| Mac 検証 | `./scripts/verify_waseda_homepage_live.sh` |

## 事実（2026-10-02 夕方更新）

| 項目 | 状態 |
|------|------|
| 審査が見る URL | `https://waseda-inspection.com/` · `privacy.html` · `#company`（`AppStoreConnectListingPolicy` 正本） |
| **本番の定義（仕様書）** | `SITES_GITHUB_PAGES.md` / `SITES_LOLIPOP_GITHUB_HANDOFF.md` — **GitHub push ＋ DNS A→GitHub** まで。**ローカル完成・FTP は本番ではない** |
| **本番トップ（ドメイン）** | まだ **「Tandem AIR System｜リニューアル中」**（Apache・`163.44.185.173`）→ Connect と不一致 |
| DNS A | `163.44.185.173`（ロリポップ Web）→ **未切替** |
| GitHub `waseda-inspection-site` | **push 済** `b70c3bf` — `main/index.html` タイトル **「早稲田インスペクション｜会社案内」** · Micon 等 |
| ローカル正本 | 同上（`waseda-inspection/`）。編集後は再 push |

**結論**: GitHub 正本は審査用。**審査員が開く URL が変わるのは DNS 切替後。** それまでは仕様上「本番未完了」。

---

## 成功条件（審査員が確認できること）

シークレット窓ですべて **200** かつ本文が新サイト:

1. https://waseda-inspection.com/ → タイトル「早稲田インスペクション｜会社案内」
2. https://waseda-inspection.com/#company → 事業者名・代表・住所・メール
3. https://waseda-inspection.com/privacy.html → 事業者情報セクションあり
4. https://waseda-inspection.com/support.html → 問い合わせ（あれば）

---

## 作業（どちらか1つ・社長 Mac で実行）

### 正攻法 — GitHub push + DNS（ロリポップ解約・FTP 不可）

```bash
cd "/Users/kiyoshisekine/Desktop/保存/AirQuick_Final_3"
./scripts/publish_homepages_to_github.sh
```

（waseda 部分だけでも可: ローカル `waseda-inspection/` → clone `bdwr54frnh-source/waseda-inspection-site` → rsync → commit → push）

**お名前.com**: A `163.44.185.173`（ロリポップ Web）をやめ、GitHub Pages 4 IP。**MX** は解約前に `info@` 移行先へ（`EMAIL_SETUP.md`）。解約後は `mx01.lolipop.jp` 不可。

---

## 触るな

- ドメイン名 `waseda-inspection.com` 変更禁止
- 特許番号: 特願2025-189376 / 特願2026-65348（事実変更禁止）
- HP に顔アップ代表写真を載せない（社長方針）
- `apple_music_glass_tile_*.jpg` の inpaint 合成禁止（社長正本のみ）

## 返してほしいもの

1. 上記 4 URL の検証結果（タイトル1行ずつ）
2. 使った手段（FTP / DNS+push）
3. push した場合: commit hash

---

## ローカルプレビュー（公開前）

```bash
cd "/Users/kiyoshisekine/Desktop/保存/AirQuick_Final_3/waseda-inspection"
python3 -m http.server 8765
# http://127.0.0.1:8765/#company
```
