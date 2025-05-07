import flet as ft
from views.compare_input_panel import CompareInputPanel
from views.compare_output_panel import CompareOutputPanel
from utils.validation import validate_data

def build_compare_page(page: ft.Page):
    input_panel = CompareInputPanel()
    output_panel = CompareOutputPanel()

    def on_calculate(e):
        x_vals, y_vals = input_panel.get_data()
        is_valid, error_message = validate_data(x_vals, y_vals)
        if not is_valid:
            page.open(ft.SnackBar(content=ft.Text(error_message), bgcolor=ft.colors.ERROR))
            return

        try:
            output_panel.update_output(x_vals, y_vals)
        except Exception as ex:
            page.open(ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"), bgcolor=ft.colors.ERROR))
            print(f"Error: {str(ex)}")

    input_container = ft.Container(
        content=input_panel.build_with_button(on_calculate, page=page),
        expand=1,
        padding=10
    )

    output_container = ft.Container(
        content=output_panel,
        expand=4,
        padding=10
    )

    return ft.Row(
        controls=[
            input_container,
            ft.VerticalDivider(width=5, thickness=1),
            output_container
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START
    )
