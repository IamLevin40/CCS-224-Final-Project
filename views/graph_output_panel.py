import flet as ft
import os

from utils.server import SERVE_DIR
from algorithms.barycentric import BarycentricInterpolator
from utils.dynamic_cartesian_plot import graph_barycentric

class GraphOutputPanel(ft.Container):
    def __init__(self):
        super().__init__(
            padding=10,
            alignment=ft.alignment.top_left,
            expand=True
        )

        self.graph_display = ft.Text("Insert data points\nto create graph.", size=16, color="#888888", text_align=ft.TextAlign.CENTER)

        self.graph_container = ft.Container(
            content=self.graph_display,
            bgcolor="#ffffff",
            alignment=ft.alignment.center,
            border_radius=10,
            padding=10,
            expand=True
        )

        self.content = ft.Column(
            [
                ft.Text("Graph", size=18, weight=ft.FontWeight.BOLD),
                self.graph_container
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def update_output(self, x_vals, y_vals):
        self.graph_container.content = ft.Text("Computing...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.update()

        results = self.compute_interpolation(x_vals, y_vals)
        self.update_graph_ui(results)

    def compute_interpolation(self, x_vals, y_vals):
        if x_vals and y_vals and len(x_vals) > 1:
            barycentric_poly = BarycentricInterpolator(x_vals, y_vals)
            html = graph_barycentric(x_vals, y_vals, barycentric_poly)

            output_dir = SERVE_DIR
            os.makedirs(output_dir, exist_ok=True)

            filename = "graph.html"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
                print(f"Graph saved to {filepath}")
            
            return f"http://localhost:8000/{filename}"
        return None

    def update_graph_ui(self, html):
        if html:
            self.graph_container.content = ft.WebView(
                expand=True,
                url=html
            )
        else:
            self.graph_container.content = ft.Text("Not enough data points to generate a graph.", color="red")

        self.update()