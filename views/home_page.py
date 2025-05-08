import flet as ft

def HomePage(page: ft.Page):
    return ft.Column(
        [
            ft.Text("PlotNomial", size=40, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Text("A Polynomial Interpolation Calculator", size=20, text_align=ft.TextAlign.CENTER),
            ft.Container(height=30),
            ft.ElevatedButton("Compare Interpolations", icon=ft.icons.COMPARE_ARROWS, icon_color="#FFFFFF", on_click=lambda e: page.go("/compare"), width=250, height=50,
                              style=ft.ButtonStyle(bgcolor={"": "#2196F3"}, color={"": "#FFFFFF"}, text_style=ft.TextStyle(weight=ft.FontWeight.BOLD))),
            ft.ElevatedButton("Graph Calculator", icon=ft.icons.SHOW_CHART, icon_color="#FFFFFF", on_click=lambda e: page.go("/graph"), width=250, height=50,
                              style=ft.ButtonStyle(bgcolor={"": "#F44336"}, color={"": "#FFFFFF"}, text_style=ft.TextStyle(weight=ft.FontWeight.BOLD))),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
