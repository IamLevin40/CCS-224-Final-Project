import base64
import flet as ft
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
from flet import Image, ImageFit

from algorithms.lagrange import LagrangeInterpolator
from algorithms.newton import NewtonInterpolator
from algorithms.barycentric import BarycentricInterpolator

class OutputPanel(ft.Container):
    def __init__(self):
        super().__init__(
            padding=10,
            alignment=ft.alignment.top_left,
            expand=True
        )

        self.graph_columns = []
        self.info_texts = []
        self.algorithms = ["Lagrange Interpolation", "Newton Interpolation", "Barycentric Interpolation"]

        for i in range(3):
            graph_display = ft.Text("Insert data points\nto create graph.", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
            title_display = ft.Text(self.algorithms[i], size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF", text_align=ft.TextAlign.CENTER)

            graph_container = ft.Container(
                content=graph_display,
                bgcolor="#f0f0f0",
                alignment=ft.alignment.center,
                border_radius=10,
                padding=10,
                expand=True
            )

            info_text = ft.Text("Information will be included here.", size=14, color="#888888")
            self.info_texts.append(info_text)

            info_container = ft.Container(
                content=ft.Column(
                    [info_text],
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    expand=True
                ),
                padding=10,
                bgcolor="#ffffff",
                border_radius=10,
                expand=True
            )

            column = ft.Column(
                [
                    title_display,
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
                spacing=10
            )

            self.graph_columns.append(column)

        self.output_row = ft.Row(
            [
                ft.Container(
                    content=column,
                    expand=True,
                    margin=ft.margin.only(right=10)
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
        # Set loading states
        for i in range(3):
            self.info_texts[i].value = "Calculating..."
            self.info_texts[i].color = "#888888"
            self.info_texts[i].update()

        # Compute and update each algorithm
        self.graph_columns[0].controls[1].content.content = ft.Text("Computing...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.graph_columns[1].controls[1].content.content = ft.Text("Waiting for the\nfirst algorithm...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.graph_columns[2].controls[1].content.content = ft.Text("Waiting for the\nsecond algorithm...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.update()
        lagrange_results = self.compute_lagrange(x_vals, y_vals)
        self.update_lagrange_ui(lagrange_results)

        self.graph_columns[1].controls[1].content.content = ft.Text("Computing...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.graph_columns[2].controls[1].content.content = ft.Text("Waiting for the\nsecond algorithm...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.update()
        newton_results = self.compute_newton(x_vals, y_vals)
        self.update_newton_ui(newton_results)

        barycentric_results = self.compute_barycentric(x_vals, y_vals)
        self.update_barycentric_ui(barycentric_results)

    def compute_lagrange(self, x_vals, y_vals):
        if x_vals and y_vals and len(x_vals) > 1:
            lagrange_poly = LagrangeInterpolator(x_vals, y_vals)
            encoded_image = self.graph_lagrange(x_vals, y_vals, lagrange_poly)
            expression = lagrange_poly.get_polynomial_expression()
            time_taken = lagrange_poly.get_interpolation_time()
            numerical_stability = lagrange_poly.get_numerical_stability()
            return lagrange_poly, expression, time_taken, encoded_image, numerical_stability
        return None, None, None, None, None

    def update_lagrange_ui(self, results):
        lagrange_poly, expression, time_taken, encoded_image, numerical_stability = results
        if lagrange_poly:
            self.graph_columns[0].controls[1].content.content = Image(
                src_base64=encoded_image,
                fit=ImageFit.CONTAIN,
                expand=True
            )
            self.info_texts[0].value = f"Time Taken: {time_taken:.10f} seconds\nNumerical Stability: {numerical_stability:.10f}\n\nLagrange Polynomial:\n{expression}"
            self.info_texts[0].color = "#000000"
        else:
            self.info_texts[0].value = "Not enough valid data points."
        
        self.update()

    def compute_newton(self, x_vals, y_vals):
        if x_vals and y_vals and len(x_vals) > 1:
            newton_poly = NewtonInterpolator(x_vals, y_vals)
            encoded_image = self.graph_newton(x_vals, y_vals, newton_poly)
            expression = newton_poly.get_polynomial_expression()
            time_taken = newton_poly.get_interpolation_time()
            numerical_stability = newton_poly.get_numerical_stability()
            return newton_poly, expression, time_taken, encoded_image, numerical_stability
        return None, None, None, None, None

    def update_newton_ui(self, results):
        newton_poly, expression, time_taken, encoded_image, numerical_stability = results
        if newton_poly:
            self.graph_columns[1].controls[1].content.content = Image(
                src_base64=encoded_image,
                fit=ImageFit.CONTAIN,
                expand=True
            )
            self.info_texts[1].value = f"Time Taken: {time_taken:.10f} seconds\nNumerical Stability: {numerical_stability:.10f}\n\nNewton Polynomial:\n{expression}"
            self.info_texts[1].color = "#000000"
        else:
            self.info_texts[1].value = "Not enough valid data points."
        
        self.update()

    def compute_barycentric(self, x_vals, y_vals):
        if x_vals and y_vals and len(x_vals) > 1:
            barycentric_poly = BarycentricInterpolator(x_vals, y_vals)
            encoded_image = self.graph_barycentric(x_vals, y_vals, barycentric_poly)
            expression = barycentric_poly.get_polynomial_expression()
            time_taken = barycentric_poly.get_interpolation_time()
            numerical_stability = barycentric_poly.get_numerical_stability()
            return barycentric_poly, expression, time_taken, encoded_image, numerical_stability
        return None, None, None, None, None

    def update_barycentric_ui(self, results):
        barycentric_poly, expression, time_taken, encoded_image, numerical_stability = results
        if barycentric_poly:
            self.graph_columns[2].controls[1].content.content = Image(
                src_base64=encoded_image,
                fit=ImageFit.CONTAIN,
                expand=True
            )
            self.info_texts[2].value = f"Time Taken: {time_taken:.10f} seconds\nNumerical Stability: {numerical_stability:.10f}\n\nBarycentric Polynomial:\n{expression}"
            self.info_texts[2].color = "#000000"
        else:
            self.info_texts[2].value = "Not enough valid data points."
        
        self.update()

    def graph_lagrange(self, x_vals, y_vals, lagrange_polynomial):
        x_range = np.linspace(min(x_vals), max(x_vals), 300)
        y_range = [lagrange_polynomial.interpolate(x) for x in x_range]

        fig, ax = plt.subplots()
        ax.plot(x_range, y_range, label="Lagrange Polynomial", color="#2196F3", linewidth=2.5)
        ax.scatter(x_vals, y_vals, color="#F44336", s=100, zorder=5, label="Data Points")
        ax.grid(True)
        ax.set_aspect('equal', adjustable='datalim')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)

        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return encoded_image
    
    def graph_newton(self, x_vals, y_vals, newton_polynomial):
        x_range = np.linspace(min(x_vals), max(x_vals), 300)
        y_range = [newton_polynomial.interpolate(x) for x in x_range]

        fig, ax = plt.subplots()
        ax.plot(x_range, y_range, label="Newton Polynomial", color="#2196F3", linewidth=2.5)
        ax.scatter(x_vals, y_vals, color="#F44336", s=100, zorder=5, label="Data Points")
        ax.grid(True)
        ax.set_aspect('equal', adjustable='datalim')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)

        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return encoded_image

    def graph_barycentric(self, x_vals, y_vals, barycentric_polynomial):
        x_range = np.linspace(min(x_vals), max(x_vals), 300)
        y_range = [barycentric_polynomial.interpolate(x) for x in x_range]

        fig, ax = plt.subplots()
        ax.plot(x_range, y_range, label="Barycentric Polynomial", color="#2196F3", linewidth=2.5)
        ax.scatter(x_vals, y_vals, color="#F44336", s=100, zorder=5, label="Data Points")
        ax.grid(True)
        ax.set_aspect('equal', adjustable='datalim')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)

        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return encoded_image