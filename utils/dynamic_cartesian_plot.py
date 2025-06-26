import plotly, json
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np

def generate_eval_history_plot(eval_times):
    if not eval_times or len(eval_times) < 1:
        return "<p>No data</p>"

    min_val = min(eval_times)
    mean_val = sum(eval_times) / len(eval_times)
    max_val = max(eval_times)

    min_ms = min_val * 1000
    mean_ms = mean_val * 1000
    max_ms = max_val * 1000

    x_vals = ["Min", "Mean", "Max"]
    y_vals = [min_ms, mean_ms, max_ms]

    text_labels = [f"{ms:.2f} ms" for ms in y_vals]

    trace = go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines+markers+text",
        line=dict(color="#2196F3", width=2),
        marker=dict(size=8),
        text=text_labels,
        textposition="top center",
        hoverinfo="x+y",
        name="Eval Time"
    )

    computation_count = len(eval_times)

    layout = go.Layout(
        showlegend=False,
        height=180,
        margin=dict(l=20, r=20, t=30, b=30),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False, title="Time (ms)"),
        annotations=[
            dict(
                text=f"Computation Count: {computation_count}",
                xref="paper", yref="paper",
                x=0, y=1.2,
                showarrow=False,
                font=dict(size=12, color="black"),
            )
        ]
    )

    fig = go.Figure(data=[trace], layout=layout)
    return plot(fig, output_type="div", include_plotlyjs="cdn", config={"displayModeBar": False})

def generate_interpolation_trace(x_range, y_range, name="Interpolation", color="#0000FF"):
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
            const fullData = JSON.parse(JSON.stringify(fig.data));
            fig.data.forEach(trace => {{
                if (trace.mode === "lines") {{
                    trace.x = [];
                    trace.y = [];
                }}
            }});
            const config = {{
                scrollZoom: true,
                displayModeBar: false,
                displaylogo: false
            }};
            Plotly.newPlot("graph", fig.data, fig.layout, config).then(() => {{
                animateLines();
            }});
            function animateLines() {{
                const steps = 25;
                const delay = 5;  // ms between steps

                let frames = [];

                fullData.forEach((trace, traceIndex) => {{
                    if (trace.mode !== "lines") return;

                    const len = trace.x.length;
                    for (let i = 1; i <= steps; i++) {{
                        const cutoff = Math.floor((i / steps) * len);
                        frames.push({{
                            traceIndex,
                            x: trace.x.slice(0, cutoff),
                            y: trace.y.slice(0, cutoff)
                        }});
                    }}
                }});

                let i = 0;
                function step() {{
                    if (i >= frames.length) return;
                    const f = frames[i];
                    Plotly.restyle("graph", {{
                        x: [f.x],
                        y: [f.y]
                    }}, [f.traceIndex]);
                    i++;
                    setTimeout(step, delay);
                }}

                step();
            }}
        </script>
        <canvas id="fireworks-canvas" style="position:absolute;top:0;left:0;pointer-events:none;width:100%;height:100%;z-index:999;"></canvas>
        <script>
            const canvas = document.getElementById('fireworks-canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            function explode(x, y, color) {{
                for (let i = 0; i < 100; i++) {{
                    let angle = Math.random() * 2 * Math.PI;
                    let speed = Math.random() * 5 + 2;
                    let vx = Math.cos(angle) * speed;
                    let vy = Math.sin(angle) * speed;
                    let alpha = 1;
                    let radius = (Math.random() * 2 + 1) * 8;

                    const particle = {{ x, y, vx, vy, alpha, radius, color }};
                    particles.push(particle);
                }}
            }}

            let particles = [];

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                particles = particles.filter(p => p.alpha > 0);
                for (let p of particles) {{
                    ctx.save();
                    ctx.globalAlpha = p.alpha;
                    ctx.fillStyle = `rgb(${{p.color}})`;
                    ctx.translate(p.x, p.y);
                    ctx.rotate(Math.random() * 2 * Math.PI);
                    ctx.fillRect(-p.radius / 2, -p.radius / 8, p.radius, p.radius / 4);
                    ctx.restore();

                    p.x += p.vx;
                    p.y += p.vy;
                    p.alpha -= 0.02;
                }}
                requestAnimationFrame(draw);
            }}

            function launchFireworks() {{
                for (let i = 0; i < 3; i++) {{
                    const x = Math.random() * canvas.width;
                    const y = Math.random() * canvas.height * 0.8; // avoid bottom edge
                    const color = [
                        '75,42,227',
                        '224,25,77',
                        '25,224,124',
                        '247,238,55',
                        '235,40,190'
                    ][Math.floor(Math.random() * 5)];

                    explode(x, y, color);
                }}
            }}

            setTimeout(() => {{
                launchFireworks();
                draw();
            }}, 20);
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
    memory_usage = 0.0

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
        memory_usage = max(memory_usage, interpolator.get_memory_usage())

        try:
            total_eval_time += interpolator.get_evaluation_only_time()
            stability = interpolator.get_numerical_stability()
            if max_stability is None or stability > max_stability:
                max_stability = stability
        except Exception as e:
            print(f"Error retrieving time/stability: {e}")


    layout = create_layout(all_x_vals, all_y_vals)
    fig = go.Figure(data=all_traces, layout=layout)
    return generate_plot_html(fig), total_eval_time, max_stability, memory_usage
