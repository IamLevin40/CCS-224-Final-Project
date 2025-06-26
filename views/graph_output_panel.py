import os
import flet as ft
import hashlib

from utils.server import SERVE_DIR
from algorithms.lagrange import LagrangeInterpolator
from algorithms.newton import NewtonInterpolator
from algorithms.barycentric import BarycentricInterpolator
from utils.dynamic_cartesian_plot import generate_multi_interpolation_plot
from utils.dynamic_cartesian_plot import generate_eval_history_plot

class GraphOutputPanel(ft.Container):
    def __init__(self):
        super().__init__(padding=10, alignment=ft.alignment.top_left, expand=True)

        self.selected_interpolator = "Barycentric"
        self.interpolator_selector = ft.RadioGroup(content=ft.Row([
                ft.Radio(value="Lagrange", label="Lagrange", fill_color="#2196F3"),
                ft.Radio(value="Newton", label="Newton", fill_color="#2196F3"),
                ft.Radio(value="Barycentric", label="Barycentric", fill_color="#2196F3"),
            ], alignment=ft.MainAxisAlignment.START),
            value="Barycentric", on_change=self.on_interpolator_change,
        )

        self.graph_display = ft.Text("Insert data points\nto create graph.", size=16, color="#888888", text_align=ft.TextAlign.CENTER)
        self.graph_container = ft.Container(content=self.graph_display, bgcolor="#ffffff", alignment=ft.alignment.center, border_radius=10, padding=10, expand=True)
        self.info_line = ft.Text("No Information Found", size=12, color="#dddddd")

        self.eval_times = []
        self.current_dataset_hash = None
        self.show_eval_graph = False

        self.eval_button = ft.TextButton("⏱ Show Eval History", on_click=self.toggle_eval_graph)
        self.eval_graph_container = ft.Container(visible=False, expand=False, height=200, content=ft.Text("No history yet."), bgcolor="#f0f0f0", border_radius=10, padding=5)

        self.content = ft.Column(
            [
                ft.Row([
                    ft.Text("Graph", size=18, weight=ft.FontWeight.BOLD),
                    self.interpolator_selector,
                    self.eval_button,
                    ft.Container(content=self.info_line, expand=True, alignment=ft.alignment.center_right),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.eval_graph_container,
                self.graph_container,
            ],
            alignment=ft.MainAxisAlignment.START, expand=True
        )

    def on_interpolator_change(self, e):
        self.selected_interpolator = e.control.value

    def update_output(self, datasets):
        """
        datasets: List of dicts with keys:
            - x_vals
            - y_vals
            - label (optional)
            - color (optional)
        """
        dataset_hash = hashlib.md5(str(datasets).encode()).hexdigest()

        if dataset_hash != self.current_dataset_hash:
            self.eval_times = []
            self.current_dataset_hash = dataset_hash

        html_url, total_eval_time, max_stability, memory_usage = self.compute_interpolations(datasets)

        if total_eval_time is not None:
            self.eval_times.append(total_eval_time)

        self.update_info_line(total_eval_time, max_stability, memory_usage)
        self.update_eval_history_ui()
        self.update_graph_ui(html_url)

    def compute_interpolations(self, datasets):
        interpolated_data = []

        for i, data in enumerate(datasets):
            x_vals = data.get("x_vals", [])
            y_vals = data.get("y_vals", [])

            if not x_vals or not y_vals or len(x_vals) <= 1:
                continue

            if self.selected_interpolator == "Lagrange":
                interpolator = LagrangeInterpolator(x_vals, y_vals)
                print(f"Using Lagrange Interpolator for {data.get('label', f'Line {i+1}')}")
            elif self.selected_interpolator == "Newton":
                interpolator = NewtonInterpolator(x_vals, y_vals)
                print(f"Using Newton Interpolator for {data.get('label', f'Line {i+1}')}")
            elif self.selected_interpolator == "Barycentric":
                interpolator = BarycentricInterpolator(x_vals, y_vals)
                print(f"Using Barycentric Interpolator for {data.get('label', f'Line {i+1}')}")
            
            interpolated_data.append({
                "x_vals": x_vals,
                "y_vals": y_vals,
                "interpolator": interpolator,
                "label": data.get("label", f"Line {i+1}"),
                "color": data.get("color")
            })

        if not interpolated_data:
            return None

        html, total_eval_time, max_stability, memory_usage = generate_multi_interpolation_plot(interpolated_data)

        output_dir = SERVE_DIR
        os.makedirs(output_dir, exist_ok=True)

        filename = "graph.html"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
            print(f"Graph saved to {filepath}")

        return f"http://localhost:8000/{filename}", total_eval_time, max_stability, memory_usage
    
    def update_info_line(self, total_eval_time, max_stability, memory_usage):
        if total_eval_time is None or max_stability is None:
            self.info_line.value = "No Information Found"
        else:
            if total_eval_time < 1:
                eval_display = f"{total_eval_time * 1000:.2f}ms"
            else:
                eval_display = f"{total_eval_time:.5f}s"

            stability_display = f"{max_stability:.7f}"

            self.info_line.value = f"Memory: {memory_usage} KB | ⏱ {eval_display} | 📈 Stability: {stability_display}"

        self.update()

    def update_graph_ui(self, html):
        if html:
            self.graph_container.content = ft.WebView(expand=True, url=html)
        else:
            self.graph_container.content = ft.Text("Not enough data points to generate a graph.", color="red")

        self.update()

    def toggle_eval_graph(self, e):
        self.show_eval_graph = not self.show_eval_graph
        self.eval_graph_container.visible = self.show_eval_graph
        self.update()

    def update_eval_history_ui(self):
        if not self.eval_times or len(self.eval_times) < 1:
            self.eval_graph_container.content = ft.Text("No history yet.")
            return

        html = generate_eval_history_plot(self.eval_times)
        output_dir = SERVE_DIR
        filepath = os.path.join(output_dir, "eval_history.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        self.eval_graph_container.content = ft.WebView(expand=True, url="http://localhost:8000/eval_history.html")
