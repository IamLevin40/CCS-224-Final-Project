import flet as ft
from views.home_view import HomeView

def main(page: ft.Page):
    page.title = "PlotNomial"
    page.window.maximized = True
    page.padding = 10

    home_view = HomeView(page)
    page.on_resized = home_view.on_resize
    page.add(home_view.layout)

ft.app(target=main, view=ft.AppView.FLET_APP)
