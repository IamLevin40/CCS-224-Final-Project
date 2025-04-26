import flet as ft
from views.input_panel import InputPanel, to_subscript
from views.output_panel import OutputPanel

def main(page: ft.Page):
    page.title = "Polynomial Finder"
    page.window.maximized = True
    page.padding = 10

    def validate_data(x_vals, y_vals):
        if not x_vals or not y_vals:
            return False, "Please enter some data points."
            
        for i, x1 in enumerate(x_vals):
            for j, x2 in enumerate(x_vals):
                if i != j and x1 == x2:
                    return False, f"Duplicate value found: x₍{to_subscript(i+1)}₎ and x₍{to_subscript(j+1)}₎ = {x1}."
        
        return True, ""

    def on_calculate(e):
        x_vals, y_vals = input_panel.get_data()
        
        is_valid, error_message = validate_data(x_vals, y_vals)
        if not is_valid:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(error_message),
                    bgcolor=ft.colors.ERROR
                )
            )
            return
            
        try:
            output_panel.update_output(x_vals, y_vals)
        except Exception as ex:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Error: {str(ex)}"),
                    bgcolor=ft.colors.ERROR
                )
            )

    def page_resize(e):
        input_container.width = page.window.width * 0.2
        output_container.width = page.window.width * 0.8
        page.update()

    input_panel = InputPanel()
    output_panel = OutputPanel()

    input_container = ft.Container(
        content=input_panel.build_with_button(on_calculate),
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
