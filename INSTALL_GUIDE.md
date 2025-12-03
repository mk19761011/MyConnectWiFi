# My Connect Wi-Fi - インストールガイド

## 📱 Android APKのインストール

### 方法1: 直接インストール（推奨）

1. **APKファイルの取得**
   - ビルド完了後、`build/apk/app-release.apk` ファイルが生成されます
   - このファイルをAndroidデバイスに転送します

2. **Androidデバイスでの設定**
   - `設定` → `セキュリティ` → `提供元不明のアプリ` を有効化
   - または `設定` → `アプリと通知` → `特別なアプリアクセス` → `不明なアプリのインストール` で許可

3. **インストール**
   - APKファイルをタップして開く
   - `インストール` をタップ
   - インストール完了後、`開く` をタップしてアプリを起動

### 方法2: ADB経由でインストール

Android Debug Bridge（ADB）を使用してインストールする方法：

```bash
# デバイスを接続し、USBデバッグを有効にする
adb devices

# APKをインストール
adb install build/apk/app-release.apk

# または既存アプリを上書き
adb install -r build/apk/app-release.apk
```

## 🔧 ビルド状態の確認

現在、以下のコマンドが実行中です：

```bash
flet build apk --project "My Connect Wi-Fi" \
  --org "com.myconnect" \
  --build-version "1.0.0" \
  --build-number 1 \
  --android-permissions "ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET"
```

### ビルドプロセス

1. ✅ Flutter SDKのダウンロード（進行中）
2. ✅ JDKのインストール（進行中）
3. ⏳ Android SDKのセットアップ
4. ⏳ プロジェクトのビルド
5. ⏳ APKの生成

**注意**: 初回ビルドは、必要なツール（Flutter、JDK、Android SDK）のダウンロードとインストールに **10〜30分** 程度かかる場合があります。

## 📦 ビルド完了後のファイル構成

```
My_Connect_Wi-Fi/
├── build/
│   └── apk/
│       ├── app-release.apk      # リリース版APK（署名なし）
│       └── app-debug.apk         # デバッグ版APK
```

## 🔐 APKの署名（本番リリース用）

Google Play Storeに公開する場合は、APKに署名が必要です：

### 1. キーストアの作成

```bash
keytool -genkey -v -keystore my-release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias my-key-alias
```

### 2. 署名付きAPKのビルド

```bash
flet build apk \
  --android-signing-key-store my-release-key.jks \
  --android-signing-key-store-password <パスワード> \
  --android-signing-key-password <キーパスワード> \
  --android-signing-key-alias my-key-alias
```

## 🌐 代替案: Webアプリとして使用

Androidビルドに時間がかかる場合、Webアプリとしてデプロイすることも可能です：

```bash
# Webアプリとして公開
flet publish --project "My Connect Wi-Fi"

# ローカルでWebサーバーとして実行
flet run --web
```

## ⚠️ トラブルシューティング

### ビルドが失敗する場合

1. **Flutterの再インストール**
   ```bash
   flet doctor
   ```

2. **キャッシュのクリア**
   ```bash
   # buildディレクトリを削除
   rmdir /s build
   ```

3. **依存関係の再インストール**
   ```bash
   pip install --upgrade flet
   ```

### インストールができない場合

- Androidのバージョンが古い場合（Android 5.0以上が必要）
- ストレージ容量が不足している場合
- セキュリティ設定で不明なアプリのインストールがブロックされている場合

## 📞 サポート

問題が発生した場合は、以下を確認してください：
- ビルドログの内容
- Androidデバイスのバージョン
- エラーメッセージの詳細
