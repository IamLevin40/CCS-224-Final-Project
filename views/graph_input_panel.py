import flet as ft
import re
import random

from utils.string_manipulation import to_digit_subscript
from utils.line_data_io import save_lines_web, load_lines_code

class GraphInputPanel(ft.Container):
    COLORS = ["#EC2525", "#EC6725", "#ECDF25", "#25EC28", "#257FEC", "#A925EC"]

    def __init__(self):
        super().__init__(padding=10, alignment=ft.alignment.top_center, expand=True)
        self.border_color = "#F2F2F2"
        self.label_color = "#ACAFB8"

        self.lines = []
        self.line_column = ft.Column(scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, expand=True)
        self.add_line_button = ft.ElevatedButton("Add Line", on_click=lambda e: self.add_line(), style=ft.ButtonStyle(bgcolor={"": "#2196F3"}, color={"": "#FFFFFF"}))
        self.save_button = ft.ElevatedButton("Save", icon=ft.icons.SAVE, icon_color="white", on_click=lambda e: save_lines_web(self.lines), style=ft.ButtonStyle(bgcolor={"": "#18A045"}, color={"": "#FFFFFF"}))

        self.code_field = ft.TextField(label="Code here", multiline=True, expand=True, min_lines=1, max_lines=1, border_color=self.border_color, label_style=ft.TextStyle(color=self.label_color))
        self.generate_button = ft.ElevatedButton("Code", icon=ft.icons.BOLT, icon_color="white", on_click=lambda e: load_lines_code(self), style=ft.ButtonStyle(bgcolor={"": "#A01823"}, color={"": "#FFFFFF"}))

        self.color_picker_popup = ft.Container(visible=False, bgcolor="white", border_radius=10, padding=10, shadow=ft.BoxShadow(blur_radius=10, color="black12"),
            content=ft.Column([], scroll=ft.ScrollMode.AUTO), width=220, height=235, alignment=ft.alignment.center)

        self.main_content = ft.Column(
            [
                ft.Text("Enter Lines with Data Points", size=18, weight=ft.FontWeight.BOLD),
                self.line_column,
                ft.Container(content=ft.Row([self.add_line_button, self.save_button], spacing=10), alignment=ft.alignment.center_left),
                ft.Row([self.code_field, self.generate_button], alignment=ft.MainAxisAlignment.START)
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )
        
        self.content = ft.Stack([
            self.main_content,
            self.color_picker_popup
        ])

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

    def create_data_row(self, line_index, point_index, on_delete):
        x_input = ft.TextField(width=80, keyboard_type=ft.KeyboardType.NUMBER, on_change=self.validate_float_input,
            border_color=self.border_color, label=f"x{to_digit_subscript(point_index + 1)}",
            label_style=ft.TextStyle(color=self.label_color))
        y_input = ft.TextField(width=80, keyboard_type=ft.KeyboardType.NUMBER, on_change=self.validate_float_input,
            border_color=self.border_color, label=f"y{to_digit_subscript(point_index + 1)}",
            label_style=ft.TextStyle(color=self.label_color))

        controls = [x_input, y_input]

        if point_index > 0:
            delete_btn = ft.IconButton(icon=ft.icons.REMOVE, icon_color="red", tooltip="Delete Row", on_click=on_delete)
            controls.append(delete_btn)

        row = ft.Row(controls, alignment="start")
        return (row, x_input, y_input)

    def add_line(self, label=None, color=None, points=None):
        line_index = len(self.lines)
        color = color or random.choice(self.COLORS)

        color_button = ft.Button(width=30, height=30, bgcolor=color, text=" ", tooltip="Select Color")
        color_button.on_click = lambda e, idx=line_index, btn=color_button: self.show_color_picker(
            btn, idx, top_offset=30, left_offset=70)

        label_input = ft.TextField(
            width=150, value=label or "", border_color=self.border_color,
            label=f"Line {line_index + 1}", label_style=ft.TextStyle(color=self.label_color)
        )
        add_row_button = ft.IconButton(icon=ft.icons.ADD, icon_color="blue", tooltip="Add Row",
            on_click=lambda e, idx=line_index: self.add_data_row(idx))
        delete_line_button = ft.IconButton(icon=ft.icons.DELETE, icon_color="red", tooltip="Delete Line",
            on_click=lambda e, idx=line_index: self.delete_line(idx))

        header = ft.Row([label_input, color_button, add_row_button] + ([delete_line_button] if line_index > 0 else []),
            alignment=ft.MainAxisAlignment.START)

        data_rows = []
        row_column = ft.Column()

        def add_row_fn():
            idx = len(data_rows)
            row_data = self.create_data_row(line_index, idx, on_delete=lambda e, i=idx: self.delete_data_row(line_index, i))
            data_rows.append(row_data)
            row_column.controls.append(row_data[0])
            self.lines[line_index] = self.lines[line_index][:3] + (data_rows, row_column) + self.lines[line_index][5:]
            self.update()

        def delete_row_fn(i):
            if 0 <= i < len(data_rows):
                del data_rows[i]
                del row_column.controls[i]
                self.relabel_data_rows(line_index, data_rows, row_column)
                self.update()

        self.lines.append((header, label_input, color, data_rows, row_column, add_row_fn, delete_row_fn, delete_line_button))
        container = ft.Column([header, row_column])
        self.line_column.controls.append(container)

        if points:
            for idx, (x, y) in enumerate(points):
                row_data = self.create_data_row(line_index, idx, on_delete=lambda e, i=idx: self.delete_data_row(line_index, i))
                row_data[1].value = str(x)
                row_data[2].value = str(y)
                data_rows.append(row_data)
                row_column.controls.append(row_data[0])
        else:
            add_row_fn()

        self.update()

    def add_data_row(self, line_index):
        if 0 <= line_index < len(self.lines):
            self.lines[line_index][5]()

    def delete_data_row(self, line_index, row_index):
        if 0 <= line_index < len(self.lines):
            self.lines[line_index][6](row_index)

    def delete_line(self, line_index):
        if len(self.lines) <= 1:
            return
        del self.lines[line_index]
        del self.line_column.controls[line_index]
        self.relabel_all_lines()
        self.update()

    def relabel_data_rows(self, line_index, data_rows, row_column):
        row_column.controls.clear()
        new_rows = []
        for i, (_, x_input, y_input) in enumerate(data_rows):
            row_data = self.create_data_row(line_index, i, on_delete=lambda e, idx=i: self.delete_data_row(line_index, idx))
            row_data[1].value = x_input.value
            row_data[2].value = y_input.value
            new_rows.append(row_data)
            row_column.controls.append(row_data[0])
        self.lines[line_index] = self.lines[line_index][:3] + (new_rows, row_column) + self.lines[line_index][5:]

    def relabel_all_lines(self):
        for idx, (header, label_input, color, data_rows, row_column, add_fn, del_fn, del_btn) in enumerate(self.lines):
            label_input.label = f"Line {idx + 1}"
            del_btn.on_click = lambda e, idx=idx: self.delete_line(idx)
            self.lines[idx] = (header, label_input, color, data_rows, row_column, add_fn, del_fn, del_btn)

    def get_all_lines_data(self):
        results = []
        for (_, label_input, color, data_rows, _, _, _, _) in self.lines:
            x_vals, y_vals = [], []
            for _, x_input, y_input in data_rows:
                try:
                    x = x_input.value.strip()
                    y = y_input.value.strip()
                    if x == "" or y == "":
                        continue
                    x = float(x)
                    y = float(y)
                    x_vals.append(x)
                    y_vals.append(y)
                except:
                    continue

            if len(x_vals) >= 2:
                results.append({"x_vals": x_vals, "y_vals": y_vals, "label": label_input.value.strip(), "color": color})
        return results

    def show_color_picker(self, color_button, line_index, top_offset=0, left_offset=0):
        def select_color(color):
            color_button.bgcolor = color
            self.lines[line_index] = self.lines[line_index][:2] + (color,) + self.lines[line_index][3:]
            self.color_picker_popup.visible = False
            self.update()

        def close_picker(e):
            self.color_picker_popup.visible = False
            self.update()

        spacing = 0
        box_size = 10
        box_radius = 0

        color_grid_rows = []
        for i in range(19):
            row = []
            for j in range(20):
                r = int(255 * (1 - j / 19))
                g = int(255 * (i / 18))
                b = int(255 * (j / 19))
                color = f"#{r:02x}{g:02x}{b:02x}"
                row.append(ft.Container(
                    width=box_size, height=box_size, bgcolor=color, border_radius=box_radius,
                    on_click=lambda e, c=color: select_color(c)
                ))
            color_grid_rows.append(ft.Row(row, spacing=spacing))

        grayscale_row = []
        for i in range(20):
            shade = int(255 * (1 - i / 19))
            gray = f"#{shade:02x}{shade:02x}{shade:02x}"
            grayscale_row.append(ft.Container(
                width=box_size, height=box_size, bgcolor=gray, border_radius=box_radius,
                on_click=lambda e, c=gray: select_color(c)
            ))

        header = ft.Row(
            controls=[
                ft.Text(f"Line {line_index + 1}", size=10, weight=ft.FontWeight.BOLD, color="black"),
                ft.Container(expand=True),
                ft.Button(text="-", tooltip="Close", on_click=close_picker, bgcolor="red", width=10, height=10)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        full_content = ft.Column(
            controls=[
                header,
                ft.Column(color_grid_rows, spacing=spacing),
                ft.Row(grayscale_row, spacing=spacing)
            ],
            spacing=spacing
        )

        self.color_picker_popup.left = left_offset
        self.color_picker_popup.top = top_offset
        self.color_picker_popup.content = full_content
        self.color_picker_popup.visible = True
        self.update()

    def build_with_button(self, on_calculate, page=None):
        def on_graph_lines_click(e):
            on_calculate(e)

        home_button = ft.IconButton(icon=ft.icons.HOME, icon_color="blue", tooltip="Back to Home", on_click=lambda e: page.go("/") if page else None)
        find_button = ft.ElevatedButton("Graph Lines", on_click=on_graph_lines_click)

        return ft.Column(
            [
                self,
                ft.Container(content=ft.Row([home_button, find_button], spacing=10))
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def did_mount(self):
        return self.add_line()
