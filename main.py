import flet as ft
from views.home_page import HomePage
from views.compare_page import build_compare_page
from views.graph_page import build_graph_page

from utils.server import run_server_in_background
run_server_in_background()

def main(page: ft.Page):
    page.title = "PlotNomial"
    page.window.maximized = True
    page.padding = 10

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(ft.View("/", [HomePage(page)]))
        elif page.route == "/compare":
            page.views.append(ft.View("/compare", [build_compare_page(page)]))
        elif page.route == "/graph":
            page.views.append(ft.View("/compare", [build_graph_page(page)]))
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
