import flet as ft

class OutputPanel(ft.Container):
    def __init__(self):
        super().__init__(
            padding=10,
            alignment=ft.alignment.top_left,
            expand=True
        )

        self.graph_columns = []
        for _ in range(3):
            graph_container = ft.Container(
                content=ft.Text("Graph Placeholder", size=16, color="gray"),
                bgcolor="#f0f0f0",
                alignment=ft.alignment.center,
                border_radius=10,
                padding=10,
                expand=True
            )
            info_container = ft.Container(
                content=ft.Text("Data points will appear here.", size=14),
                padding=10,
                bgcolor="#ffffff",
                border_radius=10,
                expand=True
            )

            column = ft.Column(
                [
                    ft.Container(
                        content=graph_container,
                        expand=7
                    ),
                    ft.Container(
                        content=info_container,
                        expand=3
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                expand=True,
                spacing=10  # Add spacing between containers
            )

            self.graph_columns.append(column)

        self.output_row = ft.Row(
            [
                ft.Container(
                    content=column,
                    expand=True,
                    margin=ft.margin.only(right=10)  # Add spacing between columns
                ) for column in self.graph_columns
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True
        )

        self.content = ft.Column(
            [
                ft.Text("Graphs and Information", size=18, weight=ft.FontWeight.BOLD),
                self.output_row
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def update_output(self, x_vals, y_vals):
        coord_list = "\n".join([f"({x}, {y})" for x, y in zip(x_vals, y_vals)]) if x_vals and y_vals else "No valid data points entered."

        for column in self.graph_columns:
            info_container = column.controls[1].content
            info_container.value = "Data Points:\n" + coord_list

        self.update()