import flet as ft
from models.wifi_config import WiFiConfig
from services.wifi_manager import WiFiManager


class AddWiFiDialog(ft.AlertDialog):
    """Wi-Fi追加ダイアログ"""
    
    def __init__(self, wifi_manager: WiFiManager, on_save, current_priority: int):
        """
        Args:
            wifi_manager: Wi-Fiマネージャー
            on_save: 保存時のコールバック関数
            current_priority: 次の優先順位番号
        """
        self.wifi_manager = wifi_manager
        self.on_save_callback = on_save
        self.current_priority = current_priority
        
        # 入力方法選択
        self.input_method_tabs = ft.Tabs(
            selected_index=0,
            on_change=self._on_tab_changed,
            tabs=[
                ft.Tab(text="スキャンから選択", icon="wifi_find"),
                ft.Tab(text="手動入力", icon="edit"),
            ],
        )
        
        # スキャン結果リスト
        self.scan_list = ft.ListView(
            expand=True,
            spacing=5,
            height=250,
        )
        
        # 手動入力フィールド
        self.manual_ssid_field = ft.TextField(
            label="SSID",
            hint_text="ネットワーク名を入力",
        )
        
        self.manual_password_field = ft.TextField(
            label="パスワード",
            password=True,
            can_reveal_password=True,
        )
        
        # 選択されたSSID
        self.selected_ssid = None
        self.selected_password = ""
        
        # コンテンツエリア
        self.scan_content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("利用可能なネットワーク", size=16),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon="refresh",
                        tooltip="再スキャン",
                        on_click=self._on_refresh_scan
                    ),
                ]),
                self.scan_list,
            ], spacing=10),
            visible=True,
        )
        
        self.manual_content = ft.Container(
            content=ft.Column([
                self.manual_ssid_field,
                ft.Container(height=10),
                self.manual_password_field,
            ], spacing=5),
            visible=False,
        )
        
        self.next_button = ft.ElevatedButton(
            "次へ (パスワード入力)",
            on_click=self._on_next,
            icon="arrow_forward",
            disabled=True,
        )
        
        super().__init__(
            modal=True,
            title=ft.Text("Wi-Fi設定を追加", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    self.input_method_tabs,
                    ft.Container(height=10),
                    self.scan_content,
                    self.manual_content,
                ], spacing=5, tight=True),
                width=500,
                height=400,
                padding=10
            ),
            actions=[
                ft.TextButton("キャンセル", on_click=self._on_cancel),
                self.next_button,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        
        # 初回スキャンはdid_mountで行う（UIフリーズ回避のため）
        # self._load_scan_results() 
        print("AddWiFiDialog initialized")

    def did_mount(self):
        """ダイアログが表示された後に実行"""
        print("AddWiFiDialog did_mount")
        self._load_scan_results()
    
    def _on_tab_changed(self, e):
        """タブ切り替え時"""
        if e.control.selected_index == 0:
            self.scan_content.visible = True
            self.manual_content.visible = False
        else:
            self.scan_content.visible = False
            self.manual_content.visible = True
        
        if self.page:
            self.page.update()
    
    def _load_scan_results(self):
        """スキャン結果を読み込み"""
        networks = self.wifi_manager.scan_networks()
        self.scan_list.controls.clear()
        
        if not networks:
            self.scan_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "ネットワークが見つかりませんでした",
                        color="grey",
                        italic=True
                    ),
                    padding=20,
                    alignment=ft.alignment.center
                )
            )
        else:
            for ssid in networks:
                self.scan_list.controls.append(
                    ft.ListTile(
                        leading=ft.Icon("wifi"),
                        title=ft.Text(ssid),
                        on_click=lambda e, s=ssid: self._on_network_selected(s),
                        hover_color="blue,0.1",
                    )
                )
        
        if self.page:
            self.page.update()
    
    def _on_refresh_scan(self, e):
        """再スキャンボタン"""
        self._load_scan_results()
    
    def _on_network_selected(self, ssid: str):
        """ネットワーク選択時"""
        self.selected_ssid = ssid
        
        # 選択状態をハイライト
        for control in self.scan_list.controls:
            if isinstance(control, ft.ListTile):
                if control.title.value == ssid:
                    control.bgcolor = "blue900"
                else:
                    control.bgcolor = None
        
        # 次へボタンを有効化
        self.next_button.disabled = False
        
        if self.page:
            self.page.update()
    
    def _on_cancel(self, e):
        """キャンセルボタン"""
        self.open = False
        if self.page:
            self.page.update()
    
    def _on_next(self, e):
        """次へボタン - パスワード入力ダイアログを表示"""
        if self.input_method_tabs.selected_index == 0:
            if self.selected_ssid:
                self._show_password_dialog(self.selected_ssid)
        else:
            ssid = self.manual_ssid_field.value.strip()
            password = self.manual_password_field.value
            
            if not ssid:
                return
            
            self._save_wifi_config(ssid, password)
    
    def _show_password_dialog(self, ssid: str):
        """パスワード入力ダイアログを表示"""
        password_field = ft.TextField(
            label="パスワード",
            password=True,
            can_reveal_password=True,
            autofocus=True,
        )
        
        def on_password_save(e):
            password = password_field.value
            password_dialog.open = False
            if self.page:
                self.page.update()
            
            self._save_wifi_config(ssid, password)
        
        password_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{ssid} のパスワード"),
            content=ft.Container(
                content=password_field,
                width=400,
                padding=20
            ),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda e: setattr(password_dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton("保存", on_click=on_password_save),
            ],
        )
        
        if self.page:
            self.page.dialog = password_dialog
            password_dialog.open = True
            self.page.update()
    
    def _save_wifi_config(self, ssid: str, password: str):
        """Wi-Fi設定を保存"""
        wifi = WiFiConfig(
            ssid=ssid,
            password=password,
            priority=self.current_priority
        )
        
        self._show_connection_test_dialog(wifi)
    
    def _show_connection_test_dialog(self, wifi: WiFiConfig):
        """接続テストダイアログを表示"""
        def on_test_now(e):
            test_dialog.open = False
            self.open = False
            if self.page:
                self.page.update()
            
            if self.on_save_callback:
                self.on_save_callback(wifi, test_connection=True)
        
        def on_save_only(e):
            test_dialog.open = False
            self.open = False
            if self.page:
                self.page.update()
            
            if self.on_save_callback:
                self.on_save_callback(wifi, test_connection=False)
        
        test_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("設定を保存しました"),
            content=ft.Text(
                f"「{wifi.ssid}」の設定が保存されました。\n今すぐ接続を試しますか？",
                size=16
            ),
            actions=[
                ft.TextButton("いいえ", on_click=on_save_only),
                ft.ElevatedButton(
                    "はい",
                    on_click=on_test_now,
                    icon="wifi"
                ),
            ],
        )
        
        if self.page:
            self.page.dialog = test_dialog
            test_dialog.open = True
            self.page.update()
