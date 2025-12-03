import flet as ft


def main(page: ft.Page):
    """シンプルなテストアプリ"""
    page.title = "My Connect Wi-Fi"
    page.theme_mode = ft.ThemeMode.DARK
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon("wifi", size=80, color="blue"),
                ft.Text("My Connect Wi-Fi", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Wi-Fi管理アプリ", size=16, color="grey"),
                ft.ElevatedButton(
                    "開始",
                    icon="play_arrow",
                    on_click=lambda e: page.add(ft.Text("準備中...", color="green"))
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            padding=50,
            alignment=ft.alignment.center,
            expand=True
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
