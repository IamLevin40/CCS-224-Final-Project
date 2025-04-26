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

        self.add_row_button = ft.ElevatedButton(
            "Add Row",
            on_click=lambda e: self.add_row(),
            style=ft.ButtonStyle(
                bgcolor={"": "#2196F3"},
                color={"": "#FFFFFF"}
            )
        )

        self.clear_all_button = ft.ElevatedButton(
            "Clear All Rows",
            on_click=lambda e: self.clear_all_rows(),
            style=ft.ButtonStyle(
                bgcolor={"": "#F44336"},
                color={"": "#FFFFFF"}
            )
        )

        self.row_buttons = ft.Row(
            [self.add_row_button, self.clear_all_button],
            spacing=10,
            alignment=ft.MainAxisAlignment.START
        )

        self.content = ft.Column(
            [
                ft.Text("Enter Data Points", size=18, weight=ft.FontWeight.BOLD),
                self.table,
                ft.Container(
                    content=self.row_buttons,
                    alignment=ft.alignment.center_left
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

        self.random_input = ft.TextField(
            width=120,
            label="Number of Random Points (1-10)",
            label_style=ft.TextStyle(color=self.label_color, size=10),
            border_color=self.border_color,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.validate_random_input
        )
        self.random_button = ft.ElevatedButton("Random", on_click=self.add_random_points)

        self.random_controls = ft.Row([self.random_input, self.random_button])

    def did_mount(self):
        return self.add_row()

    def validate_float_input(self, e):
        text_field = e.control
        value = text_field.value.strip()
        if not value:
            return
        
        pattern = r'^-?\d*\.?\d*$'
        if not re.match(pattern, value):
            cleaned = ''.join(c for c in value if c.isdigit() or c in '.-')
            parts = cleaned.split('.')
            if len(parts) > 1:
                cleaned = f"{parts[0]}.{''.join(parts[1:])}"
            text_field.value = cleaned
        
        text_field.update()
        self.check_and_add_or_remove_rows()

    def create_row(self, index):
        x_input = ft.TextField(
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.validate_float_input,
            label=f"x{to_subscript(index + 1)}",
            label_style=ft.TextStyle(color=self.label_color),
            border_color=self.border_color
        )
        y_input = ft.TextField(
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.validate_float_input,
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

    def clear_all_rows(self):
        self.rows.clear()
        self.table.controls.clear()
        self.add_row()  # Add one empty row
        self.update()

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

    def validate_random_input(self, e):
        tf = e.control
        value = tf.value.strip()

        if not value.isdigit():
            tf.value = ""
        else:
            number = int(value)
            if number < 1:
                tf.value = "1"
            elif number > 10:
                tf.value = "10"

        tf.update()

    def add_random_points(self, e):
        try:
            num_points = int(self.random_input.value.strip())
            if num_points <= 0:
                raise ValueError("The number must be a positive integer.")
        except ValueError as ex:
            self.random_input.error_text = str(ex)
            self.update()
            return

        existing_x_values = set(
            int(row[1].value.strip()) for row in self.rows if row[1].value.strip()
        )

        reference_x_values = list(existing_x_values)
        random.shuffle(reference_x_values)
        used_references = set()

        last_x, last_y = 0, 0
        for row in reversed(self.rows):
            try:
                last_x = int(row[1].value.strip())
                last_y = int(row[2].value.strip())
                break
            except (ValueError, AttributeError):
                continue

        added = 0
        while added < num_points and len(used_references) < len(reference_x_values) + 1:
            attempts = 0
            found_unique = False

            while attempts < 10:
                attempts += 1
                new_x = last_x + random.randint(-5, 5)
                new_x = max(min(new_x, 100), -100)

                if new_x not in existing_x_values:
                    new_y = last_y + random.randint(-5, 5)
                    new_y = max(min(new_y, 100), -100)

                    self.add_row_with_values(new_x, new_y)
                    existing_x_values.add(new_x)
                    last_x, last_y = new_x, new_y
                    added += 1
                    found_unique = True
                    break

            if not found_unique:
                used_references.add(last_x)
                remaining_references = [x for x in reference_x_values if x not in used_references]

                if remaining_references:
                    last_x = random.choice(remaining_references)
                    for row in self.rows:
                        try:
                            x_val = int(row[1].value.strip())
                            y_val = int(row[2].value.strip())
                            if x_val == last_x:
                                last_y = y_val
                                break
                        except ValueError:
                            continue
                else:
                    break

        self.update()

    def add_row_with_values(self, x_val, y_val):
        index = len(self.rows)
        row_data = self.create_row(index)
        row_data[1].value = str(x_val)
        row_data[2].value = str(y_val)
        self.rows.append(row_data)
        self.table.controls.append(row_data[0])

    def clean_empty_rows(self):
        i = len(self.rows) - 1
        while i >= 0:
            x_val = self.rows[i][1].value.strip()
            y_val = self.rows[i][2].value.strip()
            
            if not x_val or not y_val:
                self.delete_row(i)
            i -= 1
        
        if not self.rows:
            self.add_row()

    def build_with_button(self, on_calculate):
        def on_find_button_click(e):
            self.clean_empty_rows()
            on_calculate(e)
        
        find_button = ft.ElevatedButton(
            "Find Polynomial", 
            on_click=on_find_button_click
        )

        return ft.Column(
            [
                self,
                ft.Container(content=self.random_controls, padding=10),
                ft.Container(content=find_button, padding=10)
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )