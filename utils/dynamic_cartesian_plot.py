import plotly
import plotly.graph_objs as go
import numpy as np
import json

def generate_interpolation_trace(x_range, y_range, name="Interpolation", color="blue"):
    return go.Scatter(x=x_range, y=y_range, mode="lines", name=name, line=dict(color=color, width=2))

def generate_data_points_trace(x_vals, y_vals, name="Data Points", color="#222222"):
    return go.Scatter(x=x_vals, y=y_vals, mode="markers", name=name, marker=dict(color=color, size=6))

def create_layout(x_vals, y_vals):
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)

    zeroline_color = "#A193B3"
    major_grid_color = "#CAB9E1"
    minor_grid_color = "#E7DDF8"

    return go.Layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            scaleanchor="y",
            scaleratio=1,
            showline=True,
            zeroline=True,
            zerolinecolor=zeroline_color,
            zerolinewidth=2,
            showgrid=True,
            gridcolor=major_grid_color,
            gridwidth=1,
            tickmode="array",
            tickvals=np.arange(x_min, x_max + 1, 1),
            minor=dict(
                showgrid=True,
                gridcolor=minor_grid_color,
                gridwidth=0.5,
                tickvals=np.arange(x_min + 0.5, x_max + 1, 0.5)
            )
        ),
        yaxis=dict(
            showline=True,
            zeroline=True,
            zerolinecolor=zeroline_color,
            zerolinewidth=2,
            showgrid=True,
            gridcolor=major_grid_color,
            gridwidth=1,
            tickmode="array",
            tickvals=np.arange(y_min, y_max + 1, 1),
            minor=dict(
                showgrid=True,
                gridcolor=minor_grid_color,
                gridwidth=0.5,
                tickvals=np.arange(y_min + 0.5, y_max + 1, 0.5)
            )
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest",
        dragmode="pan",
        showlegend=False
    )

def generate_plot_html(fig):
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
            }}
            #graph {{
                width: 100vw;
                height: 100vh;
            }}
        </style>
    </head>
    <body>
        <div id="graph"></div>
        <script>
            const fig = {fig_json};
            const config = {{
                scrollZoom: true,
                displayModeBar: false,
                displaylogo: false
            }};
            Plotly.newPlot("graph", fig.data, fig.layout, config);
        </script>
    </body>
    </html>
    """

def generate_multi_interpolation_plot(data_sets):
    """
    data_sets: list of dicts with keys:
        - x_vals: list of x data
        - y_vals: list of y data
        - interpolator: object with `.interpolate(x)` method
        - label: (optional) curve name
        - color: (optional) line color
    """
    all_traces = []
    all_x_vals, all_y_vals = [], []
    total_eval_time = 0.0
    max_stability = None

    for i, data in enumerate(data_sets):
        x_vals = [float(x) for x in data["x_vals"]]
        y_vals = [float(y) for y in data["y_vals"]]
        interpolator = data["interpolator"]
        label = data.get("label", f"Interpolation {i+1}")
        color = data.get("color", f"hsl({i * 50}, 70%, 50%)")

        x_range = np.linspace(min(x_vals), max(x_vals), 1000).tolist()
        y_range = [float(interpolator.interpolate(x)) for x in x_range]

        trace_curve = generate_interpolation_trace(x_range, y_range, name=label, color=color)
        trace_points = generate_data_points_trace(x_vals, y_vals)

        all_traces.extend([trace_curve, trace_points])
        all_x_vals.extend(x_vals)
        all_y_vals.extend(y_vals)
        
        try:
            total_eval_time += interpolator.get_evaluation_only_time()
            stability = interpolator.get_numerical_stability()
            if max_stability is None or stability > max_stability:
                max_stability = stability
        except Exception as e:
            print(f"Error retrieving time/stability: {e}")

    layout = create_layout(all_x_vals, all_y_vals)
    fig = go.Figure(data=all_traces, layout=layout)
    return generate_plot_html(fig), total_eval_time, max_stability
