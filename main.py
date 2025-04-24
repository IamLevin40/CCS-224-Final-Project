import flet as ft
from views.input_panel import InputPanel
from views.output_panel import OutputPanel

def main(page: ft.Page):
    page.title = "Polynomial Finder"
    page.window.maximized = True
    page.padding = 10

    def on_find_polynomial_click(e):
        x_vals, y_vals = input_panel.get_data()
        output_panel.update_output(x_vals, y_vals)
    
    def page_resize(e):
        input_container.width = page.window.width * 0.2
        output_container.width = page.window.width * 0.8
        page.update()

    input_panel = InputPanel()
    output_panel = OutputPanel()

    input_container = ft.Container(
        content=input_panel.build_with_button(on_find_polynomial_click),
        width=page.window.width * 0.2
    )
    output_container = ft.Container(
        content=output_panel,
        width=page.window.width * 0.8
    )

    layout = ft.Row(
        [
            input_container,
            ft.VerticalDivider(
                width=10,
                color="#FFFFFF",
                thickness=2
            ),
            output_container
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    page.on_resized = page_resize
    page.add(layout)

ft.app(
    target=main,
    view=ft.AppView.FLET_APP
)
