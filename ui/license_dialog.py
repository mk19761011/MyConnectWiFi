import flet as ft
from services.license_manager import LicenseManager


class LicenseDialog(ft.AlertDialog):
    """ライセンス認証ダイアログ"""
    
    def __init__(self, license_manager: LicenseManager, on_success):
        """
        Args:
            license_manager: ライセンスマネージャー
            on_success: 認証成功時のコールバック関数
        """
        self.license_manager = license_manager
        self.on_success_callback = on_success
        
        # テキスト入力フィールド
        self.license_key_field = ft.TextField(
            label="ライセンスキー",
            hint_text="TEST-KEY-001",
            autofocus=True,
            width=400,
        )
        
        # メッセージ表示
        self.message_text = ft.Text(
            "",
            size=14,
            color="grey",
            visible=False
        )
        
        # 処理中インジケーター
        self.progress_ring = ft.ProgressRing(
            visible=False,
            width=30,
            height=30
        )
        
        super().__init__(
            modal=True,
            title=ft.Text("ライセンス認証", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "5つ目以降のWi-Fi設定を登録するには、ライセンスキーが必要です。",
                        size=14,
                        color="grey"
                    ),
                    ft.Container(height=10),
                    self.license_key_field,
                    ft.Container(height=10),
                    ft.Row([
                        self.progress_ring,
                        self.message_text,
                    ]),
                    ft.Container(height=10),
                    ft.Text(
                        "💡 テスト用キー: TEST-KEY-001",
                        size=12,
                        color="blue",
                        italic=True
                    ),
                ], spacing=5, tight=True),
                width=450,
                padding=10
            ),
            actions=[
                ft.TextButton("キャンセル", on_click=self._on_cancel),
                ft.ElevatedButton(
                    "認証",
                    on_click=self._on_verify,
                    icon="verified_user"
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def _on_cancel(self, e):
        """キャンセルボタン"""
        self.open = False
        if self.page:
            self.page.update()
    
    async def _on_verify(self, e):
        """認証ボタン"""
        license_key = self.license_key_field.value.strip()
        
        if not license_key:
            self._show_message("ライセンスキーを入力してください", "red")
            return
        
        # 処理中表示
        self.progress_ring.visible = True
        self.message_text.visible = False
        if self.page:
            self.page.update()
        
        # ライセンス検証
        success, message, remaining = await self.license_manager.verify_license(license_key)
        
        # 結果表示
        self.progress_ring.visible = False
        color = "green" if success else "red"
        self._show_message(message, color)
        
        if success:
            # 2秒後にダイアログを閉じて成功コールバックを呼ぶ
            await self._delayed_close_and_callback(license_key)
    
    async def _delayed_close_and_callback(self, license_key: str):
        """遅延してダイアログを閉じ、成功コールバックを呼ぶ"""
        import asyncio
        await asyncio.sleep(2)
        
        self.open = False
        if self.page:
            self.page.update()
        
        if self.on_success_callback:
            self.on_success_callback(license_key)
    
    def _show_message(self, message: str, color: str):
        """メッセージを表示"""
        self.message_text.value = message
        self.message_text.color = color
        self.message_text.visible = True
        if self.page:
            self.page.update()
