import flet as ft
from views.graph_input_panel import GraphInputPanel
from views.graph_output_panel import GraphOutputPanel
from utils.validation import validate_data

def build_graph_page(page: ft.Page):
    input_panel = GraphInputPanel()
    output_panel = GraphOutputPanel()

    def on_calculate(e):
        x_vals, y_vals = input_panel.get_data()
        is_valid, error_message = validate_data(x_vals, y_vals)
        if not is_valid:
            page.show_snack_bar(ft.SnackBar(content=ft.Text(error_message), bgcolor=ft.colors.ERROR))
            return

        try:
            output_panel.update_output(x_vals, y_vals)
        except Exception as ex:
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"), bgcolor=ft.colors.ERROR))

    input_container = ft.Container(content=input_panel.build_with_button(on_calculate, page=page), width=page.window.width * 0.2)
    output_container = ft.Container(content=output_panel, width=page.window.width * 0.8)

    def on_resize(e):
        input_container.width = page.window.width * 0.2
        output_container.width = page.window.width * 0.8
        page.update()

    page.on_resized = on_resize

    return ft.Row(
        controls=[
            input_container,
            ft.VerticalDivider(width=10, color="#FFFFFF", thickness=2),
            output_container
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )
