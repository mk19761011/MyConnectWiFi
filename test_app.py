import flet as ft


def main(page: ft.Page):
    page.title = "Test App"
    
    # テスト用コンポーネント
    page.add(
        ft.Container(
            content=ft.Text("Hello World", size=20),
            bgcolor="blue",
            padding=20
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
