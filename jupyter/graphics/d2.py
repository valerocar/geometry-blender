import plotly.graph_objs as go
import numpy as np
import plotly


def triangles_xy(xs, ys, triangles_indices):
    xs_n = []
    ys_n = []
    count = int(len(triangles_indices) / 3)
    for i in range(count):
        ii = list(triangles_indices[3 * i:3 * i + 3]) + [triangles_indices[3 * i]]
        xs_n = xs_n + list(xs[ii]) + [None]
        ys_n = ys_n + list(ys[ii]) + [None]
    return go.Scatter(x=xs_n, y=ys_n, name=None, mode="lines", line=dict(width=1))


def triangles(points, triangles_indices):
    xs = []
    ys = []
    for t in triangles_indices:
        p1, p2, p3 = points[t]
        xs = xs + [p1[0], p2[0], p3[0], p1[0], None]
        ys = ys + [p1[1], p2[1], p3[1], p1[1], None]
    trace = go.Scatter(x=xs, y=ys, mode='lines+markers', marker=dict(size=2, color='rgb(0,0,0)'),
                       line=dict(width=2, color='rgb(0,0,0)'))
    return trace


def function_graph(f, domain=[-2, 2], x_res=1000, name=None, showlegend=True, color=None):
    x_min, x_max = domain
    xs = np.linspace(x_min, x_max, x_res)
    ys = f(xs)
    return go.Scatter(x=xs, y=ys, mode="lines", name=name, showlegend=showlegend, line=dict(color=color))


def curve_trace(curve2d, t_res=250, name=None, showlegend=False, color=None):
    t_min, t_max = curve2d.domain
    ts = np.linspace(t_min, t_max, t_res)
    xs, ys = curve2d.eval_position(ts)
    return go.Scatter(x=xs, y=ys, mode="lines", name=name, showlegend=showlegend, line=dict(color=color))


def xys_trace(xs, ys, name=None, showlegend=False, color=None, width=1):
    return go.Scatter(x=xs, y=ys, mode="lines", name=name, showlegend=showlegend,
                      line=dict(color=color, width=width))


def points_trace(ps, name=None, showlegend=False, color=None, width=1):
    xs, ys = ps
    return xys_trace(xs, ys, name=name, showlegend=showlegend, color=color)


def function_contour(f, domain=[-1, 1, -1, 1], level=0):
    x_min, x_max, y_min, y_max = domain
    x_res = y_res = 200
    xs, ys = np.meshgrid(np.linspace(x_min, x_max, x_res), np.linspace(y_min, y_max, y_res))
    zs = f(xs, ys)
    dx = (x_max - x_min) / (x_res - 1)
    dy = (y_max - y_min) / (y_res - 1)
    contour_out = go.Contour(z=zs, x0=x_min, y0=y_min, dx=dx, dy=dy, showscale=False,
                             contours=dict(coloring='lines', start=level, end=level),
                             line=dict(width=2, color='rgb(0,0,0)'))
    return contour_out


def get_basic_layout():
    layout2d = go.Layout(
        title=None,
        paper_bgcolor="#000",
        autosize=True,
        width=800,
        height=800,
        margin=dict(l=60, r=60, b=60, t=60),
        showlegend=False,
    )
    return layout2d


def plot_data(data, frames=None, layout=None):
    if layout is None:
        layout = get_basic_layout()

    if frames is not None:
        fig = go.Figure(data=data, layout=layout, frames=frames)
    else:
        fig = go.Figure(data=data, layout=layout)

    plotly.offline.iplot(fig, )
