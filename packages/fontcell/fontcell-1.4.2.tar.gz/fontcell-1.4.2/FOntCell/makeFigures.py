import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from math import sqrt, radians


def set_labeling_coordinates(wedges, length):
    label_coord = np.zeros([len(wedges), 2], dtype=float)

    # set the polar coordinates
    coordinates = take_polar_coord(wedges)
    mean_points = list(map(lambda a: np.mean(a), coordinates))
    label_polar_coord = [[float("{0:.2f}".format(radians(coordinates[i][0]))),
                          float("{0:.2f}".format(radians(mean_points[i])))] for i in range(len(mean_points))]

    # set the sector
    for i in range(len(label_polar_coord)):

        # 1st sector:
        if 0.0 <= label_polar_coord[i][1] < 90.0:
            label_coord[i] = [np.cos(label_polar_coord[i][1]) * length, np.sin(label_polar_coord[i][1]) * length]

        # 2nd sector:
        elif 90.0 <= label_polar_coord[i][1] < 180.0:
            label_coord[i] = [- np.cos(label_polar_coord[i][1]) * length, np.sin(label_polar_coord[i][1]) * length]

        # 3rd sector:
        elif 180.0 <= label_polar_coord[i][1] < 270.0:
            label_coord[i] = [- np.cos(label_polar_coord[i][1]) * length, - np.sin(label_polar_coord[i][1]) * length]

        # 4th sector
        elif 270.0 <= label_polar_coord[i][1] < 360.0:
            label_coord[i] = [np.cos(label_polar_coord[i][1]) * length, - np.sin(label_polar_coord[i][1]) * length]

    return label_coord


def take_polar_coord(wedges):
    coordinates = np.zeros([len(wedges), 2], dtype=float)
    for i in range(len(wedges)):
        coordinates[i] = [wedges[i].theta1, wedges[i].theta2]
    return coordinates


def make_relatedfigures(graph1, graph2, name1, name2, sequen, topolo, notmat, nodes_add, original_nodes, sequen2,
                        topolo2, notmat2, donut_name='donut_diagram.png', square_name='fusion_square_plot.png',
                        donut=False, squares=False):
    # set bar details:
    color1 = '#6495ED'
    color2 = '#8FBC8F'
    color3 = '#FF7F50'
    color4 = '#008080'

    if donut:

        sequen1 = sequen
        topolo1 = topolo
        notmat1 = notmat
        make_donut(sequen1, topolo1, notmat1, sequen2, topolo2, notmat2, color1, color2, color3, donut_name,
                   name1, name2)
    if squares:
        fusion_squares(list(graph1.nodes), list(graph2.nodes), sequen + topolo, original_nodes + nodes_add,
                       color1, color2, color3, color4, square_name, name1, name2)
    return


