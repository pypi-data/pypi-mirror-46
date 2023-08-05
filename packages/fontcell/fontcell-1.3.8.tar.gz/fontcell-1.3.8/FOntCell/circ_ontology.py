from . import doc_managing as doc

import math
import numpy as np
import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go


def from_dend_to_pol(dend_points_x, dend_points_y):
    '''
    Given a set of X and Y dendrogram coordinates (dcoord and icoord elements from scipy
    dendrogram, or any related set of points) transforms these points' XY cartesian coordinates
    into (r, theta) polar coordinates, used for visualization.

    :param dend_points_x: nested list with X points.
    :param dend_points_y: nested list with Y points.
    '''
   
    # First, the nested list is flattened into a usual list
    x_flatten, y_flatten = np.array(dend_points_x).flatten(), np.array(dend_points_y).flatten()

    # print(x_flatten)
    # Extreme coordinates are obtained to calculate the span of r and theta coordinates
    min_y, max_y = np.min(y_flatten), np.max(y_flatten)
    min_x, max_x = np.min(x_flatten), np.max(x_flatten)

    # print(min_y, max_y, min_x, max_x)
    # to distribute the indexes (positions) in the last row, we find the x positions whose y
    # position is the smallest

    k = 1
    for i in set(y_flatten):
        # print(k, len(x_flatten[np.argwhere(y_flatten == i)]))
        k += 1

    n_leaves = max([len(x_flatten[np.argwhere(y_flatten == i)]) for i in set(y_flatten)])

    # Now, maximum and minimum r and thetas are calculated.
    r_f = 1.0 * max_y
    r_0 = min_y
    theta_0 = 0
    theta_f = 2*math.pi*(n_leaves - 1)/(n_leaves)
    phase = np.pi/4 + 0.35

    rcoords, thetacoords = [], []

    for i in range(len(dend_points_x)):
        rcoords.append([(r_f - r) / (r_f - r_0) for r in dend_points_y[i]])
        thetacoords.append(
            [(theta_f - theta_0) * (theta - min_x) / (max_x - min_x) + phase
             for theta in dend_points_x[i]])


    return rcoords, thetacoords


def plot_html(savefile, rcoords_init, rcoords_end,
              thetacoords_init, thetacoords_end,
              colors_init, colors_end, names_init, names_end):
    data = []

    # HTML Plotting creates a dendrogram with as many colors as clusters have been created,
    # and, due to problems rendering the text (there is no option to correctly rotate
    # the text in plotly Scatter), scatter points with hover info are created.

    # First, dendrogram scatter is created by plotting lines of the dendrograms
    plotted_coords = []

    # This plots a circle to show the levels of the dendrogram
    set_r = set(np.array(rcoords_init + rcoords_end).flatten())
    for r in set_r:
        data += [go.Scatterpolar(
            r=100*[r],
            theta=np.linspace(0, 2*np.pi, 100),
            mode='lines',
            thetaunit="radians",
            hoverinfo='none',
            line=dict(
                color='pink'),
            showlegend=False,
            opacity=0.45


        )]

    
    def return_opacity(rcoords_init, thetacoords_init, rcoords_end, thetacoords_end, i):
        minx = np.min([((rcoords_init[k]*np.cos(thetacoords_init[k])-
                        rcoords_end[k]*np.cos(thetacoords_end[k])) ** 2+
                       (rcoords_init[k] * np.sin(thetacoords_init[k]) -
                        rcoords_end[k] * np.sin(thetacoords_end[k])) ** 2)**0.5 for k in range(len(rcoords_init))])
        maxx =  np.max([((rcoords_init[k]*np.cos(thetacoords_init[k])-
                        rcoords_end[k]*np.cos(thetacoords_end[k])) ** 2+
                       (rcoords_init[k] * np.sin(thetacoords_init[k]) -
                        rcoords_end[k] * np.sin(thetacoords_end[k])) ** 2)**0.5 for k in range(len(rcoords_init))])

        alpha = ((((rcoords_init[i]*np.cos(thetacoords_init[i])-
                        rcoords_end[i]*np.cos(thetacoords_end[i])) ** 2+
                       (rcoords_init[i] * np.sin(thetacoords_init[i]) -
                        rcoords_end[i] * np.sin(thetacoords_end[i])) ** 2)**0.5 - minx)/(maxx-minx))

        return 0.75*(1 - alpha) + 0.25


    for i in range(len(rcoords_init)):
        data += [go.Scatterpolar(
            r=[rcoords_init[i], rcoords_end[i]],
            theta=[thetacoords_init[i], thetacoords_end[i]],
            mode='lines',
            thetaunit="radians",
            hoverinfo='none',
            line=dict(
                color='gray'),
            showlegend=False,
            opacity= return_opacity(rcoords_init, thetacoords_init, rcoords_end, thetacoords_end, i)

        )]

    for i in range(len(rcoords_init)):
        if [rcoords_init[i],thetacoords_init[i]] not in plotted_coords:
            data += [go.Scatterpolar(
                            r = [rcoords_init[i]],
                            theta = [thetacoords_init[i]],
                            mode = 'markers',
                            thetaunit="radians",
                            hoverinfo='text',
                            hovertext=names_init[i],
                            marker =  dict(
                            color=colors_init[i],
                            size=8),
                            showlegend=False,

                        )
                    ]
            plotted_coords.append([rcoords_init[i],thetacoords_init[i]])

        if [rcoords_end[i],thetacoords_end[i]] not in plotted_coords:
            data += [go.Scatterpolar(
                            r = [rcoords_end[i]],
                            theta = [thetacoords_end[i]],
                            mode = 'markers',
                            thetaunit="radians",
                            hoverinfo='text',
                            hovertext=names_end[i],
                            marker =  dict(
                            color=colors_end[i],
                            size=8),
                            showlegend=False,

                        )
                    ]
            plotted_coords.append([rcoords_end[i],thetacoords_end[i]])







    # if labels:
    #     # Next, points were the leaves end are also added. In this case rcoords is not used
    #     # because it contains intermediate leaves. In order to get the final positions, we
    #     # calculate the angles beforehand and store it into thetatextcoords.
    #
    #     r = 1.02
    #
    #     # Names stores into the legend each point. In order not to get any repetition, we plot with
    #     # the name parameter (legend) only once: the first time they appear.
    #     saidnames = []
    #     for i in range(len(group_numbers)):
    #         if group_names[group_numbers[i]] not in saidnames:
    #             saidnames.append(group_names[group_numbers[i]])
    #             showlegend=True
    #         else:
    #             showlegend=False
    #
    #         data += [go.Scatterpolar(
    #                 r=[r],
    #                 theta=[thetatextcoords[i]],
    #                 mode='markers',
    #                 name=group_names[group_numbers[i]],
    #                 hovertext=['%s / %s' %(ticklabels[i], group_names[group_numbers[i]])],
    #                 thetaunit="radians",
    #                 marker=dict(
    #                     color=group_colors[group_numbers[i]],
    #                     size=8
    #                 ),
    #                 showlegend=showlegend)]

    # And now we remove the info of axis ticks, ticklabels, etc.
    layout = go.Layout(polar = dict(
                        domain=dict(
                            y=[0, 1],),
                          radialaxis = dict(
                            showticklabels=False,
                              showgrid=False,
                              linewidth=0,
                              ticks='',
                              tickwidth=0,
                              categoryarray=[],
                          ),
                          angularaxis = dict(
                              showticklabels=False,
                              showgrid=False,
                              linewidth=0,
                              ticks='',
                              tickwidth=0,
                              categoryarray=[]
                          )
                        ),)

    fig = go.Figure(data=data, layout=layout)

    if savefile[-5:] != '.html':
        savefile += '.html'
    # print(savefile)
    plot(fig, filename=savefile, auto_open=False)


