import flet as ft
import re
import random

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
        self.border_color = "#F2F2F2"
        self.label_color = "#ACAFB8"

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

        self.random_input = ft.TextField(
            width=120,
            label="Number of Random Points",
            label_style=ft.TextStyle(color=self.label_color, size=10),
            border_color=self.border_color,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        self.random_button = ft.ElevatedButton("Random", on_click=self.add_random_points)

        self.random_controls = ft.Row([self.random_input, self.random_button])

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

        x_input = ft.TextField(
            width=100,
            on_change=input_changed,
            label=f"x{to_subscript(index + 1)}",
            label_style=ft.TextStyle(color=self.label_color),
            border_color=self.border_color
        )
        y_input = ft.TextField(
            width=100,
            on_change=input_changed,
            label=f"y{to_subscript(index + 1)}",
            label_style=ft.TextStyle(color=self.label_color),
            border_color=self.border_color
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

    def add_random_points(self, e):
        try:
            num_points = int(self.random_input.value.strip())
            if num_points <= 0:
                raise ValueError("The number must be a positive integer.")
        except ValueError as ex:
            self.random_input.error_text = str(ex)
            self.update()
            return

        if not self.rows:
            last_x = 0
            last_y = 0
        else:
            last_x, last_y = None, None
            for row in reversed(self.rows):
                x_val = row[1].value.strip()
                y_val = row[2].value.strip()
                if x_val and y_val:
                    try:
                        last_x = int(x_val)
                        last_y = int(y_val)
                        break
                    except ValueError:
                        continue

            if last_x is None or last_y is None:
                last_x, last_y = 0, 0

        existing_x_values = [int(row[1].value.strip()) for row in self.rows if row[1].value.strip()]
        
        for _ in range(num_points):
            x_value, y_value = None, None
            
            attempts = 0
            while x_value is None or y_value is None:
                if attempts > 20:
                    random_row = random.choice(self.rows)
                    x_value = int(random_row[1].value.strip())
                    y_value = int(random_row[2].value.strip())
                    break

                new_x_value = last_x + random.randint(-5, 5)
                new_x_value = max(min(new_x_value, 100), -100)

                if new_x_value not in existing_x_values:
                    x_value = new_x_value
                    new_y_value = last_y + random.randint(-5, 5)
                    new_y_value = max(min(new_y_value, 100), -100)

                    y_value = new_y_value
                else:
                    attempts += 1

            self.add_row_with_values(x_value, y_value)
            existing_x_values.append(x_value)

            last_x = x_value
            last_y = y_value

        self.update()

    def add_row_with_values(self, x_val, y_val):
        index = len(self.rows)
        row_data = self.create_row(index)
        row_data[1].value = str(x_val)
        row_data[2].value = str(y_val)
        self.rows.append(row_data)
        self.table.controls.append(row_data[0])

    def build_with_button(self, on_find_polynomial_click):
        find_button = ft.ElevatedButton("Find Polynomial", on_click=on_find_polynomial_click)
        return ft.Column(
            [
                self,
                ft.Container(content=self.random_controls, padding=10),
                ft.Container(content=find_button, padding=10)
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )