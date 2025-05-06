import flet as ft

def HomePage(page: ft.Page):
    return ft.Column(
        [
            ft.Text("PlotNomial", size=40, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Text("A Polynomial Interpolation Calculator", size=20, text_align=ft.TextAlign.CENTER),
            ft.Container(height=30),
            ft.ElevatedButton("Compare Interpolations", on_click=lambda e: page.go("/compare"), width=250),
            ft.ElevatedButton("Graph Calculator", on_click=lambda e: page.go("/graph"), width=250),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
