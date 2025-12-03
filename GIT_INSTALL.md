# Git インストールガイド

## Windows用 Git のインストール

### 方法1: 公式インストーラー（推奨）

1. **ダウンロード**
   - https://git-scm.com/download/win にアクセス
   - 「64-bit Git for Windows Setup」をクリックしてダウンロード

2. **インストール**
   - ダウンロードしたインストーラーを実行
   - すべてデフォルト設定のまま「Next」をクリック
   - インストール完了後、PowerShellを再起動

3. **確認**
   ```powershell
   git --version
   ```
   バージョン情報が表示されればOK

### 方法2: wingetを使用

```powershell
winget install --id Git.Git -e --source winget
```

### インストール後

Gitのインストール後、再度APKビルドコマンドを実行してください：

```powershell
flet build apk --project "MyConnectWiFi" --org "com.myconnect"
```

## 代替案: Chocolateyを使用

```powershell
# 管理者権限で実行
choco install git
```
