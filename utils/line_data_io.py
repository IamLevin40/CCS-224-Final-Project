import base64
import json
import os
import re
import webbrowser
import flet as ft

def save_lines_web(lines):
    data = []
    for (_, label_input, color, data_rows, _, _, _, _) in lines:
        points = []
        for (_, x_input, y_input) in data_rows:
            if x_input.value and y_input.value:
                try:
                    x = float(x_input.value)
                    y = float(y_input.value)
                    points.append({"x": x, "y": y})
                except ValueError:
                    continue
        data.append({"label": label_input.value, "color": color, "points": points})

    json_str = json.dumps(data)
    encoded_text = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    text_name = "line_data.txt"

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <body>
        <a id="downloadLink" 
        href="data:text/plain;base64,{encoded_text}" 
        download="{text_name}" 
        style="display:none;">
        Download File
        </a>
        <script>
        document.getElementById('downloadLink').click();
        // Wait a short moment then attempt to close the window
        setTimeout(() => {{
            window.open('', '_self');
            window.close();
        }}, 250);
        </script>
    </body>
    </html>
    '''

    filename = "download_trigger.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    webbrowser.open(f"file://{os.path.abspath(filename)}")

def load_lines_code(panel):
    try:
        code = panel.code_field.value
        data = json.loads(code)

        if not isinstance(data, list):
            raise ValueError("Invalid format: root JSON element must be a list.")

        panel.lines.clear()
        panel.line_column.controls.clear()

        hex_color_pattern = re.compile(r"^#(?:[0-9a-fA-F]{6})$")

        for i, line_data in enumerate(data):
            if not isinstance(line_data, dict):
                raise ValueError(f"Line {i + 1} must be a JSON object.")

            allowed_keys = {"label", "color", "points"}
            extra_keys = set(line_data.keys()) - allowed_keys
            if extra_keys:
                raise ValueError(f"Line {i + 1} contains unexpected keys: {', '.join(extra_keys)}")

            label = line_data.get("label", f"Line {i + 1}")
            if not isinstance(label, str):
                raise ValueError(f"Invalid type for 'label' in line {i + 1}: must be a string.")

            color = line_data.get("color", "#0000FF")
            if not isinstance(color, str) or not hex_color_pattern.fullmatch(color):
                raise ValueError(f"Invalid color format in line {i + 1}: '{color}' must be a hex string like '#RRGGBB'.")

            # Validate points
            points = line_data.get("points")
            if not isinstance(points, list):
                raise ValueError(f"'points' in line {i + 1} must be a list.")

            valid_points = []
            for j, point in enumerate(points):
                if not isinstance(point, dict):
                    raise ValueError(f"Point {j + 1} in line {i + 1} must be a dictionary.")

                if "x" not in point or "y" not in point:
                    raise ValueError(f"Point {j + 1} in line {i + 1} must contain 'x' and 'y' keys.")

                x, y = point.get("x"), point.get("y")
                if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                    raise ValueError(f"Invalid coordinate types in point {j + 1} of line {i + 1}: 'x' and 'y' must be numbers.")

                extra_point_keys = set(point.keys()) - {"x", "y"}
                if extra_point_keys:
                    raise ValueError(f"Point {j + 1} in line {i + 1} has unexpected keys: {', '.join(extra_point_keys)}")

                valid_points.append((x, y))

            print(f"Loaded line {i + 1}: {label}, color: {color}, points: {valid_points}")
            panel.add_line(label=label, color=color, points=valid_points)

        panel.update()

    except Exception as ex:
        error_message = f"Error loading code: {ex}"
        panel.page.open(ft.SnackBar(content=ft.Text(error_message), bgcolor=ft.colors.ERROR))
        print(error_message)