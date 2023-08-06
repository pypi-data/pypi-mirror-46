
# Libraries #
from . import Tree_com as tc
from . import doc_managing as doc

from graphviz import Digraph
import numpy as np
import os
# # # # # # #


# main Functions #


def take_coordinates(data, result, color, graph1=None, equiv=None):

    if result:
        # nodes1 = list(map(lambda a: eval, (list(graph1.nodes))))
        nodes1 = list(graph1.nodes)
        # nodes2 = list(map(lambda a:eval, (list(graph2.nodes))))
        data1 = tc.numerate_nodes_in_edge(data)
        color_sequential = 'palegreen2'
        color_topological = 'red'
        color_descendant_assigned = 'lightskyblue'
        # onto1 = taking_old_nodes(data)
        dot = Digraph(comment='Tree fusing', engine='dot', filename='graph.gv')
        # dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp', 'patchwork', 'osage',
        for i in range(len(data)):
            if data[i][0] in nodes1 and data[i][0] not in equiv:
                dot.node(str(data1[i][0]), label="")
            elif data[i][0] in nodes1 and data[i][0] in equiv:
                # print('found')
                if equiv[data[i][0]] == 'Sequential':
                    dot.node(str(data1[i][0]), color=color_sequential, style='filled', label="")
                elif equiv[data[i][0]] == 'Topological':
                    dot.node(str(data1[i][0]), color=color_topological, style='filled', label="")
            else:
                dot.node(str(data1[i][0]), color=color_descendant_assigned, style='filled', label="")

            if data[i][1] in nodes1:
                dot.node(str(data1[i][0]), label="")
            elif data[i][1] in equiv:
                # print('found')
                if equiv[data[i][1]] == 'Sequential':
                    dot.node(str(data1[i][1]), color=color_sequential, style='filled', label="")
                elif equiv[data[i][1]] == 'Topological':
                    dot.node(str(data1[i][1]), color=color_topological, style='filled', label="")
            else:
                dot.node(str(data1[i][1]), color=color_descendant_assigned, style='filled', label="")

        for j in range(data.__len__()):
            dot.edge(str(data1[j][0]), str(data1[j][1]))

        # .view() for saving
        root_dir = os.path.dirname(os.path.realpath(__file__))
        coord = dot.render(filename=root_dir + os.sep + 'graph.gv', view=False, format='plain', directory=root_dir + os.sep)
        # dot.render(view=False)
        # root_dir = os.path.dirname(os.path.realpath(__file__))
        # # project_path = root_dir + os.sep + 'fontcell_files'
        # gv.render('dot', format='plain', filepath=root_dir + os.sep + 'graph.gv')
        # print(coord)
    else:
        data1 = tc.numerate_nodes_in_edge(data)
        dot = Digraph(comment='Tree fusing', engine='dot',
                      filename='graph.gv')  # dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp', 'patchwork', 'osage',
        for i in range(len(data)):
            dot.node(str(data1[i][0]), label="", style='filled', color=color)
            dot.node(str(data1[i][1]), label="", style='filled', color=color)

        for j in range(data.__len__()):
            dot.edge(str(data1[j][0]), str(data1[j][1]))

        # .view() for saving
        root_dir = os.path.dirname(os.path.realpath(__file__))
        coord = dot.render(filename=root_dir + os.sep + 'graph.gv', view=False, format='plain', directory=root_dir + os.sep)
        # project_path = root_dir + os.sep + 'fontcell_files'
        # gv.render('dot', format='plain', filepath=root_dir + os.sep + 'graph.gv')
        # print(coord)
    return


