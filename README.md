# My Connect Wi-Fi

場所と状況に応じて最適なWi-Fi接続を提案するAndroidアプリ

## 概要

**My Connect Wi-Fi**は、登録したWi-Fiネットワークを優先順位に基づいて管理し、より優先度の高いネットワークが検出された際に通知でお知らせするアプリです。

### 主な機能

- 📶 **Wi-Fiネットワークのスキャン**: 周囲の利用可能なネットワークを自動検出
- 🔢 **優先順位管理**: 各Wi-Fiに優先順位を設定し、自動的に最適な接続を提案
- 🔕 **一時的な除外**: 「今日だけ無視」で特定のネットワークを一時的にスキップ
- ⛔ **永続的な除外**: 「次回まで無視」で手動解除するまで接続候補から除外
- 🔐 **ライセンス管理**: 5つ目以降のWi-Fi登録にはライセンスキーが必要
- ☁️ **Google Sheets連携**: ライセンス認証をクラウドで管理

## 技術スタック

- **フレームワーク**: Python / Flet (Android Build)
- **データベース**: ローカルJSON + Google Sheets API
- **暗号化**: cryptography (パスワード暗号化)
- **プラットフォーム**: Android (開発環境: Windows/Mac/Linux)

## インストール

### 開発環境でのセットアップ

```bash
# 依存関係のインストール
pip install -r requirements.txt

# アプリケーションの実行
python main.py
```

### Android用ビルド

Fletアプリケーションをandroid APKにビルドするには、以下のコマンドを使用します：

```bash
flet build apk
```

‼️ **重要**: Android向けビルド時には、適切な権限設定が必要です。

## Android権限設定

Android環境でWi-Fi操作を行うには、以下の権限が必要です。

`android/app/src/main/AndroidManifest.xml` に以下を追加してください:

```xml
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.INTERNET" />
```

## 使い方

### 1. Wi-Fi設定の追加

1. 右下の「+」ボタンをタップ
2. 「スキャンから選択」または「手動入力」を選択
3. SSID とパスワードを入力
4. 「今すぐ接続を試しますか？」で接続テストが可能

### 2. 優先順位管理

- Wi-Fiは登録順に優先順位が割り当てられます
- 優先順位1が最も高く、数字が大きいほど優先度が低くなります

### 3. 一時的な除外

「今日だけ無視」スイッチをONにすると、その日の00:00まで接続候補から除外されます。

### 4. 永続的な除外

「次回まで無視」スイッチをONにすると、手動でOFFにするまで接続候補から除外されます。

### 5. ライセンス認証

- **1〜4つ目のWi-Fi**: 無料で登録可能
- **5つ目以降**: ライセンスキーが必要

#### テスト用ライセンスキー

開発環境では以下のテストキーが使用できます：

- `TEST-KEY-001`: 3台まで、現在0台使用中
- `TEST-KEY-002`: 5台まで、現在4台使用中

## Google Sheets APIの設定（本番環境）

本番環境でライセンス管理機能を使用する場合:

1. **Google Cloud Platformでプロジェクトを作成**
2. **Google Sheets APIを有効化**
3. **サービスアカウントを作成し、認証情報JSONをダウンロード**
4. **認証情報ファイルを配置**:
   ```
   credentials/google_sheets_credentials.json
   ```

5. **スプレッドシートの構造**:

   | LicenseKey    | MaxLimit | ActiveCount |
   |---------------|----------|-------------|
   | ABC-123-XYZ   | 3        | 0           |
   | DEF-456-UVW   | 5        | 2           |

6. **LicenseManagerの初期化を変更**:
   ```python
   license_manager = LicenseManager(
       credentials_file="credentials/google_sheets_credentials.json"
   )
   license_manager.set_spreadsheet(
       spreadsheet_url="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID",
       worksheet_name="Sheet1"
   )
   ```

## プロジェクト構造

```
My_Connect_Wi-Fi/
├── main.py                     # メインアプリケーション
├── requirements.txt            # 依存関係
├── README.md                   # このファイル
├── models/
│   ├── __init__.py
│   └── wifi_config.py          # Wi-Fi設定データモデル
├── services/
│   ├── __init__.py
│   ├── storage_manager.py      # ローカルストレージ管理
│   ├── wifi_manager.py         # Wi-Fiスキャン・接続管理
│   └── license_manager.py      # ライセンス認証管理
└── ui/
    ├── __init__.py
    ├── dashboard.py            # メイン画面
    ├── wifi_card.py            # Wi-Fiカードコンポーネント
    ├── add_wifi_dialog.py      # Wi-Fi追加ダイアログ
    └── license_dialog.py       # ライセンス認証ダイアログ
```

## データストレージ

アプリのデータは以下の場所に保存されます：

- **パス**: `~/.my_connect_wifi/config.json`
- **暗号化キー**: `~/.my_connect_wifi/encryption.key`

### データ構造

```json
{
  "user_settings": {
    "scan_interval_seconds": 300,
    "notifications_enabled": true
  },
  "wifi_configs": [
    {
      "id": "uuid_1",
      "ssid": "MyHome_5G",
      "password": "encrypted_password",
      "priority": 1,
      "status_flags": {
        "ignore_today": false,
        "ignore_until_manual_reset": false,
        "last_ignored_date": null
      }
    }
  ],
  "license_info": {
    "is_pro_unlocked": false,
    "activated_keys": []
  }
}
```

## 今後の実装予定

- [ ] バックグラウンドスキャン機能
- [ ] 通知システム（優先度の高いWi-Fi検出時）
- [ ] Android 10以降のWi-Fi接続対応
- [ ] 接続履歴の記録
- [ ] 自動接続設定
- [ ] ダークモード/ライトモードの切り替え

## トラブルシューティング

### Wi-Fiスキャンが動作しない

開発環境（Windows/Mac）ではモックデータが表示されます。実際のスキャン機能はAndroidビルド時に有効になります。

### ライセンス認証エラー

- 開発環境ではモックモードで動作します
- テストキー `TEST-KEY-001` を使用してください
- 本番環境ではGoogle Sheets APIの設定が必要です

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 開発者

Developed with ❤️ using Flet and Python
