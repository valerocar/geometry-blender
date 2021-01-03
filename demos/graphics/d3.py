import plotly.graph_objs as go
import numpy as np

default_lighting = dict(ambient=0.5, diffuse=0.3, roughness=.4, specular=.3)
default_lightposition = dict(x=10000, y=10000, z=50)


def faces3d(vs, ts, lighting=default_lighting, lightposition=default_lightposition, opacity=1,
            color='rgb(210,210,210)'):
    return go.Mesh3d(x=vs[:, 0], y=vs[:, 1], z=vs[:, 2], i=ts[:, 0], j=ts[:, 1], k=ts[:, 2], lighting=lighting,
                     lightposition=lightposition, color=color, flatshading=False, opacity=opacity)


def function_graph(f, domain=[-2, 2, -2, 2], x_res=100, y_res=100, name=None, opacity=1.0):
    rd = 180
    gr = 180
    bl = 180
    cs = [[0.0, 'rgb(' + str(rd) + ',' + str(gr) + ',' + str(bl) + ')'],
          [1.0, 'rgb(' + str(rd) + ',' + str(gr) + ',' + str(bl) + ')']]

    x_min, x_max, y_min, y_max = domain
    xs, ys = np.meshgrid(np.linspace(x_min, x_max, x_res), np.linspace(y_min, y_max, y_res))
    zs = f(xs, ys)
    lighting_effects = dict(ambient=0.4, diffuse=0.6, roughness=.4, specular=.14)

    return go.Surface(x=xs, y=ys, z=zs, colorscale=cs, showscale=False, opacity=opacity,
                      lighting=lighting_effects, lightposition=dict(x=10000, y=10000, z=50), name=name
                      )


def plot_data(data, layout=None, width=700, height=400, bg_color="rgba(0,0,0,0)"):
    layout = go.Layout(
        title=None,
        paper_bgcolor=bg_color,
        autosize=False,
        width=width,
        height=height,
        margin=dict(l=10, r=10, b=50, t=50),
        showlegend=False,
        scene=dict(
            aspectmode='data',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        )
    )
    return go.Figure(data=data, layout=layout)
