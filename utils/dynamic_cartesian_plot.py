import plotly.graph_objs as go
import numpy as np
import plotly
import json

def graph_barycentric(x_vals, y_vals, barycentric_polynomial):
    x_range = np.linspace(float(min(x_vals)), float(max(x_vals)), 1000)
    y_range = [float(barycentric_polynomial.interpolate(x)) for x in x_range]
    print(f"X Range: {x_range}")
    print(f"Y Range: {y_range}")

    x_vals_float = [float(x) for x in x_vals]
    y_vals_float = [float(y) for y in y_vals]

    trace_curve = go.Scatter(
        x=x_range,
        y=y_range,
        mode="lines",
        name="Interpolation",
        line=dict(color="blue", width=2)
    )

    trace_points = go.Scatter(
        x=x_vals_float,
        y=y_vals_float,
        mode="markers",
        name="Data Points",
        marker=dict(color="red", size=10)
    )

    layout = go.Layout(
        title="Barycentric Interpolation",
        xaxis=dict(title="X", scaleanchor="y", scaleratio=1),
        yaxis=dict(title="Y"),
        hovermode="closest",
        dragmode="pan"
    )

    fig = go.Figure(data=[trace_curve, trace_points], layout=layout)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    html_content = f"""
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    </head>
    <body>
        <div id="graph" style="width:100%;height:100%;"></div>
        <script>
            const fig = {fig_json};
            Plotly.newPlot("graph", fig.data, fig.layout);
        </script>
    </body>
    </html>
    """

    return html_content
