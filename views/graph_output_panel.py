import flet as ft
from flet import Image, ImageFit

from algorithms.barycentric import BarycentricInterpolator
from utils.cartesian_plot import graph_barycentric

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
            bgcolor="#f0f0f0",
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
            encoded_image = graph_barycentric(x_vals, y_vals, barycentric_poly)
            return barycentric_poly, encoded_image
        return None, None
    
    def update_graph_ui(self, results):
        barycentric_poly, encoded_image = results
        if barycentric_poly:
            self.graph_container.content = Image(
                src_base64=encoded_image,
                fit=ImageFit.CONTAIN,
                expand=True
            )
        else:
            self.graph_container.content = ft.Text("Not enough data points to generate a graph.", color="red")
        
        self.update()