def make_donut(sequen1, topolo1, notmat1, sequen2, topolo2, notmat2, color1, color2, color3, donut_name,
               onto1_name, onto2_name):

    fig, ax = plt.subplots()
    size = 0.3
    textes1 = ['Sequence', 'Topology', 'Non-matched']
    # textes2 = [onto2_name + ' Sequential', onto2_name + ' ' + topo_state, onto2_name + ' Non-matched']
    array1 = np.array([(sequen1 + topolo1 + notmat1), sequen1, topolo1, notmat1])
    array2 = np.array([(sequen2 + topolo2 + notmat2), sequen2, topolo2, notmat2])
    inter_vals1 = np.interp(array1, (0, array1.max()), (0, 100))
    inter_vals2 = np.interp(array2, (0, array2.max()), (0, 100))
    vals1 = inter_vals1[1:]
    vals2 = inter_vals2[1:]
    # cmap = plt.get_cmap("tab20c")
    outer_colors = np.array([color1, color2, color3])
    inner_colors = np.array([color1, color2, color3])

    wedges1 = ax.pie(vals1, radius=1, colors=outer_colors, wedgeprops=dict(width=size, edgecolor='w'))

    wedges2 = ax.pie(vals2, radius=1-size, colors=inner_colors, wedgeprops=dict(width=size, edgecolor='w'))
    coord1 = set_labeling_coordinates(wedges1[0], size*3)
    coord2 = set_labeling_coordinates(wedges2[0], size*2)
    # for i in range(len(wedges1)):
    #     ax.annotate(str("{0:.2f}".format(vals1[i])))
    # for j in enumerate(len(wedges2)):
    #     ax.annotate(str("{0:.2f}".format(vals2[j])))
    ax.legend(wedges1[0], textes1,
              # title="Ingredients",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              frameon=False)
    plt.text(0, 0, onto2_name, horizontalalignment='center', verticalalignment='center')
    plt.text(0, size*3.1 + size*0.4, onto1_name, horizontalalignment='center', verticalalignment='center')
    [plt.text(coord1[i][0], coord1[i][1], "{0:.1f}".format(vals1[i]), horizontalalignment='center',
              verticalalignment='center') for i in range(len(coord1))]
    [plt.text(coord2[j][0], coord2[j][1], "{0:.1f}".format(vals2[j]), horizontalalignment='center',
              verticalalignment='center') for j in range(len(coord2))]
    # plt.legend((color1, color2, color3, inner_colors[0], inner_colors[0]),
    #            ('Sequential', 'Topological', 'Not matched', 'Added', 'Original'))
    plt.savefig(donut_name)
    plt.close()
    return


def fusion_squares(onto1, onto2, common, resultant, color1, color2, color3, color4, fig_name, name1, name2, r=0.6,
                   alpha=1.0):
    # set the minor 'x' and major 'y'

    if len(onto1) > len(onto2):
        a = len(onto2)
        b1 = len(onto1)
        color_a = color1
        color_b = color2
        label1 = name1
        label2 = name2
    else:
        a = len(onto1)
        b1 = len(onto2)
        label1 = name2
        label2 = name1
        color_b = color1
        color_a = color2

    # check if the minor is 0.2 smaller than the major
    if 0.8*b1 <= a:
        c1 = common * (r-0.2)
        result = resultant * (r-0.2)
        a1 = a * r
        base_a = sqrt(a1)
        height_a = sqrt(a1)
        base_b = sqrt(b1)
        height_b = sqrt(b1)
        base_c = (c1 / height_a)
        height_c = height_a
    else:
        c1 = common
        result = resultant
        # take the borders length
        base_a = sqrt(a)
        height_a = base_a
        base_b = sqrt(b1)
        height_b = base_b
        base_c = c1 / height_a
        height_c = height_a

    # base_c = c1 / height_a
    base_result = (result - (base_a*height_a) + (base_c * height_c)) / height_b
    # Z = border_x * border_z
    # set the start coordinates for x and y
    start_a = ((height_b - height_a) / 2)
    start_b = base_a - base_c
    # start_result = start_y
    # create figures and rectangles
    # fig,ax = plt.subplots()
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, aspect='equal')
    height_max = max(height_b, height_a, height_c)
    base_max = max(base_b, base_a, base_c)
    y_limit = height_max + height_max * 0.1
    x_limit = start_b + base_max + base_max * 0.1
    ax.set_xlim([0, x_limit])
    ax.set_ylim([0, y_limit])

    rect_a = Rectangle((0, start_a), base_a, height_a, fill=True, color=color_a, alpha=alpha)
    ax.add_patch(rect_a)
    rect_b = Rectangle((start_b, 0), base_b, height_b, fill=True, color=color_b, alpha=alpha)
    ax.add_patch(rect_b)
    rect_final = Rectangle((start_b, 0), base_result, height_b, fill=True, color=color3, alpha=alpha-0.2)
    ax.add_patch(rect_final)
    rect_inter = Rectangle((start_b, start_a), base_c, height_c, fill=True, color=color4, alpha=alpha-0.2)
    ax.add_patch(rect_inter)
    plt.savefig(fig_name)

    # calculate the limits

    # plt.legend((color1, color2, color3, color4),
    #            ('ontology A', 'Ontology B', 'How grow Ontology A', 'Equivalents'))

    if label1 == name1:
        # labels
        plt.text(0, start_a + height_a, label1, horizontalalignment='left', verticalalignment='bottom', color=color_a,
                 fontsize='x-large', fontweight='black')
        plt.text(start_b + base_b, height_b, label2, horizontalalignment='right', verticalalignment='bottom',
                 color=color_b, fontsize='x-large', fontweight='black')

        plt.text(start_b, start_a + height_a, 'Synonyms', verticalalignment='bottom', color=color4, fontsize='x-large',
                 fontweight='black')
        plt.text(start_b, height_b, 'Ontology growth', verticalalignment='bottom', color=color3, fontsize='x-large',
                 fontweight='black')

        # numbers
        plt.text(0, start_a + height_a/2, len(onto1), horizontalalignment='left', verticalalignment='bottom',
                 fontsize='x-large', bbox=dict(boxstyle="square", facecolor=color_a, edgecolor=color_a))
        plt.text(start_b + base_b, height_b/2, len(onto2), horizontalalignment='right', verticalalignment='bottom',
                 fontsize='x-large', bbox=dict(boxstyle="square", facecolor=color_b, edgecolor=color_b))

        plt.text(start_b, start_a + height_a/2, common, verticalalignment='bottom', fontsize='x-large',
                 bbox=dict(boxstyle="square", facecolor=color4, edgecolor=color4))
        plt.text(start_b, 0, resultant, verticalalignment='bottom', fontsize='x-large',
                 bbox=dict(boxstyle="square", facecolor=color3, edgecolor=color3))

    elif label2 == name1:
        # labels
        plt.text(0, start_a + height_a, label2, horizontalalignment='left', verticalalignment='bottom', color=color_b,
                 fontsize='x-large')
        plt.text(start_b + base_b, height_b, label1, horizontalalignment='right', verticalalignment='bottom',
                 color=color_a, fontsize='x-large')

        plt.text(start_b, start_a + height_a, 'Synonyms', verticalalignment='bottom', color=color4, fontsize='x-large')
        plt.text(start_b, height_b, 'Ontology growth', verticalalignment='bottom', color=color3, fontsize='x-large')

        # numbers
        plt.text(0, start_a + height_a / 2, len(onto1), horizontalalignment='left', verticalalignment='bottom',
                 fontsize='x-large', bbox=dict(boxstyle="square", facecolor=color_b, edgecolor=color_b))
        plt.text(start_b + base_b, height_b / 2, len(onto2), horizontalalignment='right', verticalalignment='bottom',
                 fontsize='x-large', bbox=dict(boxstyle="square", facecolor=color_a, edgecolor=color_a))

        plt.text(start_b, start_a + height_a / 2, common, verticalalignment='bottom', fontsize='x-large',
                 bbox=dict(boxstyle="square", facecolor=color4, edgecolor=color4))
        plt.text(start_b, 0, resultant, verticalalignment='bottom', fontsize='x-large',
                 bbox=dict(boxstyle="square", facecolor=color3, edgecolor=color3))


    # plt.savefig('test')

    plt.axis('off')

    plt.savefig(fig_name)

    plt.close()

    return
