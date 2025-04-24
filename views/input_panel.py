import flet as ft
import re

def to_subscript(n: int) -> str:
    subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(n).translate(subscript_digits)

class InputPanel(ft.Container):
    def __init__(self):
        super().__init__(
            padding=10,
            alignment=ft.alignment.top_center,
            expand=True
        )

        self.rows = []
        self.table = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

        self.content = ft.Column(
            [ft.Text("Enter Data Points", size=18, weight=ft.FontWeight.BOLD), self.table],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def did_mount(self):
        self.add_row()

    def is_valid_number(self, text):
        return re.fullmatch(r"-?\d*", text) is not None

    def create_row(self, index):
        def input_changed(e):
            if not self.is_valid_number(e.control.value):
                e.control.value = re.sub(r"[^\d-]", "", e.control.value)
                self.update()
            self.check_and_add_or_remove_rows()

        border_color = "#F2F2F2"
        label_color = "#ACAFB8"

        x_input = ft.TextField(
            width=100,
            on_change=input_changed,
            label=f"x{to_subscript(index + 1)}",
            label_style=ft.TextStyle(color=label_color),
            border_color=border_color
        )
        y_input = ft.TextField(
            width=100,
            on_change=input_changed,
            label=f"y{to_subscript(index + 1)}",
            label_style=ft.TextStyle(color=label_color),
            border_color=border_color
        )

        controls = [x_input, y_input]

        if index > 0:
            delete_btn = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color="red",
                tooltip="Delete Row",
                on_click=lambda e, idx=index: self.delete_row(idx)
            )
            controls.append(delete_btn)

        row = ft.Row(controls, alignment="start")
        return (row, x_input, y_input)

    def add_row(self):
        index = len(self.rows)
        row_data = self.create_row(index)
        self.rows.append(row_data)
        self.table.controls.append(row_data[0])
        self.update()

    def delete_row(self, index):
        if len(self.rows) > 1:
            del self.rows[index]
            del self.table.controls[index]
            self.relabel_rows()

    def relabel_rows(self):
        self.table.controls.clear()
        new_rows = []
        for i, (_, x_input, y_input) in enumerate(self.rows):
            new_row_data = self.create_row(i)
            new_row_data[1].value = x_input.value
            new_row_data[2].value = y_input.value
            new_rows.append(new_row_data)
            self.table.controls.append(new_row_data[0])
        self.rows = new_rows
        self.update()

    def check_and_add_or_remove_rows(self):
        for i in range(len(self.rows) - 2, 0, -1):
            x_val = self.rows[i][1].value.strip()
            y_val = self.rows[i][2].value.strip()
            if x_val == "" and y_val == "":
                self.delete_row(i)

        if self.rows:
            last_x = self.rows[-1][1].value.strip()
            last_y = self.rows[-1][2].value.strip()
            if last_x and last_y:
                self.add_row()

    def get_data(self):
        x_values = []
        y_values = []
        for _, x_input, y_input in self.rows:
            x_val = x_input.value.strip()
            y_val = y_input.value.strip()
            if x_val and y_val:
                try:
                    x_values.append(float(x_val))
                    y_values.append(float(y_val))
                except ValueError:
                    pass
        return x_values, y_values

    def build_with_button(self, on_find_polynomial_click):
        find_button = ft.ElevatedButton("Find Polynomial", on_click=on_find_polynomial_click)
        return ft.Column(
            [
                self,
                ft.Container(content=find_button, padding=10)
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )