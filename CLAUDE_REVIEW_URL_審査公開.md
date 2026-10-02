# クロード用 — waseda-inspection.com 審査公開（社長がそのまま貼る）

## 依頼（一言）

**App Store Connect が指している URL を、審査員が開いて会社案内・プライバシーが読める状態に公開してください。ローカル完成版はある。本番ドメインだけ古い。**

---

## 事実（2026-10-02 時点）

| 項目 | 状態 |
|------|------|
| 審査が見る URL | `https://waseda-inspection.com/` · `privacy.html` · `#company`（`AppStoreConnectListingPolicy` 正本） |
| **本番トップ** | タイトル **「Tandem AIR System｜リニューアル中」** — **`#company` なし** → 会社案内 URL が実質死んでいる |
| DNS A | `163.44.185.173`（ロリポップ）→ GitHub Pages ではない |
| GitHub `waseda-inspection-site` | リモートも **古い index** のまま（ローカル新 `早稲田インスペクション｜会社案内` は **未 push**） |
| ローカル正本 | `AirQuick_Final_3/waseda-inspection/index.html` に `#company` · `#bank` · 特許 · `privacy.html` 更新済み |

**結論**: URL は「公開されている」が **Connect に書いた内容と一致しない** → 審査落ちリスク大。

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
