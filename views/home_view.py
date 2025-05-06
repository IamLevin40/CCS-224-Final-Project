import flet as ft
from views.input_panel import InputPanel
from views.output_panel import OutputPanel
from utils.validation import validate_data

class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.input_panel = InputPanel()
        self.output_panel = OutputPanel()

        self.input_container = ft.Container(
            content=self.input_panel.build_with_button(self.on_calculate),
            width=self.page.window.width * 0.2
        )
        self.output_container = ft.Container(
            content=self.output_panel,
            width=self.page.window.width * 0.8
        )

        self.layout = ft.Row(
            [
                self.input_container,
                ft.VerticalDivider(width=10, color="#FFFFFF", thickness=2),
                self.output_container
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

    def on_calculate(self, e):
        x_vals, y_vals = self.input_panel.get_data()
        is_valid, error_message = validate_data(x_vals, y_vals)

        if not is_valid:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(error_message), bgcolor=ft.colors.ERROR))
            return

        try:
            self.output_panel.update_output(x_vals, y_vals)
        except Exception as ex:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"), bgcolor=ft.colors.ERROR))

    def on_resize(self, e):
        self.input_container.width = self.page.window.width * 0.2
        self.output_container.width = self.page.window.width * 0.8
        self.page.update()
