import flet as ft
from typing import List
from models.wifi_config import WiFiConfig
from services.wifi_manager import WiFiManager
from services.storage_manager import StorageManager
from services.license_manager import LicenseManager
from ui.wifi_card import WiFiCard
from ui.add_wifi_dialog import AddWiFiDialog
from ui.license_dialog import LicenseDialog


class Dashboard(ft.Container):
    """メインダッシュボード画面"""
    
    def __init__(self, storage_manager: StorageManager, wifi_manager: WiFiManager, license_manager: LicenseManager, page: ft.Page):
        self.storage_manager = storage_manager
        self.wifi_manager = wifi_manager
        self.license_manager = license_manager
        self.page = page
        
        # ヘッダー
        self.status_text = ft.Text(
            "準備完了",
            size=16,
            color="green",
            weight=ft.FontWeight.BOLD
        )
        
        self.current_network_text = ft.Text(
            "",
            size=14,
            color="grey"
        )
        
        # Wi-Fiカードのリスト
        self.wifi_list_view = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
        )
        
        # 追加ボタン
        self.add_button = ft.IconButton(
            icon="add_circle",
            icon_size=40,
            on_click=self._on_add_wifi_clicked,
            tooltip="Wi-Fi設定を追加",
            icon_color="blue",
        )
        
        super().__init__(
            content=ft.Column([
                # ヘッダー
                ft.Container(
                    content=ft.Row([
                        ft.Icon("wifi", size=40, color="blue"),
                        ft.Container(width=10),
                        ft.Column([
                            ft.Text(
                                "My Connect Wi-Fi",
                                size=24,
                                weight=ft.FontWeight.BOLD
                            ),
                            self.current_network_text,
                        ], spacing=2),
                        ft.Container(expand=True),
                        ft.Column([
                            self.status_text,
                        ], horizontal_alignment=ft.CrossAxisAlignment.END),
                        ft.Container(width=10),
                        self.add_button,
                    ]),
                    padding=20,
                    bgcolor="surfacevariant",
                ),
                ft.Divider(height=1),
                # Wi-Fiリスト
                ft.Container(
                    content=self.wifi_list_view,
                    expand=True,
                ),
            ], spacing=0, expand=True),
            expand=True,
        )
        
        # 初期データ読み込み
        self.load_wifi_configs()
        self.update_current_network()
    
    def load_wifi_configs(self):
        """Wi-Fi設定を読み込んで表示"""
        wifi_configs = self.storage_manager.get_wifi_configs()
        self.wifi_list_view.controls.clear()
        
        if not wifi_configs:
            self.wifi_list_view.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon("wifi_off", size=80, color="grey"),
                        ft.Text(
                            "Wi-Fi設定がありません",
                            size=18,
                            color="grey"
                        ),
                        ft.Text(
                            "右下の「+」ボタンから追加してください",
                            size=14,
                            color="grey"
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=50,
                    alignment=ft.alignment.center
                )
            )
        else:
            for wifi in wifi_configs:
                card = WiFiCard(
                    wifi=wifi,
                    on_update=self._on_wifi_updated,
                    on_delete=self._on_wifi_deleted,
                    on_connect=self._on_wifi_connect
                )
                self.wifi_list_view.controls.append(card)
        
        if self.page:
            self.page.update()
    
    def update_current_network(self):
        """現在の接続ネットワークを更新"""
        current = self.wifi_manager.get_current_network()
        if current:
            self.current_network_text.value = f"現在の接続: {current}"
        else:
            self.current_network_text.value = "接続なし"
        
        if self.page:
            self.page.update()
    
    def _on_add_wifi_clicked(self, e):
        """Wi-Fi追加ボタンクリック"""
        # 最もシンプルなテスト：ステータステキストを変更するだけ
        print("Button clicked!")
        self.status_text.value = "ボタンが押されました！"
        self.status_text.color = "orange"
        self.update()
        
        # 元の処理（一旦コメントアウト）
        # try:
        #     print("Add button clicked - START")
        #     self.page.snack_bar = ft.SnackBar(
        #         content=ft.Text("ボタンがクリックされました"),
        #         bgcolor="blue"
        #     )
        #     self.page.snack_bar.open = True
        #     self.page.update()
        #     print("Add button clicked - SnackBar displayed")
        #     
        #     wifi_configs = self.storage_manager.get_wifi_configs()
        #     current_count = len(wifi_configs)
        #     print(f"Add button clicked - Current count: {current_count}")
        #     
        #     if current_count >= 4:
        #         print("Add button clicked - Checking license")
        #         license_info = self.storage_manager.get_license_info()
        #         if not license_info.get("is_pro_unlocked", False):
        #             print("Add button clicked - Showing license dialog")
        #             self._show_license_dialog()
        #             return
        #     
        #     print("Add button clicked - Showing add wifi dialog")
        #     self._show_add_wifi_dialog()
        #     print("Add button clicked - END")
        #     
        # except Exception as ex:
        #     import traceback
        #     error_msg = traceback.format_exc()
        #     print(f"ERROR in _on_add_wifi_clicked: {error_msg}")
        #     self.page.snack_bar = ft.SnackBar(
        #         content=ft.Text(f"エラー: {str(ex)}"),
        #         bgcolor="red"
        #     )
        #     self.page.snack_bar.open = True
        #     self.page.update()
    
    def _show_license_dialog(self):
        """ライセンスダイアログを表示"""
        dialog = LicenseDialog(
            license_manager=self.license_manager,
            on_success=self._on_license_success
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def _on_license_success(self, license_key: str):
        """ライセンス認証成功時"""
        # アクティベート済みキーを保存
        self.storage_manager.add_activated_key(license_key)
        
        # Wi-Fi追加ダイアログを表示
        self._show_add_wifi_dialog()
    
    def _show_add_wifi_dialog(self):
        """Wi-Fi追加ダイアログを表示"""
        try:
            print("_show_add_wifi_dialog - START")
            wifi_configs = self.storage_manager.get_wifi_configs()
            next_priority = len(wifi_configs) + 1
            print(f"_show_add_wifi_dialog - next_priority: {next_priority}")
            
            dialog = AddWiFiDialog(
                wifi_manager=self.wifi_manager,
                on_save=self._on_wifi_added,
                current_priority=next_priority
            )
            print("_show_add_wifi_dialog - dialog created")
            
            self.page.dialog = dialog
            dialog.open = True
            print("_show_add_wifi_dialog - dialog.open set to True")
            
            self.page.update()
            print("_show_add_wifi_dialog - page.update() called")
            
        except Exception as ex:
            import traceback
            error_msg = traceback.format_exc()
            print(f"ERROR in _show_add_wifi_dialog: {error_msg}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"ダイアログエラー: {str(ex)}"),
                bgcolor="red"
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _on_wifi_added(self, wifi: WiFiConfig, test_connection: bool = False):
        """Wi-Fi追加時"""
        self.storage_manager.add_wifi_config(wifi)
        self.load_wifi_configs()
        
        if test_connection:
            self._on_wifi_connect(wifi)
        
        # スナックバー表示
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"「{wifi.ssid}」を追加しました"),
            bgcolor="green"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def _on_wifi_updated(self, wifi: WiFiConfig):
        """Wi-Fi更新時"""
        self.storage_manager.update_wifi_config(wifi)
        self.load_wifi_configs()
    
    def _on_wifi_deleted(self, wifi: WiFiConfig):
        """Wi-Fi削除時"""
        def on_confirm(e):
            confirm_dialog.open = False
            self.page.update()
            
            self.storage_manager.delete_wifi_config(wifi.id)
            self.load_wifi_configs()
            
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"「{wifi.ssid}」を削除しました"),
                bgcolor="orange"
            )
            self.page.snack_bar.open = True
            self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("削除確認"),
            content=ft.Text(f"「{wifi.ssid}」を削除しますか？"),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda e: setattr(confirm_dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton("削除", on_click=on_confirm, bgcolor="red"),
            ],
        )
        
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()
    
    def _on_wifi_connect(self, wifi: WiFiConfig):
        """Wi-Fi接続試行"""
        self.status_text.value = "接続中..."
        self.status_text.color = "orange"
        self.page.update()
        
        success = self.wifi_manager.connect_to_network(wifi.ssid, wifi.password)
        
        if success:
            self.status_text.value = "接続成功"
            self.status_text.color = "green"
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"「{wifi.ssid}」に接続しました"),
                bgcolor="green"
            )
            self.update_current_network()
        else:
            self.status_text.value = "接続失敗"
            self.status_text.color = "red"
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"「{wifi.ssid}」への接続に失敗しました"),
                bgcolor="red"
            )
        
        self.page.snack_bar.open = True
        self.page.update()
