import flet as ft
from services.storage_manager import StorageManager
from services.wifi_manager import WiFiManager
from services.license_manager import LicenseManager
from ui.dashboard import Dashboard


def main(page: ft.Page):
    """メインアプリケーション"""
    
    # ページ設定
    page.title = "My Connect Wi-Fi"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    # サービス初期化
    storage_manager = StorageManager()
    wifi_manager = WiFiManager()
    license_manager = LicenseManager()  # 開発環境ではモックモード
    
    # ダッシュボード作成
    dashboard = Dashboard(
        storage_manager=storage_manager,
        wifi_manager=wifi_manager,
        license_manager=license_manager,
        page=page
    )
    
    # FABを追加
    page.floating_action_button = dashboard.fab
    
    # ページに追加
    page.add(dashboard)


if __name__ == "__main__":
    # デスクトップアプリとして起動
    ft.app(target=main)
    
    # Android用ビルド時は以下を使用:
    # ft.app(target=main, view=ft.AppView.FLET_APP)
