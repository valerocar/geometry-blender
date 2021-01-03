import plotly.graph_objs as go
import numpy as np
from skimage import measure
import plotly


def surface(parametric_surface, u_res=100, v_res=100, opacity=1.0):
    rd = 180
    gr = 180
    bl = 180
    cs = [[0.0, 'rgb(' + str(rd) + ',' + str(gr) + ',' + str(bl) + ')'],
          [1.0, 'rgb(' + str(rd) + ',' + str(gr) + ',' + str(bl) + ')']]

    u_min, u_max, v_min, v_max = parametric_surface.domain
    us, vs = np.meshgrid(np.linspace(u_min, u_max, u_res), np.linspace(v_min, v_max, v_res))
    xs, ys, zs = parametric_surface.eval_position(us, vs)

    lighting_effects = dict(ambient=0.4, diffuse=0.6, roughness=.4, specular=.14)

    return go.Surface(x=xs, y=ys, z=zs, colorscale=cs, showscale=False, opacity=opacity,
                      lighting=lighting_effects, lightposition=dict(x=10000, y=10000, z=50)
                      )


def curve_trace(curve3d, t_res=250, name=None, showlegend=False, color=None):
    t_min, t_max = curve3d.domain
    ts = np.linspace(t_min, t_max, t_res)
    xs, ys, zs = curve3d.eval_position(ts)
    return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", name=name, showlegend=showlegend, line=dict(color=color))


default_lighting = dict(ambient=0.5, diffuse=0.3, roughness=.4, specular=.3)
default_lightposition = dict(x=10000, y=10000, z=50)


def triangles_mesh_and_trace(vs, ts, lighting=default_lighting, lightposition=default_lightposition, opacity=1, color='rgb(180,180,180)'):
    mesh = go.Mesh3d(x=vs[:, 0], y=vs[:, 1], z=vs[:, 2], i=ts[:, 0], j=ts[:, 1], k=ts[:, 2], lighting=lighting,
                     lightposition=lightposition, color=color, flatshading=False, opacity=opacity)

    xs = []
    ys = []
    zs = []
    for t in ts:
        p1, p2, p3 = vs[t]
        xs = xs + [p1[0], p2[0], p3[0], p1[0], None]
        ys = ys + [p1[1], p2[1], p3[1], p1[1], None]
        zs = zs + [p1[2], p2[2], p3[2], p1[2], None]
    trace = go.Scatter3d(x=xs, y=ys, z=zs, mode='lines+markers', marker=dict(size=2, color='rgb(0,0,0)'),
                         line=dict(width=2, color='rgb(0,0,0)'))
    return mesh, trace


def function_graph(f, domain=[-2, 2, -2, 2], x_res=100, y_res=100, name=None, opacity=1.0):
    rd = 180
    gr = 180
    bl = 180
    cs = [[0.0, 'rgb(' + str(rd) + ',' + str(gr) + ',' + str(bl) + ')'],
          [1.0, 'rgb(' + str(rd) + ',' + str(gr) + ',' + str(bl) + ')']]

    x_min, x_max, y_min, y_max = domain
    xs, ys = np.meshgrid(np.linspace(x_min, x_max, x_res), np.linspace(y_min, y_max, y_res))
    zs = f(xs, ys)
    ##lighting_effects = dict(ambient=0.4, diffuse=0.6, roughness=.4, specular=.14, facenormalsepsilon=1,
    ##                        vertexnormalsepsilon=1)

    lighting_effects = dict(ambient=0.4, diffuse=0.6, roughness=.4, specular=.14)

    return go.Surface(x=xs, y=ys, z=zs, colorscale=cs, showscale=False, opacity=opacity,
                      lighting=lighting_effects, lightposition=dict(x=10000, y=10000, z=50), name=name
                      )


def implicit_surface_mesh_and_trace(f, level, domain, resolutions, normals=None):
    res_x, res_y, res_z = resolutions
    x_min, x_max, y_min, y_max, z_min, z_max = domain
    x_inc = (x_max - x_min) / (res_x - 1)
    y_inc = (y_max - y_min) / (res_y - 1)
    z_inc = (z_max - z_min) / (res_z - 1)
    xs, ys, zs = np.meshgrid(np.linspace(x_min, x_max, res_x), np.linspace(y_min, y_max, res_y),
                             np.linspace(z_min, z_max, res_z))
    fs = f(xs, ys, zs)
    #vs, ts, normals, values = measure.marching_cubes_lewiner(fs, level, spacing=(x_inc, y_inc, z_inc),
    #                                                         use_classic=True)
    
    vs, ts, normals, values = measure.marching_cubes(fs, level, spacing=(x_inc, y_inc, z_inc))
    # Correct triangle orientations


    # Adding
    vs[:, 0] += x_min
    vs[:, 1] += y_min
    vs[:, 2] += z_min

    return triangles_mesh_and_trace(vs, ts)


def get_basic_layout(paper_bgcolor="#000"):
    layout3d = go.Layout(
        title=None,
        paper_bgcolor=paper_bgcolor,
        autosize=False,
        width=1200,
        height=800,
        margin=dict(l=10, r=10, b=50, t=50),
        showlegend=False,
        scene=dict(
            aspectmode='data',
            xaxis=dict(showticklabels=True, titlefont=dict(size=20),
                       zeroline=True, showbackground=False, mirror=True,
                       tickfont=dict(size=14), nticks=4, showline=True),

            yaxis=dict(showticklabels=True, titlefont=dict(size=20),
                       zeroline=True, showbackground=False, mirror=True,
                       tickfont=dict(size=14), nticks=4, showline=True),

            zaxis=dict(showticklabels=True, titlefont=dict(size=20),
                       zeroline=True, showbackground=False, mirror=True,
                       tickfont=dict(size=14), nticks=4, showline=True)
        )
    )
    return layout3d

def geometry_mesh_and_trace(geometry, box, res):
    return implicit_surface_mesh_and_trace(geometry.get_lambda(), .5, box,res)
    
def plot_data(data, layout=None):
    if layout is None:
        layout = get_basic_layout("#000")
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.iplot(fig)


def plot_surface(parametric_surface, u_res=100, v_res=100):
    surface_pl = parametric_surface(parametric_surface, u_res=u_res, v_res=v_res)
    fig = go.Figure(data=[surface_pl], layout=get_basic_layout())
    plotly.offline.iplot(fig)
