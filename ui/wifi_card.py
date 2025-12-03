import flet as ft
from models.wifi_config import WiFiConfig


class WiFiCard(ft.Container):
    """Wi-Fi設定カードコンポーネント"""
    
    def __init__(self, wifi: WiFiConfig, on_update, on_delete, on_connect):
        """
        Args:
            wifi: Wi-Fi設定オブジェクト
            on_update: 更新時のコールバック関数
            on_delete: 削除時のコールバック関数
            on_connect: 接続時のコールバック関数
        """
        self.wifi = wifi
        self.on_update_callback = on_update
        self.on_delete_callback = on_delete
        self.on_connect_callback = on_connect
        
        # トグルスイッチ
        self.ignore_today_switch = ft.Switch(
            label="今日だけ無視",
            value=wifi.status_flags.ignore_today,
            on_change=self._on_ignore_today_changed
        )
        
        self.ignore_permanently_switch = ft.Switch(
            label="次回まで無視",
            value=wifi.status_flags.ignore_until_manual_reset,
            on_change=self._on_ignore_permanently_changed
        )
        
        super().__init__(
            content=ft.Column([
                ft.Row([
                    ft.Icon(
                        "wifi",
                        size=32,
                        color="blue" if not wifi.is_ignored() else "grey"
                    ),
                    ft.Column([
                        ft.Text(
                            wifi.ssid,
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="white" if not wifi.is_ignored() else "grey"
                        ),
                        ft.Text(
                            f"優先順位: {wifi.priority}",
                            size=14,
                            color="grey" if not wifi.is_ignored() else "grey"
                        ),
                    ], spacing=2),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon="play_arrow",
                        icon_color="green",
                        tooltip="接続",
                        on_click=self._on_connect_clicked
                    ),
                    ft.IconButton(
                        icon="delete",
                        icon_color="red",
                        tooltip="削除",
                        on_click=self._on_delete_clicked
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(height=1, color="grey"),
                ft.Row([
                    self.ignore_today_switch,
                    ft.Container(width=20),
                    self.ignore_permanently_switch,
                ], spacing=10),
            ], spacing=10),
            padding=15,
            margin=ft.margin.only(bottom=10),
            border_radius=10,
            bgcolor="surfacevariant" if not wifi.is_ignored() else "grey900",
            border=ft.border.all(1, "outline" if not wifi.is_ignored() else "grey"),
        )
    
    def _on_ignore_today_changed(self, e):
        """今日だけ無視スイッチ変更時"""
        if e.control.value:
            self.wifi.set_ignore_today()
        else:
            self.wifi.status_flags.ignore_today = False
            self.wifi.status_flags.last_ignored_date = None
        
        self.on_update_callback(self.wifi)
    
    def _on_ignore_permanently_changed(self, e):
        """次回まで無視スイッチ変更時"""
        self.wifi.set_ignore_permanently(e.control.value)
        self.on_update_callback(self.wifi)
    
    def _on_delete_clicked(self, e):
        """削除ボタンクリック時"""
        self.on_delete_callback(self.wifi)
    
    def _on_connect_clicked(self, e):
        """接続ボタンクリック時"""
        self.on_connect_callback(self.wifi)
