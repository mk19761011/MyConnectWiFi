# My Connect Wi-Fi - Android APK用設定

## アプリ情報
- **アプリ名**: My Connect Wi-Fi
- **パッケージ名**: com.myconnect.wifi
- **バージョン**: 1.0.0
- **ビルド番号**: 1

## 必要な権限
- ACCESS_WIFI_STATE
- CHANGE_WIFI_STATE  
- ACCESS_FINE_LOCATION
- ACCESS_COARSE_LOCATION
- INTERNET

## ビルド手順

### 準備
1. Android SDKがインストールされていること
2. Java JDK 11以降がインストールされていること

### ビルドコマンド
```bash
flet build apk \
  --project "My Connect Wi-Fi" \
  --org "com.myconnect" \
  --build-version "1.0.0" \
  --build-number 1 \
  --android-permissions "ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET"
```

### 出力先
ビルドされたAPKファイルは以下に出力されます：
`build/apk/app-release.apk`
