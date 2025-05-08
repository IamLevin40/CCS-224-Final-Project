import flet as ft
from views.graph_input_panel import GraphInputPanel
from views.graph_output_panel import GraphOutputPanel
from utils.validation import graph_validate_data

def build_graph_page(page: ft.Page):
    input_panel = GraphInputPanel()
    output_panel = GraphOutputPanel()

    def on_calculate(e):
        all_lines_data = input_panel.get_all_lines_data()
        is_valid, error_message = graph_validate_data(all_lines_data)
        if not is_valid:
            page.open(ft.SnackBar(content=ft.Text(error_message), bgcolor=ft.colors.ERROR))
            return

        try:
            output_panel.update_output(all_lines_data)
        except Exception as ex:
            page.open(ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"), bgcolor=ft.colors.ERROR))
            print(f"Error: {str(ex)}")

    input_container = ft.Container(content=input_panel.build_with_button(on_calculate, page=page), expand=1, padding=10)
    output_container = ft.Container(content=output_panel, expand=3, padding=10)

    return ft.Row(
        controls=[
            input_container,
            ft.VerticalDivider(width=5, thickness=1),
            output_container
        ],
        vertical_alignment=ft.CrossAxisAlignment.START, expand=True
    )
