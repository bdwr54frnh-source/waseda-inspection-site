# waseda-inspection.com 公開 — 振り分け（2026-10-03 大至急）

## 結論

| レイヤ | 状態 | 担当 |
|--------|------|------|
| **GitHub 正本** | ✅ `waseda-inspection-site` の `main` に「早稲田インスペクション｜会社案内」 | **コンちゃん** — 済（push 不要ならスキップ可） |
| **GitHub Pages** | ✅ `CNAME` = `waseda-inspection.com` · `.nojekyll` あり | コンちゃん — 済 |
| **本番ドメイン** | ❌ A = `163.44.185.173`（ロリポップ）→ 旧「リニューアル中」 | **社長 or コパイロット** — **お名前.com のみ** |

**審査員が Connect の URL を開いても古いページになる理由は DNS だけ。** コード・GitHub 側の追加作業では直りません。

---

## 社長 / コパイロット — 今すぐ（5分）

1. [お名前.com](https://www.onamae.com/) → ドメイン **`waseda-inspection.com`** → **DNS 設定**
2. **MX レコードは触らない**（メール継続）
3. TYPE **A** で **`163.44.185.173`** を **削除**
4. TYPE **A** ホスト **`@`** を **4 行** 追加（VALUE はそのままコピー）:

   | TYPE | ホスト | VALUE |
   |------|--------|--------|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |

5. 保存 → **5〜30 分**待つ
6. GitHub → `bdwr54frnh-source/waseda-inspection-site` → **Settings → Pages**  
   - Custom domain: `waseda-inspection.com`  
   - **Enforce HTTPS** が出たら ON

詳細表: リポジトリ直下 `SITES_ONAMAE_DNS_入力表.md`（waseda は tandem と同じ A×4）

---

## コンちゃん — Mac 側（DNS 前後）

```bash
cd "/Users/kiyoshisekine/Desktop/保存/AirQuick_Final_3"
chmod +x scripts/verify_waseda_homepage_live.sh
./scripts/publish_homepages_to_github.sh waseda   # ローカル変更があるときだけ
./scripts/verify_waseda_homepage_live.sh            # DNS 後に OK が出るまで
```

**成功条件（審査）**

- https://waseda-inspection.com/ → タイトル **早稲田インスペクション｜会社案内**
- https://waseda-inspection.com/#company → 事業者情報
- https://waseda-inspection.com/privacy.html

---

## コパイロットに貼る依頼文（そのまま）

```
waseda-inspection.com の App Store 審査用 HP は GitHub Pages に push 済み。
dig waseda-inspection.com A は 163.44.185.173（ロリポップ）のままなので、
https://waseda-inspection.com/ は旧「Tandem AIR System｜リニューアル中」を返す。

お名前.com で A 163.44.185.173 を削除し、GitHub Pages の A×4（185.199.108–111.153）を @ に追加。
MX は変更しない。保存後 Enforce HTTPS。検証は verify スクリプトまたはシークレット窓で #company。
```

---

## シャッター・チャット

- **チャット審査** … HP URL と無関係なら並行可
- **Connect のサポート URL** … **DNS 完了まで審査リスクあり** → HP を先に

---

## 参考（2026-10-03 09:05 JST 計測）

- `dig waseda-inspection.com A` → `163.44.185.173`
- GitHub clone `waseda-inspection-site` → `index.html` タイトルは正本どおり
- `https://bdwr54frnh-source.github.io/waseda-inspection-site/` → 301 で `http://waseda-inspection.com/`（カスタムドメイン設定のため、**DNS 修正まで中身は旧サイト**）