def circular_graph(file, name):
    '''
    :param file: localization of .ods file in the specific format for taking the current coordinates
    format (for every row): [(father_num_code, son_num_code), (father node coordinate), (son node coordinate), color_father, color_son, father_label, son_label
    '''
    array = doc.import_ods(file)
    # print(array)

    graph_init_num_list, graph_end_num_list = [], []
    graph_init_x_list, graph_init_y_list = [], []
    graph_end_x_list, graph_end_y_list = [], []
    color_init_list, color_end_list = [], []
    name_init_list, name_end_list = [], []

    color_translator = {'y': 'orange', 'b': 'dodgerblue', 'r': 'darkred', 'g': 'limegreen',
                        'tab:purple': 'purple', 'palegreen2': 'palegreen', '': 'black'}

    delm = ','

    for i in array:
        graph_init_num_list.append(float(i[0][1:-1].split(delm)[0]))
        graph_end_num_list.append(float(i[0][1:-1].split(delm)[1]))
        graph_init_x_list.append(float(i[1][1:-1].split(delm)[0]))
        graph_init_y_list.append(float(i[1][1:-1].split(delm)[1]))
        graph_end_x_list.append(float(i[2][1:-1].split(delm)[0]))
        graph_end_y_list.append(float(i[2][1:-1].split(delm)[1]))
        if i[3] in color_translator.keys():
            color_init_list.append(color_translator[i[3]])
        else:
            color_init_list.append(i[3])
        if i[4] in color_translator.keys():
            color_end_list.append(color_translator[i[4]])
        else:
            color_end_list.append(i[4])
        name_init_list.append(i[5])
        name_end_list.append(i[6])

    df_graph = pd.DataFrame({'Graph init num': graph_init_num_list, 'Graph init x': graph_init_x_list,
                             'Graph init y': graph_init_y_list, 'Graph init color': color_init_list,
                             'Graph init name': name_init_list,
                             'Graph end num': graph_end_num_list, 'Graph end x': graph_end_x_list,
                             'Graph end y': graph_end_y_list, 'Graph end color': color_end_list,
                             'Graph end name': name_end_list,
                             })

    df_graph = df_graph[['Graph init num', 'Graph init x', 'Graph init y', 'Graph init color',
                         'Graph init name',
                         'Graph end num', 'Graph end x', 'Graph end y', 'Graph end color',
                         'Graph end name']]
    # print(df_graph)

    rcoords, thetacoords = from_dend_to_pol(
        dend_points_x=[graph_init_x_list, graph_end_x_list],
        dend_points_y=[graph_init_y_list, graph_end_y_list])

    # print(rcoords, '\n', thetacoords)

    plot_html(savefile=name, rcoords_init=rcoords[0], rcoords_end=rcoords[1],
              thetacoords_init=thetacoords[0], thetacoords_end=thetacoords[1],
              colors_init=color_init_list, colors_end=color_end_list,
              names_init=name_init_list, names_end=name_end_list)
    return