import plotly.graph_objs as go


def mesh3d(ps, ts, opacity=1, color='rgb(210,210,210)'):
    """
    Creates a plotly graphical object from the position of a collection of points ps and triangles ts
    :param ps: positions of vertices in 3-dimensional space
    :param ts: indices of vertices forming triangles
    :param opacity: the opacity of the mesh
    :param color: the color of the mesh
    :return:
    """
    lighting = dict(ambient=0.5, diffuse=0.3, roughness=.4, specular=.3)
    light_position = dict(x=10000, y=10000, z=50)
    return go.Mesh3d(x=ps[:, 0], y=ps[:, 1], z=ps[:, 2], i=ts[:, 0], j=ts[:, 1], k=ts[:, 2], lighting=lighting,
                     lightposition=light_position, color=color, flatshading=False, opacity=opacity)


def get_figure(data, width=700, height=400, bg_color="rgba(0,0,0,0)"):
    """
    Gets a plotly figure for the list of plotly graphical objects

    :param data: A list of plotly graphical objects to be displayed
    :param width: The width of the 3d renderer
    :param height: the height of the 3d renderer
    :param bg_color: background color of the 3d renderer
    :return: A plotly Figure
    """
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
