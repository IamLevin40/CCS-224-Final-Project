import base64
import json
import os
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
        data.append({
            "label": label_input.value,
            "color": color,
            "points": points
        })

    json_str = json.dumps(data, indent=2)
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

def load_lines_web(panel, e):
    try:
        if not e.files:
            return

        file = e.files[0]
        content = file.read().decode("utf-8")
        data = json.loads(content)

        if not isinstance(data, list):
            raise ValueError("Invalid data format: root must be a list.")

        panel.lines.clear()
        panel.line_column.controls.clear()
        print(f"Loaded {len(data)} lines from file.")
        print(f"Data: {data}")

        for i, line_data in enumerate(data):
            label = line_data.get("label", f"Line {i + 1}")
            color = line_data.get("color", "#0000FF")

            points = line_data.get("points", [])
            if not isinstance(points, list):
                raise ValueError(f"Invalid points format in line {i + 1}")

            valid_points = []
            for point in points:
                if (
                    isinstance(point, dict) and
                    "x" in point and "y" in point and
                    isinstance(point["x"], (int, float)) and
                    isinstance(point["y"], (int, float))
                ):
                    valid_points.append({"x": point["x"], "y": point["y"]})
                else:
                    raise ValueError(f"Invalid point in line {i + 1}: {point}")

            print(f"Loaded line {i + 1}: {label}, color: {color}, points: {valid_points}")
            panel.add_line(label=label, color=color, points=valid_points)

        panel.update()

    except Exception as ex:
        panel.page.open(ft.SnackBar(content=ft.Text(f"Error loading file: {ex}"), bgcolor=ft.colors.ERROR))