def parse_documents_coordinates(data, result):
    """
    run after take_coordinates without deleting the documents generated
    :param data: a output .ods file from ontology fused
    :param result:
    Creates a parsed coordinates for future drawing
    """
    root_dir = os.path.dirname(os.path.realpath(__file__))
    # project_path = root_dir + os.sep + 'fontcell_files'
    x = open(root_dir + os.sep + 'graph.gv.plain', 'r')
    txt = x.read()
    x.close()
    # print(txt.splitlines().__len__())
    lines = txt.splitlines()
    # print(lines[2].split())

    # Set the number of nodes and edges
    totalnodes = 0
    totaledges = 0
    for i in range(len(lines)):
        if i > 0:
            current = lines[i].split()
            if current[0] == 'node':
                totalnodes += 1
            elif current[0] == 'edge':
                totaledges += 1
    y = 0
    z = 0
    matrixnodes = np.zeros([totalnodes, 4], dtype=object)
    matrixedges = np.zeros([totaledges, 2], dtype=object)
    for i in range(len(lines)):
        if i > 0:
            current = lines[i].split()
            if current[0] == 'node':
                row = [current[1], current[2], current[3], current[10]]
                matrixnodes[y] = row
                y += 1
            elif current[0] == 'edge':
                row = (current[1], current[2])
                matrixedges[z] = row
                z += 1

    # print(matrixnodes)
    # print(matrixedges)
    if result:
        data1 = tc.numerate_nodes_in_edge(data)
        data = transform_for_fill(data, 4)
        dictionary = make_dic_from_numerates(data1, data)
        final_matrix = np.zeros([matrixedges.__len__(), 7], dtype=object)

        for i in range(len(matrixedges)):
            # print(i)
            final_matrix[i][0] = str((int(matrixedges[i][0]), int(matrixedges[i][1])))
            for j in range(len(matrixnodes)):
                if matrixedges[i][0] == matrixnodes[j][0]:
                    final_matrix[i][1] = str((float(matrixnodes[j][1]), float(matrixnodes[j][2])))
                    if matrixnodes[j][3] == 'lightgrey':
                        final_matrix[i][3] = 'orange'
                    else:
                        final_matrix[i][3] = matrixnodes[j][3]
                    final_matrix[i][5] = dictionary[int(matrixedges[i][0])]
                if matrixedges[i][1] == matrixnodes[j][0]:
                    final_matrix[i][2] = str((float(matrixnodes[j][1]), float(matrixnodes[j][2])))
                    if matrixnodes[j][3] == 'lightgrey':
                        final_matrix[i][4] = 'orange'
                    else:
                        final_matrix[i][4] = matrixnodes[j][3]
                    final_matrix[i][6] = dictionary[int(matrixedges[i][1])]
        # print(final_matrix)
        root_dir = os.path.dirname(os.path.realpath(__file__))
        project_path = root_dir + os.sep + 'fontcell_files' + os.sep
        doc.save_ods(final_matrix, project_path + 'graph_viz_coord.ods')
    else:
        data1 = tc.numerate_nodes_in_edge(data)
        data = transform_for_fill(list(data.edges), 4)
        dictionary = make_dic_from_numerates(data1, data)
        final_matrix = np.zeros([matrixedges.__len__(), 7], dtype=object)

        for i in range(len(matrixedges)):
            # print(i)
            final_matrix[i][0] = str((int(matrixedges[i][0]), int(matrixedges[i][1])))
            for j in range(len(matrixnodes)):
                if matrixedges[i][0] == matrixnodes[j][0]:
                    final_matrix[i][1] = str((float(matrixnodes[j][1]), float(matrixnodes[j][2])))
                    if matrixnodes[j][3] == 'lightgrey':
                        final_matrix[i][3] = 'orange'
                    else:
                        final_matrix[i][3] = matrixnodes[j][3]
                    final_matrix[i][5] = dictionary[int(matrixedges[i][0])]
                if matrixedges[i][1] == matrixnodes[j][0]:
                    # if i == 1:
                    #     print()
                    final_matrix[i][2] = str((float(matrixnodes[j][1]), float(matrixnodes[j][2])))
                    if matrixnodes[j][3] == 'lightgrey':
                        final_matrix[i][4] = 'orange'
                    else:
                        final_matrix[i][4] = matrixnodes[j][3]
                    final_matrix[i][6] = dictionary[int(matrixedges[i][1])]
        # print(final_matrix)
        root_dir = os.path.dirname(os.path.realpath(__file__))
        project_path = root_dir + os.sep + 'fontcell_files' + os.sep
        doc.save_ods(final_matrix, project_path + os.sep + 'graph_viz_coord.ods')

    return project_path + os.sep + 'graph_viz_coord.ods'


# support functions #


def taking_old_nodes(fusion_output):
    oldies = []
    for i in range(len(fusion_output)):
        if fusion_output[i][2] == 'new':
            break
        else:
            if fusion_output[i][0] not in oldies:
                oldies.append(fusion_output[i][0])
            if fusion_output[i][1] not in oldies:
                oldies.append(fusion_output[i][1])
    return oldies


def transform_for_fill(array, dimension):
    new_array = np.zeros([array.__len__(), dimension], dtype=object)

    for i in range(len(array)):
        for j in range(len(array[i])):
            new_array[i][j] = array[i][j]

    return new_array


def make_dic_from_numerates(numerates, original):

    dictionary = {}
    for i in range(numerates.__len__()):
        dictionary.update({int(numerates[i][0]): original[i][0]})
        dictionary.update({int(numerates[i][1]): original[i][1]})

    return dictionary
