import flet as ft
import os

from utils.server import SERVE_DIR
from algorithms.barycentric import BarycentricInterpolator
from utils.dynamic_cartesian_plot import generate_multi_interpolation_plot

class GraphOutputPanel(ft.Container):
    def __init__(self):
        super().__init__(padding=10, alignment=ft.alignment.top_left, expand=True)

        self.graph_display = ft.Text("Insert data points\nto create graph.", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.graph_container = ft.Container(content=self.graph_display, bgcolor="#ffffff", alignment=ft.alignment.center, border_radius=10, padding=10, expand=True)

        self.content = ft.Column(
            [
                ft.Text("Graph", size=18, weight=ft.FontWeight.BOLD),
                self.graph_container
            ],
            alignment=ft.MainAxisAlignment.START, expand=True
        )

    def update_output(self, datasets):
        """
        datasets: List of dicts with keys:
            - x_vals
            - y_vals
            - label (optional)
            - color (optional)
        """
        self.graph_container.content = ft.Text("Computing...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.update()

        html_url = self.compute_interpolations(datasets)
        self.update_graph_ui(html_url)

    def compute_interpolations(self, datasets):
        interpolated_data = []

        for i, data in enumerate(datasets):
            x_vals = data.get("x_vals", [])
            y_vals = data.get("y_vals", [])

            if not x_vals or not y_vals or len(x_vals) <= 1:
                continue

            interpolator = BarycentricInterpolator(x_vals, y_vals)
            interpolated_data.append({
                "x_vals": x_vals,
                "y_vals": y_vals,
                "interpolator": interpolator,
                "label": data.get("label", f"Curve {i+1}"),
                "color": data.get("color")
            })

        if not interpolated_data:
            return None

        html = generate_multi_interpolation_plot(interpolated_data)

        output_dir = SERVE_DIR
        os.makedirs(output_dir, exist_ok=True)

        filename = "graph.html"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
            print(f"Graph saved to {filepath}")

        return f"http://localhost:8000/{filename}"

    def update_graph_ui(self, html):
        if html:
            self.graph_container.content = ft.WebView(expand=True, url=html)
        else:
            self.graph_container.content = ft.Text("Not enough data points to generate a graph.", color="red")

        self.update()
