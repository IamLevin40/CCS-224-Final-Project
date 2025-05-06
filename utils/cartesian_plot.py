import matplotlib.pyplot as plt
import numpy as np
import base64
import io

def graph_lagrange(x_vals, y_vals, lagrange_polynomial):
    x_range = np.linspace(min(x_vals), max(x_vals), 1000)
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

def graph_newton(x_vals, y_vals, newton_polynomial):
    x_range = np.linspace(min(x_vals), max(x_vals), 1000)
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

def graph_barycentric(x_vals, y_vals, barycentric_polynomial):
    x_range = np.linspace(min(x_vals), max(x_vals), 1000)
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