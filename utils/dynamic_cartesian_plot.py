import plotly.graph_objs as go
import numpy as np
import plotly
import json

def graph_barycentric(x_vals, y_vals, barycentric_polynomial):
    x_vals_float = [float(x) for x in x_vals]
    y_vals_float = [float(y) for y in y_vals]

    x_min, x_max = min(x_vals_float), max(x_vals_float)
    x_range = np.linspace(x_min, x_max, 1000).tolist()
    y_range = [float(barycentric_polynomial.interpolate(x)) for x in x_range]

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
        marker=dict(color="red", size=8)
    )

    zeroline_color="#A193B3"
    major_grid_color="#CAB9E1"
    minor_grid_color="#E7DDF8"

    layout = go.Layout(
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
            tickvals=np.arange(min(y_vals_float), max(y_vals_float) + 1, 1),
            minor=dict(
                showgrid=True,
                gridcolor=minor_grid_color,
                gridwidth=0.5,
                tickvals=np.arange(min(y_vals_float) + 0.5, max(y_vals_float) + 1, 0.5)
            )
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest",
        dragmode="pan",
        showlegend=False
    )

    fig = go.Figure(data=[trace_curve, trace_points], layout=layout)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    html_content = f"""
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

    return html_content
