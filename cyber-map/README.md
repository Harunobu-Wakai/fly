# サイバー攻撃マップ

世界中でいまどれくらいサイバー攻撃が起きているかを、暗い世界地図の上を飛ぶ光の弧で見せる、Kaspersky Cybermap 風のリアルタイム可視化です。

`index.html` をブラウザで直接開くだけで動きます。ビルド不要で、ネット接続もいりません（地図データとライブラリは `vendor/` に同梱）。

モードは2つあります。

- **世界（デモ）**: 世界中の攻撃の様子を模擬データで見せます。
- **あなたのPC**: 自分のWindows PCのファイアウォールログを読み込み、実際にどこの国から、どの入口（ポート）を狙われたかを表示します。

## あなたのPCモードの使い方

1. 管理者のPowerShellで、ブロックした通信の記録をオンにします。
   ```powershell
   Set-NetFirewallProfile -Profile Domain,Public,Private -LogBlocked True -LogMaxSizeKilobytes 32767
   ```
2. 数時間〜1日ほど普段どおりPCを使います。
3. ログをデスクトップにコピーします（管理者PowerShell）。
   ```powershell
   Copy-Item "$env:SystemRoot\System32\LogFiles\Firewall\pfirewall.log" "$env:USERPROFILE\Desktop\pfirewall.log"
   ```
4. 画面右上の「あなたのPC」を押し、`pfirewall.log` をドラッグして読み込みます。

ログはブラウザの中だけで処理され、外部には送信されません。IPアドレスから国を調べるデータも同梱しているのでオフラインで動きます。

- 家のルーター（NAT）の内側にあるPCは、外からの通信をまずルーターが止めるため、件数が少ないかゼロになることがあります。
- LAN内の通信（192.168.x.x など）は攻撃として数えず、別に件数だけ表示します。
- 攻撃の種類は狙われたポートからの推定です（3389=リモートデスクトップ → 遠隔操作ねらい、445=SMB → ファイル共有ねらい など）。
- 「あなたのPC」の位置は東京に置いています。
- 記録をやめるときは `Set-NetFirewallProfile -Profile Domain,Public,Private -LogBlocked False`。

## 画面の見方（世界モード）

- **光の弧**: 1本が1件の攻撃です。攻撃元から標的へ飛び、着弾すると波紋が広がります。色は攻撃の種類を表します。
- **本日の検知数**: 深夜0時からの累計です（表示されている弧1本 = 約137件として換算）。
- **攻撃元 TOP / 標的 TOP**: ページを開いてからの国別ランキングです。
- **ヒートマップ**: よく攻撃されている国ほど赤く光り、時間が経つと徐々に冷めます。
- **DDoS波**: ときどき複数の国から1つの国へ集中攻撃が起きます。ボタンで手動発生も可能です。
- 国の点にマウスを乗せると、その国の件数が表示されます。

## 注意点

世界モードで表示しているのは**模擬データ**です。攻撃元・標的の国の偏りや攻撃種別の割合は、公開されている脅威レポートの傾向をざっくり参考にした重み付き乱数で、実際の観測値ではありません。

本物のデータに置き換える場合は、`spawn(src, dst, type)` を AbuseIPDB や Shodan、自前のハニーポット/ファイアウォールのログなどから呼び出すようにしてください。

## 同梱ライブラリ

- [d3-geo](https://github.com/d3/d3-geo) / [d3-array](https://github.com/d3/d3-array)（ISC）
- [topojson-client](https://github.com/topojson/topojson-client)（ISC）
- [world-atlas](https://github.com/topojson/world-atlas) countries-110m（Natural Earth 由来、ISC）
- [ip-location-db](https://github.com/sapics/ip-location-db) geo-whois-asn-country IPv4（CC0。元データは [NRO](https://www.nro.net) の統計、CC BY 4.0）。`tools/build_ipv4_country.py` で `vendor/ipv4-country.js` に圧縮しています。国コードの数値対応は [i18n-iso-countries](https://github.com/michaelwittig/node-i18n-iso-countries)（MIT）から生成。
