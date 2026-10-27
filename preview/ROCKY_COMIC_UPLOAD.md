# ロッキー作 · ELEMENTARY CODE 漫画アップ手順（確認用のみ）

本番 elementarycode.tokyo / main への反映は社長 GO まで禁止。

## 指定テンプレート

- ページ正本: `elementary-comic-live-confirm.html`
- LIVE 時計: 第2コマ MacBook · `.comic-panel2-screen`（四隅 clip-path）＋ `.comic-panel2-static-mask`（固定時刻行のみ `rgb(4,23,56)`）＋ `#comic-panel2-clock`（小さめ LIVE · `rotate(-2.35deg)`）· `ec-live-clock.js` **変更禁止**
- 本番表示: `.ec-comic-fullbleed` ＋ 横幅 **100%**（余白トリミング済み PNG をそのまま大きく）
- スクリプト: `js/ec-live-clock.js`（触らない）

## 置き場所（ファイル名固定）

| ファイル | 用途 |
|----------|------|
| `preview/assets/elementary_code_rocky_8panel.png` | 1〜8コマ（現行 **1024×678** 横長トリミング · LIVE は `ec-comic-fullbleed.css`） |
| `waseda-inspection/assets/elementary_code_rocky_8panel.png` | 本番用ミラー（社長 GO まで未デプロイ） |

10コマを**1枚縦長**で作る場合は、上 1199px が旧8コマと同じ寸法・構図になるよう分割 export し、上段だけ `elementary_code_rocky_8panel.png` にしてください（LIVE オーバーレイのため）。

## アップ後の確認

1. `cd waseda-inspection/preview && python3 -m http.server 8766`
2. http://127.0.0.1:8766/elementary-comic-live-confirm.html
3. 第2コマ PC 内時計が東京・100分の1秒で動くこと
4. PC / iPhone で全コマ文字の重なりなし

## 旧 PIL 差し替え（参考）

けんちゃん側の `preview/tools/build_comic_confirm.py` は、ロッキー PNG 差し替え後は**使わなくてよい**（正本 `elementary_code_correct_8panel.png` は保管用のまま）。

## ロッキー向けチェック

- 吹き出し内文案は完成 PNG に含める（HTML 白オーバーレイなし）
- 内部ロジック・双子コード・数字配置の説明は載せない
- 人物・背景・構図は社長指示どおり
