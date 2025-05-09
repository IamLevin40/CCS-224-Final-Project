import base64, io, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import flet as ft
from flet import Image, ImageFit

from algorithms.lagrange import LagrangeInterpolator
from algorithms.newton import NewtonInterpolator
from algorithms.barycentric import BarycentricInterpolator
from utils.static_cartesian_plot import graph_lagrange, graph_newton, graph_barycentric

class CompareOutputPanel(ft.Container):
    def __init__(self):
        super().__init__(padding=10, alignment=ft.alignment.top_left, expand=True)

        self.graph_columns = []
        self.algorithms = ["Lagrange Interpolation", "Newton Interpolation", "Barycentric Interpolation"]

        self.expressions = ["", "", ""]
        self.time_taken = [0.0, 0.0, 0.0]
        self.numerical_stability = [0.0, 0.0, 0.0]

        for i in range(3):
            graph_display = ft.Text("Insert data points\nto create graph.", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
            title_display = ft.Text(self.algorithms[i], size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF", text_align=ft.TextAlign.CENTER)

            graph_container = ft.Container(content=graph_display, bgcolor="#ffffff", alignment=ft.alignment.center, border_radius=10, expand=True)

            column = ft.Column(
                [
                    title_display,
                    ft.Container(content=graph_container, expand=True)
                ],
                alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, expand=True, spacing=10
            )

            self.graph_columns.append(column)

        self.output_row = ft.Row(
            [
                ft.Container(content=column, expand=True) for column in self.graph_columns
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START, expand=True
        )

        self.polynomial_info = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
        self.time_chart = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
        self.stability_chart = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)

        self.bottom_row = ft.Row(
            [
                ft.Container(content=self.polynomial_info, bgcolor="#ffffff", border_radius=10, padding=10, expand=True, margin=ft.margin.only(left=10, right=10)),
                ft.Container(content=self.time_chart, bgcolor="#ffffff", border_radius=10, padding=10, expand=True, margin=ft.margin.only(left=10, right=10)),
                ft.Container(content=self.stability_chart, bgcolor="#ffffff", border_radius=10, padding=10, expand=True, margin=ft.margin.only(left=10, right=10))
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START, expand=True
        )

        self.content = ft.Column(
            [
                ft.Text("Graphs and Information", size=18, weight=ft.FontWeight.BOLD),
                self.output_row,
                self.bottom_row
            ],
            alignment=ft.MainAxisAlignment.START, expand=True
        )

    def update_output(self, x_vals, y_vals):
        for i in range(3):
            self.graph_columns[i].controls[1].content.content = ft.Text("Computing...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        
        self.polynomial_info.controls = [ft.Text("Loading...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)]
        self.time_chart.controls = [ft.Text("Loading...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)]
        self.stability_chart.controls = [ft.Text("Loading...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)]
        self.update()

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

        self.graph_columns[2].controls[1].content.content = ft.Text("Computing...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.update()
        barycentric_results = self.compute_barycentric(x_vals, y_vals)
        self.update_barycentric_ui(barycentric_results)

        self.update_time_chart()
        self.update_stability_chart()
        self.update_polynomial_info(lagrange_results[0], newton_results[0], barycentric_results[0])

    def compute_lagrange(self, x_vals, y_vals):
        if x_vals and y_vals and len(x_vals) > 1:
            lagrange_poly = LagrangeInterpolator(x_vals, y_vals)
            encoded_image = graph_lagrange(x_vals, y_vals, lagrange_poly)
            time_taken = lagrange_poly.get_evaluation_only_time()
            numerical_stability = lagrange_poly.get_numerical_stability()
            return lagrange_poly, time_taken, encoded_image, numerical_stability
        return None, None, None, None, None

    def update_lagrange_ui(self, results):
        lagrange_poly, time_taken, encoded_image, numerical_stability = results
        if lagrange_poly:
            self.graph_columns[0].controls[1].content.content = Image(src_base64=encoded_image, fit=ImageFit.CONTAIN, expand=True)
            self.time_taken[0] = time_taken
            self.numerical_stability[0] = numerical_stability
        
        self.update()

    def compute_newton(self, x_vals, y_vals):
        if x_vals and y_vals and len(x_vals) > 1:
            newton_poly = NewtonInterpolator(x_vals, y_vals)
            encoded_image = graph_newton(x_vals, y_vals, newton_poly)
            time_taken = newton_poly.get_evaluation_only_time()
            numerical_stability = newton_poly.get_numerical_stability()
            return newton_poly, time_taken, encoded_image, numerical_stability
        return None, None, None, None, None

    def update_newton_ui(self, results):
        newton_poly, time_taken, encoded_image, numerical_stability = results
        if newton_poly:
            self.graph_columns[1].controls[1].content.content = Image(src_base64=encoded_image, fit=ImageFit.CONTAIN, expand=True)
            self.time_taken[1] = time_taken
            self.numerical_stability[1] = numerical_stability
        
        self.update()

    def compute_barycentric(self, x_vals, y_vals):
        if x_vals and y_vals and len(x_vals) > 1:
            barycentric_poly = BarycentricInterpolator(x_vals, y_vals)
            encoded_image = graph_barycentric(x_vals, y_vals, barycentric_poly)
            time_taken = barycentric_poly.get_evaluation_only_time()
            numerical_stability = barycentric_poly.get_numerical_stability()
            return barycentric_poly, time_taken, encoded_image, numerical_stability
        return None, None, None, None, None

    def update_barycentric_ui(self, results):
        barycentric_poly, time_taken, encoded_image, numerical_stability = results
        if barycentric_poly:
            self.graph_columns[2].controls[1].content.content = Image(src_base64=encoded_image, fit=ImageFit.CONTAIN, expand=True)
            self.time_taken[2] = time_taken
            self.numerical_stability[2] = numerical_stability
        
        self.update()

    def update_time_chart(self):
        labels = ["Lagrange", "Newton", "Barycentric"]

        fig, ax = plt.subplots(figsize=(4, 3))
        bars = ax.bar(labels, self.time_taken, color='#2196F3')
        ax.set_ylabel('Time (seconds)')
        ax.set_title('Interpolation Time Comparison')
        ax.grid(True, linestyle='--', alpha=0.7)

        for bar, time in zip(bars, self.time_taken):
            height = bar.get_height()
            label = f"{time*1000:.2f} ms" if time < 1 else f"{time:.4f} s"
            ax.text(bar.get_x() + bar.get_width()/2., height, label, ha='center', va='bottom', rotation=0, fontsize=8)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        time_chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        self.time_chart.controls = [
            ft.Text("Time Taken", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
            ft.Image(src_base64=time_chart_base64, fit=ft.ImageFit.CONTAIN, expand=True)
        ]
        self.update()

    def update_stability_chart(self):
        labels = ["Lagrange", "Newton", "Barycentric"]

        fig, ax = plt.subplots(figsize=(4, 3))
        bars = ax.bar(labels, self.numerical_stability, color='#18A045')
        ax.set_ylabel('Stability Measure')
        ax.set_title('Numerical Stability Comparison')
        ax.grid(True, linestyle='--', alpha=0.7)

        for bar, stability in zip(bars, self.numerical_stability):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{stability:.4f}', ha='center', va='bottom', rotation=0, fontsize=8)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        stability_chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        self.stability_chart.controls = [
            ft.Text("Numerical Stability", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
            ft.Image(src_base64=stability_chart_base64, fit=ft.ImageFit.CONTAIN, expand=True)
        ]
        self.update()

    def update_polynomial_info(self, lagrange_poly, newton_poly, barycentric_poly):
        self.polynomial_info.controls = [ft.Text("Evaluating f(x) from graphs...", size=16, color="#888888", text_align=ft.TextAlign.CENTER)]
        self.update()

        lagrange_poly_expr = lagrange_poly.get_polynomial_expression() if lagrange_poly else "L(x): No data."
        newton_poly_expr = newton_poly.get_polynomial_expression() if newton_poly else "N(x): No data."
        barycentric_poly_expr = barycentric_poly.get_polynomial_expression() if barycentric_poly else "B(x): No data."
        
        lagrange_text = f"Lagrange:\n{lagrange_poly_expr}"
        newton_text = f"Newton:\n{newton_poly_expr}"
        barycentric_text = f"Barycentric:\n{barycentric_poly_expr}"

        self.polynomial_info.controls = [
            ft.Text("Polynomial Expressions", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
            ft.Text(lagrange_text, size=14, color="#000000"),
            ft.Text(newton_text, size=14, color="#000000"),
            ft.Text(barycentric_text, size=14, color="#000000")
        ]
        self.update()
