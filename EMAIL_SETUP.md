# waseda-inspection.com メール（ロリポップ解約後）

## 正本（表記・2件 — 変わらない）

| 順 | アドレス | 役割 |
|----|----------|------|
| 1 | **info@waseda-inspection.com** | 公開・Connect 第一 |
| 2 | **waseda-inspection@outlook.com** | 第二・**スマホは今まで通り** |

コード: `AirFaceOfficialContactPolicy`

---

## 重要（ロリポップ解約）

- **Web（HP）** … ロリポップ FTP **使わない**。正本は **GitHub Pages** → `./scripts/publish_homepages_to_github.sh` ＋ お名前.com の **A を GitHub 4 IP**
- **メール** … 解約すると **mx01.lolipop.jp の受信は止まる**。解約**前**に `info@` の **MX を別サービスへ移す**か、移行完了まで Connect は **Outlook のみ** も可（HP は2件表記のままでよい）

---

## info@ の移行先（どれか1つ）

### A. Microsoft（Outlook と同じスマホ操作 — 社長向け）

- **Microsoft 365** または Outlook で **独自ドメインを追加**（プラン要確認）
- `info@waseda-inspection.com` を作成 → iPhone **Outlook アプリ**で追加アカウント（今まで通り）

### B. お名前.com メール / ムームーメール

- お名前の **メールホスティング** にドメイン追加 → MX をお名前案内どおり変更 → スマホ IMAP（ベンダー表記どおり）

### C. 転送専用（受信は Outlook に集約）

- Cloudflare Email Routing / ForwardEmail 等で **info@ → waseda-inspection@outlook.com**
- お名前.com の **MX だけ** 転送サービス向けに変更
- スマホは **Outlook だけ** 見る（今まで通り）

---

## 解約前チェック（順番）

1. [ ] GitHub に HP push → DNS A を GitHub → `https://waseda-inspection.com/#company` 確認  
2. [ ] **info@** の MX 移行 → テスト送信で受信  
3. [ ] **Outlook** 受信確認（変更なし）  
4. [ ] App Store Connect サポートメール = **info@**（届く状態）または暫定 Outlook  
5. [ ] 上記 OK 後にロリポップ **Web 停止 → 解約**

詳細: リポジトリ直下 `SITES_LOLIPOP_GITHUB_HANDOFF.md` チェックリスト C・D

---

## iPhone（今まで通り）

| アカウント | 操作 |
|------------|------|
| **waseda-inspection@outlook.com** | **変更しない**（Outlook アプリ / Apple メールの Microsoft） |
| **info@waseda-inspection.com** | 移行先（A/B）の IMAP を **追加**。C の転送なら **追加不要**（Outlook だけで可） |

---

## 審査

- サポート URL: `https://waseda-inspection.com/`（GitHub 正本が見えること）
- メール: HP `#company` と Connect が一致
