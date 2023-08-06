# Aim: This file will work as a main for a 'Ontology fusion'


# ##################### #
# Libraries and Modules #
# ##################### #
from . import Tree_com as treeComp
from . import doc_managing as doc
from . import OBO_Formating as obo
from . import coord_taker as coord
from . import circ_ontology as co
from . import pyhtml as h
from . import makeFigures as make

import numpy as np
import os
from mpi4py import MPI
import bigmpi4py as tbx
from collections import OrderedDict
import networkx as nx
import tqdm as tq
import warnings
# ######### #


def gen_graph_similarity_array(node1, ontology1, ontology2, subgraphs2, window_size, topological=True,
                               constraint_threshold=0.0, sequential_dictionary=None, topological_cosine=False,
                               topological_pearson=False, topological_euclidean=False):
    nodes2_i = np.array(ontology2.nodes)
    nodes2 = list(map(lambda a: eval(a), nodes2_i))

    subgraph1 = treeComp.subGraphGenerator(ontology1, node1, window_size)

    if topological:
        topological_matrixx = np.zeros((subgraphs2.__len__()), dtype=object)
        if not topological_cosine and not topological_euclidean and not topological_pearson:
            for i in range(len(subgraphs2)):
                topological_matrixx[i] = treeComp.g_similarity(subgraph1, subgraphs2[i], convergence_threshold=0.001,
                                                               obtain_loops_number=False)
        else:
            for j in range(len(subgraphs2)):
                topological_matrixx[j] = treeComp.g_similarity_noniterative(subgraph1, subgraphs2[j],
                                                                            topological_cosine, topological_euclidean,
                                                                            topological_pearson)
        return topological_matrixx
    else:
        match, value = treeComp.g_constraint_similarity(subgraph1, subgraphs2, node1, nodes2, sequential_dictionary,
                                                          window_size, constraint_threshold)
        return match, value


def gen_text_sequential_matrix(graph1, graph2, text_process=False, synonyms=False, word_list_to_clear1=None,
                               word_list_to_clear2=None, split_from1=None, split_since1=None, split_from2=None,
                               split_since2=None):
    nodes1 = list(graph1.nodes)
    nodes2 = list(graph2.nodes)

    nodes1_p = list(map(lambda a: a, list(map(lambda a: eval(a), nodes1))))
    nodes2_p = list(map(lambda a: a, list(map(lambda a: eval(a), nodes2))))

    if text_process:
        # print()
        # process the nodes_labeling
        if word_list_to_clear1 is not None:
            nodes1_t = treeComp.clearOntology_labels(nodes1_p, word_list_to_clear1, synonyms, split_from=split_from1,
                                                     split_since=split_since1)
        if word_list_to_clear2 is not None:
            nodes2_t = treeComp.clearOntology_labels(nodes2_p, word_list_to_clear2, synonyms, split_from=split_from2,
                                                     split_since=split_since2)
    else:
        nodes1_t = nodes1_p
        nodes2_t = nodes2_p

    if not synonyms:
        sequential_matrix = np.zeros([nodes1_t.__len__(), nodes2_t.__len__()], dtype=object)

        for i in range(nodes1_t.__len__()):
            for j in range(nodes2_t.__len__()):
                simil = treeComp.similarity(nodes1_t[i], nodes2_t[j])
                sequential_matrix[i][j] = simil

        return sequential_matrix

    elif synonyms:

        sequential_matrix = np.zeros([nodes1_t.__len__(), nodes2_t.__len__()], dtype=object)

        for i in range(nodes1_t.__len__()):
            # print(i)
            for j in range(nodes2_t.__len__()):
                simil = treeComp.similarity_synonyms(nodes1_t[i], nodes2_t[j])
                sequential_matrix[i][j] = simil
        return sequential_matrix


def fuse_graphs(graph1, graph2, assing_matrix, root):
    '''
    Fuse two graphs having a assignation matrix. V5: Another way to fuse... 'Translating fuse'
    '''
    # Make the dictionaries and introduce edges
    edges1 = list(graph1.edges)
    edges2 = list(graph2.edges)

    type_dictionary = {}
    assing_dictionary = {}
    assing_dictionary_inverse = {}
    typus_2_dictionary = {}

    for i in range(len(assing_matrix)):
        term1 = str(assing_matrix[i][0])
        term2 = str(assing_matrix[i][1])
        tipus = assing_matrix[i][4]
        both = [term1, term2]
        assing_dictionary.update({term2: term1})
        type_dictionary.update({tuple(both): tipus})
        assing_dictionary_inverse.update({term1: term2})
        typus_2_dictionary.update({term1: tipus})

    # Translate all the possibles graph2 nodes
    new_edges2 = np.zeros([len(edges2), 2], dtype=object)
    translated = []
    for i in range(len(edges2)):
        row = [edges2[i][0], edges2[i][1]]
        if edges2[i][0] in assing_dictionary:
            row[0] = assing_dictionary[edges2[i][0]]
            translated.append(row[0])
        if edges2[i][1] in assing_dictionary:
            row[1] = assing_dictionary[edges2[i][1]]
            translated.append(row[1])
        new_edges2[i] = row

    new_edges = list(map(lambda a: tuple(a), new_edges2))

    old_edges = list(map(lambda a: tuple(a), edges1))

    # fuse both list with no repeats
    if root is None:
        fusedlist = list(OrderedDict.fromkeys(old_edges + new_edges))
    else:
        fusedlist1 = list(OrderedDict.fromkeys(old_edges + new_edges))
        test_digraph = treeComp.buildDiGraph(fusedlist1)
        fused_edges = list(test_digraph.edges)
        fusedlist = []
        for i in range(len(fused_edges)):
            if test_digraph.has_node(fused_edges[i][0]) and test_digraph.has_node(fused_edges[i][1]):
                if nx.has_path(test_digraph, root, fused_edges[i][0]) and nx.has_path(test_digraph, root, fused_edges[i][1]):
                    fusedlist.append((fused_edges[i][0], fused_edges[i][1]))

    # add old/new for colouring
    finallist = np.zeros([len(fusedlist), 4], dtype=list)
    for i in range(len(fusedlist)):
        if fusedlist[i] not in edges1:
            finallist[i] = [fusedlist[i][0], fusedlist[i][1], 'new', 0]
            if fusedlist[i][0] in assing_dictionary_inverse:
                tipus = tuple([fusedlist[i][0], assing_dictionary_inverse[fusedlist[i][0]]])
                finallist[i][3] = type_dictionary[tipus]
        else:
            finallist[i] = [fusedlist[i][0], fusedlist[i][1], 'old', 0]
    return finallist, typus_2_dictionary


def equivalent_dictionaryV4(graph1, graph2, sequential, globalthreshold, localthreshold, subgraphs1, subgraphs2
                            , windowsize=4, simtopo=True, constraint_threshold=0.0, topological_cosine=False
                            , topological_pearson=False, topological_euclidean=False, topological_threshold=0.0):

    '''
    This function was a improvement of the another function with similar name.
    :param topological: matrix format (graph1.nodes x graph2.nodes)
    :param sequential: matrix format (graph1.nodes x graph2.nodes)
    :param globalthreshold: threshold of word similarity
    :param subgraphs1/subgraphs2: list of digraph object from every graph at the previous window size
    :param B_to_A: a analysis that search a topological candidate and now compares
    :return: matrix: graph1.__len__() x 5
    [node from graph1, node from graph2 assigned, topological score, sequence score, assignation type]
    '''
    # Pre-process
    graph1_nodes = list(map(lambda a: eval(a), graph1.nodes))
    graph2_nodes = list(map(lambda a: eval(a), graph2.nodes))

    # Explicit conversion string to float
    sequen_score = np.zeros(sequential.__len__(), dtype=object)

    for l in range(sequential.__len__()):
        sequen_score[l] = list(map(lambda a:float(a), sequential[l]))

    matchMatrix = np.zeros([graph1_nodes.__len__(), 5], dtype=object)
    # print('graph1_nodes.__len__():', graph1_nodes.__len__())
    # print('graph2_nodes.__len__():', graph2_nodes.__len__())
    # print('sequential: ', len(sequential), len(sequential[0]))
    dictionary_seq = dictionary_fromMatrix(graph1_nodes, graph2_nodes, sequential)
    # print('Topological: ', len(topological), len(topological[0]))

    # Sequential match
    sequential_founds_g1 = []
    sequential_founds_g2 = []

    seq_match= betters(graph1_nodes, graph2_nodes, dictionary_seq)
    count = 0
    for i in range(len(seq_match)):
        # if i == 88:
        #     print()
        if seq_match[i][2] >= globalthreshold:
            matchMatrix[i] = [seq_match[i][0],
                              seq_match[i][1],
                              seq_match[i][2],
                              'None',
                              'Sequential'
                              ]
            sequential_founds_g1.append(seq_match[i][0])
            sequential_founds_g2.append(seq_match[i][1])
        else:
            matchMatrix[i][0] = seq_match[i][0]
            count += 1
            continue

    if simtopo:
        for i in range(len(matchMatrix)):
            # print(i)
            if matchMatrix[i][1] == '0' or matchMatrix[i][1] == 0:
                # A non-sequential resolved node
                # Inside topological match, use the localSequence() tool, and add a mean threshold for accept or deny
                # one of assignations.
                # if a node wasn't found a match, pass to the next. (keep it blank)

                matrix = gen_graph_similarity_array(graph1_nodes[i], graph1, graph2, subgraphs2, windowsize
                                                    , topological_cosine=topological_cosine
                                                    , topological_pearson=topological_pearson
                                                    , topological_euclidean=topological_euclidean)
                # for n in range(len(matrix)):
                #     matrix[n] = float(matrix[n])
                event = False
                count = 0
                # Default not match assign
                matchMatrix[i] = [graph1_nodes[i],
                                  0,
                                  0,
                                  0,
                                  'Not Matched'
                                  ]
                while not event:
                    # print('node ' + str(i) + ', sub-loop: ' + str(count))
                    if count >= len(matrix):
                        # print('no')
                        event = True
                    pos = np.argmax(matrix)
                    candidate1 = graph2_nodes[pos]
                    if candidate1 not in seq_match and subgraphs1[i] != None and matrix[pos] >= topological_threshold:
                        # matrix = set_positionNegative(matrix, pos)
                        mean = localSequence(subgraphs1[i], subgraphs2[pos], dictionary_seq, node1=graph1_nodes[i], node2=candidate1)
                        if mean > localthreshold :
                            # print('yes')
                            matchMatrix[i] = [graph1_nodes[i],
                                              candidate1,
                                              dictionary_seq[(tuple(graph1_nodes[i]), tuple(candidate1))],
                                              mean,
                                              'Topological'
                                              ]

                            event = True
                            count += 1
                        else:
                            count += 1
                    else:
                        count += 1
                    matrix = set_positionNegative(matrix, pos)
            else:
                continue

    elif not simtopo:
        dictionary_of_sequentials =dictionary_from_betters(seq_match, globalthreshold)
        for i in range(len(matchMatrix)):
            # print(i)
            if matchMatrix[i][1] == '0' or matchMatrix[i][1] == 0:
                # A non-sequential resolved node
                match, value = gen_graph_similarity_array(graph1_nodes[i], graph1, graph2, subgraphs2, windowsize, topological=False,
                                                   constraint_threshold=constraint_threshold,
                                                   sequential_dictionary=dictionary_of_sequentials)
                # for n in range(len(matrix)):
                #     matrix[n] = float(matrix[n])

                # Default not match assign
                if match == None:
                    matchMatrix[i] = [graph1_nodes[i],
                                      0,
                                      0,
                                      0,
                                      'Not Matched'
                                      ]
                else:
                    # print('yes')
                    candidate = match
                    matchMatrix[i] = [graph1_nodes[i],
                                      candidate,
                                      dictionary_seq[(tuple(graph1_nodes[i]), tuple(candidate))],
                                      value,
                                      'Topological'
                                      ]
                continue

    return matchMatrix


def equivalent_dictionaryV4_parallelized(comm, graph1, graph2, sequential, globalthreshold, localthreshold, subgraphs1,
                                         subgraphs2 , windowsize=4, simtopo=True, constraint_threshold=0.0,
                                         topological_cosine=False, topological_pearson=False,
                                         topological_euclidean=False, topological_threshold=0.0):
    '''
    This function was a improvement of the another function with similar name.
    :param topological: matrix format (graph1.nodes x graph2.nodes)
    :param sequential: matrix format (graph1.nodes x graph2.nodes)
    :param globalthreshold: threshold of word similarity
    :param subgraphs1/subgraphs2: list of digraph object from every graph at the previous window size
    :param B_to_A: a analysis that search a topological candidate and now compares
    :return: matrix: graph1.__len__() x 5
    [node from graph1, node from graph2 assigned, topological score, sequence score, assignation type]
    '''
    # Pre-process
    graph1_nodes = list(map(lambda a: eval(a), graph1.nodes))
    graph2_nodes = list(map(lambda a: eval(a), graph2.nodes))

    # Explicit conversion string to float
    sequen_score = np.zeros(sequential.__len__(), dtype=object)

    for l in range(sequential.__len__()):
        sequen_score[l] = list(map(lambda a:float(a), sequential[l]))

    matchMatrix = np.zeros([graph1_nodes.__len__(), 5], dtype=object)
    # print('graph1_nodes.__len__():', graph1_nodes.__len__())
    # print('graph2_nodes.__len__():', graph2_nodes.__len__())
    # print('sequential: ', len(sequential), len(sequential[0]))
    dictionary_seq = dictionary_fromMatrix(graph1_nodes, graph2_nodes, sequential)
    # print('Topological: ', len(topological), len(topological[0]))

    # Sequential match
    sequential_founds_g1 = []
    sequential_founds_g2 = []

    seq_match= betters(graph1_nodes, graph2_nodes, dictionary_seq)
    count = 0
    for i in range(len(seq_match)):
        # if i == 88:
        #     print()
        if seq_match[i][2] >= globalthreshold:
            matchMatrix[i] = [seq_match[i][0],
                              seq_match[i][1],
                              seq_match[i][2],
                              'None',
                              'Sequential'
                              ]
            sequential_founds_g1.append(seq_match[i][0])
            sequential_founds_g2.append(seq_match[i][1])
        else:
            matchMatrix[i][0] = seq_match[i][0]
            count += 1
            continue

    matchMatrix1 = tbx.scatter(matchMatrix, comm)

    matchMatrix2 = equivalent_analysis_for_paralellized(matchMatrix1, simtopo, graph1_nodes, graph1, graph2, subgraphs2,
                                                        windowsize, graph2_nodes, seq_match, subgraphs1, dictionary_seq,
                                                        constraint_threshold, localthreshold, topological_cosine,
                                                        topological_pearson, topological_euclidean,
                                                        topological_threshold, globalthreshold)

    matchMatrix = tbx.gather(matchMatrix2, comm)

    return matchMatrix


def equivalent_analysis_for_paralellized(matchMatrix, simtopo, graph1_nodes, graph1, graph2, subgraphs2, windowsize,
                                         graph2_nodes, seq_match, subgraphs1, dictionary_seq, constraint_threshold,
                                         localthreshold, topological_cosine, topological_pearson, topological_euclidean,
                                         topological_threshold, globalthresgold):
    # Delete a message of a False error from numpy (a bug at numpy>=1.16.1)
    if simtopo:
        for i in range(len(matchMatrix)):
            # print(i)
            if matchMatrix[i][1] == '0' or matchMatrix[i][1] == 0:
                # A non-sequential resolved node
                # Inside topological match, use the localSequence() tool, and add a mean threshold for accept or deny one of
                # assignations.
                # if a node wasn't found a match, pass to the next. (keep it blank)

                matrix = gen_graph_similarity_array(graph1_nodes[i], graph1, graph2, subgraphs2, windowsize,
                                                    topological_cosine=topological_cosine,
                                                    topological_pearson= topological_pearson,
                                                    topological_euclidean=topological_euclidean)
                # for n in range(len(matrix)):
                #     matrix[n] = float(matrix[n])
                event = False
                count = 0
                # Default not match assign
                matchMatrix[i] = [graph1_nodes[i],
                                  0,
                                  0,
                                  0,
                                  'Not Matched'
                                  ]
                while not event:
                     # print('node ' + str(i) + ', sub-loop: ' + str(count))
                    if count >= len(matrix):
                        # print('no')
                        event = True
                    pos = np.argmax(matrix)
                    candidate1 = graph2_nodes[pos]
                    if candidate1 not in seq_match and subgraphs1[i] != None and matrix[pos] >= topological_threshold:
                        # matrix = set_positionNegative(matrix, pos)
                        mean = localSequence(subgraphs1[i], subgraphs2[pos], dictionary_seq, node1=graph1_nodes[i], node2=candidate1)
                        if mean > localthreshold :
                            # print('yes')
                            matchMatrix[i] = [graph1_nodes[i],
                                              candidate1,
                                              dictionary_seq[(tuple(graph1_nodes[i]), tuple(candidate1))],
                                              mean,
                                              'Topological'
                                              ]

                            event = True
                            count += 1
                        else:
                            count += 1
                    else:
                        count += 1
                    matrix = set_positionNegative(matrix, pos)
            else:
                continue

    elif not simtopo:
        dictionary_of_sequentials =dictionary_from_betters(seq_match, globalthresgold)
        for i in range(len(matchMatrix)):
            # print(i)
            if matchMatrix[i][1] == '0' or matchMatrix[i][1] == 0:
                # A non-sequential resolved node
                match, value = gen_graph_similarity_array(graph1_nodes[i], graph1, graph2, subgraphs2, windowsize, topological=False,
                                                   constraint_threshold=constraint_threshold,
                                                   sequential_dictionary=dictionary_of_sequentials)
                # for n in range(len(matrix)):
                #     matrix[n] = float(matrix[n])

                # Default not match assign
                if match == None:
                    matchMatrix[i] = [graph1_nodes[i],
                                      0,
                                      0,
                                      0,
                                      'Not Matched'
                                      ]
                else:
                    # print('yes')
                    candidate = match
                    matchMatrix[i] = [graph1_nodes[i],
                                      candidate,
                                      dictionary_seq[(tuple(graph1_nodes[i]), tuple(candidate))],
                                      value,
                                      'Topological'
                                      ]
                continue
    return matchMatrix


def dictionary_from_betters(sequential_matchs, globalthreshold):
    '''
    create a dictionary that you put node from ontology1 and give node from ontology2 assigned by betters.
    '''
    dictionary_sq = {}
    for i in range(len(sequential_matchs)):
        if sequential_matchs[i][2] >= globalthreshold:
            dictionary_sq.update({sequential_matchs[i][0]: sequential_matchs[i][1]})
    return dictionary_sq


def localSequence(subgraph1, subgraph2, dictioseq, node1=None, node2=None, inverted=False):
    '''
    Given two nodes, his graphs and the sequential matrix. Make the mean of the convolutional windows
    '''
    nodelist1 = list(subgraph1.nodes)
    nodelist2 = list(subgraph2.nodes)

    # take both node_problem
    if node1 != None:
        nodelist1.remove(node1)
    if node2 != None:
        nodelist2.remove(node2)

    bettervalues = np.zeros(nodelist1.__len__(), float)
    for i in range(nodelist1.__len__()):
        values = np.zeros(nodelist2.__len__(), dtype=float)
        for j in range(nodelist2.__len__()):
            if not inverted:
                values[j] = dictioseq[(tuple(nodelist1[i]), tuple(nodelist2[j]))]
            elif inverted:
                values[j] = dictioseq[(tuple(nodelist2[j]), tuple(nodelist1[i]))]
        bettervalues[i] = np.amax(values)

    mean = np.mean(bettervalues)
    return mean


def betters(nodes1, nodes2, dictio):
    '''
    Make a list of nodes from graph 1 to a list with nodes of graph 2 and his better value of assignation
    '''
    final_list = np.zeros(nodes1.__len__(), dtype=object)
    for i in range(len(nodes1)):
        # if i == 87:
        #     print(i)
        old_value = 0.0
        row = [0, 0, 0]
        for j in range(nodes2.__len__()):
            value = dictio[(tuple(nodes1[i]), tuple(nodes2[j]))]
            if value > old_value:
                old_value = value
                row = [nodes1[i], nodes2[j], value]
        final_list[i] = row
    return final_list


def dictionary_fromMatrix(graph1_nodes, graph2_nodes, sequential_matrix):
    # nodes1 = list(graph1.nodes)
    # nodes2 = list(graph2.nodes)
    # print('graph1_nodes.__len__():', graph1_nodes.__len__())
    # print('graph2_nodes.__len__():', graph2_nodes.__len__())
    # print('matrix: ', len(sequential_matrix), len(sequential_matrix[0]))
    dictionary = {}
    for i in range(len(graph1_nodes)):
        for j in range(len(graph2_nodes)):
            dictionary.update({(graph1_nodes[i], graph2_nodes[j]): float(sequential_matrix[i][j])})
    return dictionary


def set_positionNegative(array, position):
    '''
    Given an array change the symbol(positive or negative) for the value on position
    '''
    if isinstance(array[position], int):
        array[position] = -1 * array[position]
    elif isinstance(array[position], float):
        array[position] = -1.0 * array[position]
    '''
    for i in range(len(array)):
        if i == position and isinstance(array[i], int):
            array[i] = -1 * array[i]
        elif i == position and isinstance(array[i], float):
            array[i] = -1.0 * array[i]
    '''
    return array


def quality_controls(equivalent_matrix, fused_matrix, graph2, return_values=False):
    '''
    :param equivalent_matrix: Matrix of equivalence obtained during fusing ontology
    :param fused_matrix: final matrix from the ontology fusing process
    :return: Shows the results of quality control
    '''
    # Number of nodes and edges added
    nodes2 = list(graph2.nodes)
    original_edges = 0
    original_edges_list = []
    original_nodes = 0
    edges_add = 0
    all_nodes = []
    original_old_nodes = []
    nodes_add = 0
    all_edges = []
    onto2_nodes_added = []

    for i in range(len(fused_matrix)):
        all_edges.append(fused_matrix[i][0:2])
        if fused_matrix[i][2] == 'new':
            edges_add += 1
            if fused_matrix[i][0] not in all_nodes:
                nodes_add += 1
                all_nodes.append(fused_matrix[i][0])
            if fused_matrix[i][1] not in all_nodes:
                nodes_add +=1
                all_nodes.append(fused_matrix[i][1])
        else:
            original_edges += 1
            original_edges_list.append(fused_matrix[i][0:2])
            if fused_matrix[i][0] not in all_nodes:
                all_nodes.append(fused_matrix[i][0])
                original_old_nodes.append(fused_matrix[i][0])
                original_nodes +=1
            if fused_matrix[i][1] not in all_nodes:
                all_nodes.append(fused_matrix[i][1])
                original_old_nodes.append(fused_matrix[i][1])
                original_nodes +=1

    # % of Sequential and Topological and Not Matched
    totals = 0
    sequen = 0
    topolo = 0
    notmat = 0
    sequen2_listed = []
    topolo2_listed = []
    nodes_onto2_assigned = []
    for i in range(len(equivalent_matrix)):
        totals += 1
        if equivalent_matrix[i][4] == 'Sequential':
            sequen += 1
            if equivalent_matrix[i][1] not in sequen2_listed and equivalent_matrix[i][1] != '0' \
                    and equivalent_matrix[i][1] != 0:
                sequen2_listed.append(equivalent_matrix[i][1])
        elif equivalent_matrix[i][4] == 'Topological':
            topolo += 1
            if equivalent_matrix[i][1] not in topolo2_listed and equivalent_matrix[i][1] != '0' \
                    and equivalent_matrix[i][1] != 0:
                topolo2_listed.append(equivalent_matrix[i][1])
        elif equivalent_matrix[i][4] == 'Not Matched':
            notmat += 1
        nodes_onto2_assigned.append(equivalent_matrix[i][1])

    # Find how many ontology2 nodes don't be at the final ontology fused
    sequen2 = sequen2_listed.__len__()
    topolo2 = topolo2_listed.__len__()
    notmat2 = nodes2.__len__() - (sequen2 + topolo2)
    graph = graph2
    nodes = np.array(graph.nodes)
    nodes_left = []
    for i in range(len(nodes)):
        if nodes[i] not in all_nodes and nodes[i] not in nodes_onto2_assigned and nodes[i] not in nodes_left:
            nodes_left.append(nodes[i])
        if nodes[i] not in all_nodes and nodes[i] not in nodes_onto2_assigned and nodes[i] not in nodes_left:
            nodes_left.append(nodes[i])

    nodes_onto2_sort = len(list(set(nodes_onto2_assigned)))

    if return_values:
        return sequen, topolo, notmat, totals, edges_add, nodes_add, original_edges, original_nodes, nodes_onto2_sort,\
               sequen2, topolo2, notmat2
    elif not return_values:

        # Print results:
        print('added as a sequential: ', sequen)
        p_sequen = "{0:.3f}".format(sequen/totals*100)
        print('% of sequential match: ', p_sequen, '%')
        print('added as a topological-local sequential: ', topolo)
        p_topolo = "{0:.3f}".format(topolo / totals*100)
        print('% of topological match: ', p_topolo, '%')
        print('Not Matched: ', notmat)
        p_notmat = "{0:.3f}".format(notmat / totals*100)
        print('% of not matched: ', p_notmat, '%')

        print('Edges added: ', edges_add)
        print('edges grow in a ', "{0:.3f}".format(edges_add / original_edges * 100), '%')
        print('Nodes added: ', nodes_add)
        print('nodes grow in a ', "{0:.3f}".format(nodes_add / original_nodes * 100), '%')
        return


def quality_controls_V2(equivalent_matrix, fused_matrix, graph1, graph2):
    '''
    :param equivalent_matrix: Matrix of equivalence obtained during fusing ontology
    :param fused_matrix: final matrix from the ontology fusing process
    :return: Shows the results of quality control
    '''
    # Number of nodes and edges added
    nodes1 = list(graph1.nodes)
    nodes2 = list(graph2.nodes)
    edges1 = list(graph1.edges)
    # edges2 = list(graph2.edges)

    # make a edges structure
    descendant_relations = []
    for i in range(len(fused_matrix)):
        descendant_relations.append([fused_matrix[i][0], fused_matrix[i][1]])
    resulted_graph = treeComp.buildDiGraph(descendant_relations)
    nodes_result = list(resulted_graph.nodes)

    # % of Sequential and Topological and Not Matched
    totals = 0
    sequen = 0
    topolo = 0
    notmat = 0
    sequen2_listed = []
    topolo2_listed = []
    nodes_onto2_assigned = []
    for i in range(len(equivalent_matrix)):
        totals += 1
        if equivalent_matrix[i][4] == 'Sequential':
            sequen += 1
            if equivalent_matrix[i][1] not in sequen2_listed and equivalent_matrix[i][1] != '0' \
                    and equivalent_matrix[i][1] != 0:
                sequen2_listed.append(equivalent_matrix[i][1])
        elif equivalent_matrix[i][4] == 'Topological':
            topolo += 1
            if equivalent_matrix[i][1] not in topolo2_listed and equivalent_matrix[i][1] != '0' \
                    and equivalent_matrix[i][1] != 0:
                topolo2_listed.append(equivalent_matrix[i][1])
        elif equivalent_matrix[i][4] == 'Not Matched':
            notmat += 1
        nodes_onto2_assigned.append(equivalent_matrix[i][1])

    # Find how many ontology2 nodes don't be at the final ontology fused
    sequen2 = sequen2_listed.__len__()
    topolo2 = topolo2_listed.__len__()
    notmat2 = nodes2.__len__() - (sequen2 + topolo2)
    graph = graph2
    nodes = np.array(graph.nodes)
    nodes_left = []
    for i in range(len(nodes)):
        if nodes[i] not in nodes_result and nodes[i] not in nodes_onto2_assigned and nodes[i] not in nodes_left:
            nodes_left.append(nodes[i])
        if nodes[i] not in nodes_result and nodes[i] not in nodes_onto2_assigned and nodes[i] not in nodes_left:
            nodes_left.append(nodes[i])

    nodes_onto2_sort = len(list(set(nodes_onto2_assigned)))

    return sequen, topolo, notmat, totals, len(fused_matrix) - len(edges1), len(nodes_result) - len(nodes1), \
           len(edges1), len(nodes1), nodes_onto2_sort, sequen2, topolo2, notmat2


def circular_graphing(data, name, directory, result=True, color=None, parallelization=False, g1=None, equiv=None):
    coord.take_coordinates(data, result, color, g1, equiv)
    coordin = coord.parse_documents_coordinates(data, result)
    co.circular_graph(coordin, directory + name)
    if not parallelization:
        root_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep
        os.remove(root_dir + 'graph.gv')
        #     os.remove(root_dir + 'graph.gv.pdf')
        os.remove(root_dir + 'graph.gv.plain')
    return


def generate_subgraphs(ontology, nodes, windows, paralellization):
    subgraphs = np.zeros(len(nodes), dtype=object)
    if paralellization:
        for j in range(len(nodes)):
            subgraphs[j] = treeComp.subGraphGenerator(ontology, nodes[j], windows)
    else:
        pbar = tq.tqdm(total=len(nodes))
        for j in range(len(nodes)):
            subgraphs[j] = treeComp.subGraphGenerator(ontology, nodes[j], windows)
            pbar.update(1)
        pbar.close()
    return subgraphs


def set_True_root(graph1, root):
    root_final = root
    nodes = list(graph1.nodes)
    for i in range(len(nodes)):
        if eval(nodes[i])[0] == root:
            root_final = nodes[i]

    return root_final


def fuseOntologies3(onto1, onto2
                    , name1, name2
                    , onto1_path=''
                    , onto1_fuseclasses=True
                    , onto2_fuseclasses=True
                    , onto1_restriction=False
                    , onto2_restriction=False
                    , onto1_list_clear=None
                    , onto2_list_clear=None
                    , synonyms=False
                    , text_process=False
                    , split_from1=None
                    , split_since1=None
                    , split_from2=None
                    , split_since2=None
                    , windowsize=4
                    , globalthreshold=0.85
                    , localthreshold=0.7
                    , constraint_threshold=0.0
                    , topological_threshold=0.0
                    , save_internals=True
                    , parallelization=False
                    , OBO_format_result=True
                    , save_internals_equiv=True
                    , draw_circular=True
                    , topological_test=True
                    , topological_cosine=False
                    , topological_pearson=False
                    , topological_euclidean=False
                    , output_folder=None):

    # generate names
    # r_path = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.dirname(os.path.realpath(__file__))
    path_to_doc = root_dir + os.sep + 'fontcell_files' + os.sep
    # path_to_img = r_path + os.sep + 'images' + os.sep
    warnings.simplefilter(action='ignore', category=FutureWarning)
    if output_folder is None:
        output_folder = path_to_doc
    comm = MPI.COMM_WORLD
    if name1.__len__() >= 3:
        first_partA = name1[0:3]
    else:
        first_partA = name1[0:1]

    if name2.__len__() >= 3:
        first_partB = name2[0:3]
    else:
        first_partB = name2[0:1]

    add_name1 = first_partA + '_' + first_partB + '_S' + ''.join(str(globalthreshold).split('.'))
    if topological_test:
        add_name2 = '_LS' + ''.join(str(localthreshold).split('.'))
    else:
        add_name2 = '_CT' + ''.join(str(constraint_threshold).split('.'))
    add_name3 = '_W' + str(windowsize)

    sequential_name = 'seq_matrix_' + add_name1 + '.csv'
    # topological_name = folder + 'top_matrix_' + add_name1 + add_name3 + '.csv'
    equivalent_name = 'equiv_dictio_' + add_name1 + add_name2 + add_name3 + '.ods'
    result_name = 'f_graphs_' + add_name1 + add_name2 + add_name3 + '.ods'

    # print('import the ontologies')
    # if onto1_fusedproduct:
    #     # print('do something')
    #     onto1 = fromOutputFusedOntology_to_readableOntology(import_ods(onto1_path))
    # else:
    #     onto1 = import_ods(onto1_path)
    # onto2 = import_ods(onto2_path)

    print('make a graph for each ontology')
    # T ~ 3 mins
    O1, secondary1 = treeComp.makeDigraph_fromOntology(onto1, onto1_fuseclasses, onto1_restriction)
    O2, secondary2 = treeComp.makeDigraph_fromOntology(onto2, onto2_fuseclasses, onto2_restriction)
    nodes1 = list(map(lambda a: eval(a), O1.nodes))
    nodes2 = list(map(lambda a: eval(a), O2.nodes))
    # Pre-generate sub-graph
    if parallelization:
        # comm = MPI.COMM_WORLD

        if comm.rank == 0:
            print('Pre-generate sub-graph')
            idx1 = [int(i) for i in np.linspace(0, len(nodes1), comm.size+1)]
            nodes1 = [nodes1[idx1[i]:idx1[i+1]] for i in range(len(idx1)-1)]

            idx2 = [int(i) for i in np.linspace(0, len(nodes2), comm.size + 1)]
            nodes2 = [nodes2[idx2[i]:idx2[i + 1]] for i in range(len(idx2) - 1)]

        else:
            nodes1, nodes2 = None, None


        nodes1_p = comm.scatter(nodes1)
        nodes2_p = comm.scatter(nodes2)
        subgraphs1_r = generate_subgraphs(O1, nodes1_p, windowsize, parallelization)
        subgraphs2_r = generate_subgraphs(O2, nodes2_p, windowsize, parallelization)
        subgraphs1 = comm.allgather(subgraphs1_r)
        subgraphs2 = comm.allgather(subgraphs2_r)

        xxx = []
        yyy = []
        for i in subgraphs1:
            xxx += list(i)
        for j in subgraphs2:
            yyy += list(j)

        subgraphs1, subgraphs2 = xxx, yyy

        comm.Barrier()
        # print('Debugging')
        # print(type(subgraphs1))
        # print(subgraphs1)
            # print(list(subgraphs2[0].nodes))
    else:
        print('Pre-generate sub-graph')
        subgraphs1 = generate_subgraphs(O1, nodes1, windowsize, parallelization)
        subgraphs2 = generate_subgraphs(O2, nodes2, windowsize, parallelization)

    # root = set_True_root(O1, root_1)
    # subgraphs1 = np.zeros(len(nodes1), dtype=object)
    # for j in range(len(nodes1)):
    #     subgraphs1[j] = treeComp.subGraphGenerator(O1, nodes1[j], windowsize)
    #
    # subgraphs2 = np.zeros(len(nodes2), dtype=object)
    # for j in range(len(nodes2)):
    #     subgraphs2[j] = treeComp.subGraphGenerator(O2, nodes2[j], windowsize)

    # SEQUENTIAL MATRIX #
    print('generate sequential matrix')
    if os.path.isfile(path_to_doc + sequential_name):
        sequential = doc.import_csv(path_to_doc + sequential_name)
    else:
        # graph1, graph2, text_process = False, synonyms = False, word_list_to_clear1 = None,
        # word_list_to_clear2 = None, split_from1 = None, split_since1 = None, split_from2 = None, split_since2 = None
        sequential = gen_text_sequential_matrix(O1, O2, text_process, synonyms, onto1_list_clear, onto2_list_clear,
                                                split_from1, split_since1, split_from2, split_since2)
        if save_internals:
            # SAVING SEQUENTIAL #
            doc.save_csv(sequential, path_to_doc + sequential_name)

    # EQUIVALENT #
    print('Set equivalent nodes')
    # if topological T ~ +20 min
    # if not topological T ~
    if os.path.isfile(path_to_doc + equivalent_name):
        equivalent = doc.import_ods(path_to_doc + equivalent_name)
    else:
        if parallelization:
            equivalent = equivalent_dictionaryV4_parallelized(comm, O1, O2, sequential, globalthreshold, localthreshold
                                                              , subgraphs1,subgraphs2, windowsize=windowsize
                                                              , simtopo=topological_test
                                                              , constraint_threshold=constraint_threshold
                                                              , topological_cosine=topological_cosine
                                                              , topological_pearson=topological_pearson
                                                              , topological_euclidean=topological_euclidean
                                                              , topological_threshold=topological_threshold)
            comm.Barrier()
        else:
            equivalent = equivalent_dictionaryV4(O1, O2, sequential, globalthreshold, localthreshold, subgraphs1
                                                 , subgraphs2, windowsize=windowsize, simtopo=topological_test
                                                 , constraint_threshold=constraint_threshold
                                                 , topological_cosine=topological_cosine
                                                 , topological_pearson=topological_pearson
                                                 , topological_euclidean=topological_euclidean
                                                 , topological_threshold=topological_threshold)
        if save_internals_equiv:
            # SAVE EQUIVALENT #
            doc.save_ods(equivalent, path_to_doc + equivalent_name)
    if parallelization:
        rank = comm.Get_rank()
        print(rank)
        if rank == 0:
            onto1_path_clear = onto1_path[:-1]
            output_folder_clear = output_folder[:-1]
            # print(equivalent.__len__())
            # FUSING GRAPHS #
            print('fuse graphs')
            result, type_dict = fuse_graphs(O1, O2, equivalent, root=None)
            doc.save_ods(result, path_to_doc + result_name)
            # save_ods()
            if OBO_format_result and onto1_path is not None and onto1_path != '':
                if not secondary1:
                    print('DISCLAIMER: can not perform a OBO format: Ontology 1 input as not IDs')
                else:
                    obo.OBOFormat(result, doc.import_txt(onto1_path_clear), secondary1,
                              file_name=output_folder_clear + first_partA + '_' + first_partB)
            if draw_circular:
                circular_graphing(O1, 'ontology1_graph', directory=output_folder_clear, result=False, color='orange',  parallelization=parallelization)
                circular_graphing(O2, 'ontology2_graph', directory=output_folder_clear, result=False, color='lightskyblue', parallelization=parallelization)
                circular_graphing(result, 'fused_ontology_graph',  directory=output_folder_clear, parallelization=parallelization, g1=O1, equiv=type_dict)
                topo_state = set_topologicalstate(topological_test, topological_cosine, topological_pearson, topological_euclidean)

                create_HTML_w_results('ontology1_graph.html', 'ontology2_graph.html','fused_ontology_graph.html',
                                      name1, name2, equivalent, result, O1,  O2, topo_state, globalthreshold,
                                      localthreshold, constraint_threshold, topological_threshold, OBO_format_result,
                                      file_name_output=output_folder_clear, obo_name=first_partA + '_' + first_partB)
    else:
        # FUSING GRAPHS #
        print('fuse graphs')
        result, type_dict = fuse_graphs(O1, O2, equivalent, root=None)
        doc.save_ods(result, path_to_doc + result_name)
        # save_ods()
        print('Creating OBO resultant file, trees and html')
        if OBO_format_result and onto1_path is not None:
            obo.OBOFormat(result, doc.import_txt(onto1_path), secondary1, output_folder + first_partA + '_' + first_partB)
        if draw_circular:
            circular_graphing(O1, 'ontology1_graph', directory=output_folder, result=False, color='orange',
                              parallelization=parallelization)
            circular_graphing(O2, 'ontology2_graph', directory=output_folder, result=False, color='lightskyblue',
                              parallelization=parallelization)
            circular_graphing(result, 'fused_ontology_graph', directory=output_folder,
                              parallelization=parallelization, g1=O1, equiv=type_dict)
            topo_state = set_topologicalstate(topological_test, topological_cosine, topological_pearson,
                                              topological_euclidean)
            create_HTML_w_results('ontology1_graph.html', 'ontology2_graph.html', 'fused_ontology_graph.html', name1,
                                  name2, equivalent, result, O1, O2, topo_state, globalthreshold, localthreshold,
                                  constraint_threshold, topological_threshold, OBO_format_result,
                                  file_name_output=output_folder, obo_name=first_partA + '_' + first_partB)
    print('FOntCell end')
    return


def create_HTML_w_results(circle1, circle2, circlemixed, onto1name1, onto2name1, equivalent, result, graph1, graph2,
                          topo_state, sim_threshold, localthreshold, cons_threshold, topological_threshold, OBO,
                          file_name_output, obo_name):
    # todo: explicar los colores de los graphos grandes
    # Explicar porque no coinciden los nodos al sumar y los añadidos u.u

    # print(file_name_output + 'example')
    root_dir = os.path.dirname(os.path.realpath(__file__))
    current_path_img = root_dir + os.sep + 'fontcell_demo' + os.sep

    sequen, topolo, notmat, totals, edges_add, nodes_add, original_edges, original_nodes, nodesonto2_assigned,\
    sequen2, topolo2, notmat2 = quality_controls_V2(equivalent, result, graph1, graph2)

    nodesonto1 = len(list(graph1.nodes))
    nodesonto2 = len(list(graph2.nodes))
    edgesonto1 = len(list(graph1.edges))
    edgesonto2 = len(list(graph2.edges))

    onto1name = clean_onto_name(onto1name1)
    onto2name =clean_onto_name(onto2name1)
    style1 = h.add_style('', type='h', number=1, style='color: #000000;')
    style2 = h.add_style(style1, type='h', number=2, style='color: #ffffff;')
    style3 = h.add_style(style2, type='.block1', number='', style='background-color: #000099;')
    style4 = h.add_style(style3, type='.block2', number='', style='background-color: #000099;')
    styles = h.add_style(style4, type='h', number=3, style='color: #ffffff;')

    fig0 = h.insert_image(current_path_img + 'logo.png', width=150, height=150, align='left')
    heading = h.heading(fig0 + 'FOntCell <br> Fusion of ' + onto1name + ' and ' + onto2name, number=1)
    heading2 = h.add_box(h.heading('Interactive circular Directed Acyclic Graphs (DAGs) of (a) ' + onto1name
                                   + ', (b) ' + onto2name + ' and (c) Fused ontologies', number=2), type='block1')

    link1 = h.insert_link(file_name_output + circle1, '(a) DAG of ' + onto1name + ' ontology (nodes in orange)')
    link2 = h.insert_link(file_name_output + circle2, '(b) DAG of ' + onto2name + ' ontology (nodes in blue)')
    link3 = h.insert_link(file_name_output + circlemixed, '(c) DAG of the Fused ontology (nodes in orange (from '
                          + onto1name + '), blue(from '
                          + onto2name + '), red for topological match and green for sequential match)')

    line0 = h.paragraph('The ontology labels associated to the nodes appear when hovering over the nodes.')
    line1 = h.paragraph('Some nodes may appear overlapping.')

    first_part = heading + h.blankspace() + h.blankspace() + h.blankspace() + h.blankspace() + h.blankspace() + \
                 heading2 + link1 + h.blankspace() + link2 + h.blankspace() + link3 + h.blankspace() + line0 + line1

    heading3_1 = h.add_box(h.heading('Parameters of the FOntCell fusion algorithm', number=3), type='block2')
    line3_1_1 = ['Sequence similarity threshold &Theta;<sub>S</sub>: ' + str(sim_threshold)]
    line3_1_2 = ['Topology metric: ' + str(topo_state)]
    if topo_state != 'constraint':
        line3_1_3 = ['Sequence local similarity threshold &Theta;<sub>SL</sub>: '
                     + str(localthreshold)]
        line3_1_4 = ['Topological similarity threshold &Theta;<sub>T</sub>: '
                     + str(topological_threshold)]
        list3_1 = heading3_1 + h.htmllist(line3_1_1 + line3_1_2 + line3_1_3 + line3_1_4)
    else:
        line3_1_3 = ['constraint threshold &Theta;<sub>C</sub>: ' + str(cons_threshold)]
        list3_1 = heading3_1 + h.htmllist(line3_1_1 + line3_1_2 + line3_1_3)

    heading3_2 = h.add_box(h.heading('Statistics of the input ontologies', number=3), type='block2')
    line3_2_1 = ['Number of nodes of ' + onto1name + ' ontology: ' + str(nodesonto1)]
    line3_2_2 = ['Number of edges of ' + onto1name + ' ontology: ' + str(edgesonto1)]
    line3_2_3 = ['Number of nodes of ' + onto2name + ' ontology: ' + str(nodesonto2)]
    line3_2_4 = ['Number of edges of ' + onto2name + ' ontology: ' + str(edgesonto2)]
    list3_2 = heading3_2 + h.htmllist(line3_2_1 + line3_2_2 + line3_2_3 + line3_2_4)

    heading3_3 = h.add_box(h.heading('Statistics of the fused ontology', number=3), type='block2')
    heading3_3_1 = h.heading('Statistics of the fusion by sequence similarity', number=4)
    line3_3_1_1 = ['Number of nodes with equivalence found in ' + onto1name + ' by sequence similarity: ' + str(sequen)]
    line3_3_1_1_0 = ['Number of nodes with equivalence found in ' + onto2name + ' by sequence similarity: ' + str(sequen2)]
    line3_3_1_2 = ['Percentage of nodes (in relation to the number of nodes of ' \
                  + onto1name + ' ontology) added to '\
                  + onto1name + ' by sequence similarity: '\
                  + str("{0:.2f}".format(sequen / nodesonto1 * 100)) + '%']
    line3_3_1_2_0 = ['Percentage of nodes added to ' + onto2name + ' (in relation to the number of nodes of ' \
                     + onto2name + ' ontology) by sequence similarity: ' \
                     + str("{0:.2f}".format(sequen2 / nodesonto2 * 100)) + '%']

    list3_3_1 = heading3_3_1 + h.htmllist(line3_3_1_1 + line3_3_1_1_0 + line3_3_1_2 + line3_3_1_2_0)  # + line3_3_1_3 + line3_3_1_4)

    heading3_3_2 = h.heading('Statistics of the fusion by topological similarity', number=4)
    line3_3_2_1 = ['Number of nodes with equivalence found in ' + onto1name + ' by topological similarity: ' + str(topolo)]
    line3_3_2_1_0 = ['Number of nodes with equivalence found in ' + onto2name + ' by topological similarity: ' + str(topolo2)]
    line3_3_2_2 = ['Percentage of nodes added to ' \
                  + onto1name + ' (in relation to the number of nodes of '\
                  + onto1name + ' ontology) by topology similarity: '\
                  + str("{0:.2f}".format(topolo / nodesonto1 * 100)) + '%']
    line3_3_2_2_0 = ['Percentage of nodes added to ' + onto2name + ' (in relation to the number of nodes of ' \
                     + onto2name + ' ontology) by topology similarity: ' \
                     + str("{0:.2f}".format(topolo2 / nodesonto2 * 100)) + '%']

    list3_3_2 = heading3_3_2 + h.htmllist(line3_3_2_1 + line3_3_2_1_0 + line3_3_2_2 + line3_3_2_2_0)  # + line3_3_2_3 + line3_3_2_4)

    heading3_3_3 = h.heading('Statistics of the fusion of non-matched nodes', number=4)
    line3_3_3_1 = ['Number of nodes in ' + onto1name + ' non-matched in ' + onto2name + ': ' + str(notmat)]
    line3_3_3_2 = ['Percentage of nodes in '\
                  + onto1name + ' non-matched in '\
                  + onto2name + ' (in relation to the number of nodes of '\
                  + onto1name + ' ontology): ' + str("{0:.2f}".format(notmat / nodesonto1 * 100)) + '%']
    line3_3_3_3 = ['Number of nodes in ' + onto2name + ' non-matched in ' + onto1name + ': ' + str(nodesonto2 - (sequen2 + topolo2))]

    line3_3_3_4 = ['Percentage of nodes in '\
                  + onto2name + ' non-matched in '\
                  + onto1name + ' (in relation to the number of nodes of ' \
                  + onto2name + ' ontology): '\
                  + str("{0:.2f}".format((nodesonto2 - (sequen2 + topolo2)) / nodesonto2 * 100)) + '%']
    list3_3_3 = heading3_3_3 + h.htmllist(line3_3_3_1 + line3_3_3_2 + line3_3_3_3 + line3_3_3_4)

    heading3_3_4 = h.heading('Statistics of the fusion by sequence and topological similarity', number=4)
    line3_3_4_1 = ['Number of nodes added in total (by sequence similarity and by topological similarity): ' + str(nodes_add)]
    line3_3_4_2 = ['Percentage of nodes added in total (by sequence similarity and by topological similarity): ' \
                  + str("{0:.2f}".format(nodes_add / nodesonto1 * 100)) + '%']
    line3_3_4_3 = ['Number of edges added in total (by sequence similarity and by topological similarity): ' + str(edges_add)]
    line3_3_4_4 = ['Percentage of edges added in total (by sequence similarity and by topological similarity): ' \
                  + str("{0:.2f}".format(edges_add / edgesonto1 * 100)) + '%']
    line_3_3_4_5 = h.paragraph('Added nodes refers to the descendants nodes founded on the synonyms')
    list3_3_4 = heading3_3_4 + h.htmllist(line3_3_4_1 + line3_3_4_2 + line3_3_4_3 + line3_3_4_4) + line_3_3_4_5

    second_part = list3_1 + list3_2 + heading3_3 + list3_3_1 + list3_3_2 + list3_3_3 + list3_3_4 + h.blankspace()

    if OBO:
        header_for_OBO = h.add_box(h.heading('Fused ontology in OBO format', number=3), type='block2')
        line_for_OBO = h.paragraph('Fused ontology from ' + onto1name + ' and ' + onto2name + ': ')
        link4 = header_for_OBO + line_for_OBO + h.insert_link(file_name_output + obo_name + '.owl', 'here')
    else:
        link4 = ''

    heading4 = h.add_box(h.heading('Results on the fused ontology', number=2), type='block1')
    line4_1 = h.heading('Percentages of contribution of nodes to the fused ontology in relation to the nodes of each contributant ontology', number=4)
    line4_2 = h.heading('Euler-Venn diagram of the nodes of ' + onto1name + ' and ' + onto2name + ' fusion', number=4)

    # Donut text

    # ontology1
    donut_ontology1_title = h.heading('Outter: Numbers and percentages of ' + onto1name, number=5)
    donut_1 = ['Blue: Nodes with sequential equivalence: ' + str(sequen) + ', percentage: ' + str(round((sequen/nodesonto1)*100, 2))]
    donut_2 = ['Green: Nodes with topological equivalence: ' + str(topolo) + ', percentage: ' + str(round((topolo/nodesonto1)*100, 2))]
    donut_3 = ['Orange: Non-matched nodes: ' + str(nodesonto1 - sequen - topolo) + ', percentage: ' + str(round((((nodesonto1 - sequen - topolo)/nodesonto1)*100), 2))]
    # ontology2
    donut_ontology2_title = h.heading('Inner: NUmbers and percentages of ' + onto2name, number=5)
    donut_4 = ['Blue: Nodes with sequential equivalence: ' + str(sequen2) + ', percentage: ' + str(round((sequen2/nodesonto2)*100, 2))]
    donut_5 = ['Green: Nodes with topological equivalence: ' + str(topolo2) + ', percentage: ' + str(round((topolo2/nodesonto2)*100, 2))]
    donut_6 = ['Orange: Non-matched nodes: ' + str(nodesonto2 - sequen2 - topolo2) + ', percentage: ' + str(round((((nodesonto2 - sequen2 - topolo2)/nodesonto2)*100), 2))]

    # Venn text
    venn_1 = ['Nodes from ' + onto1name + ': ' + str(nodesonto1) + ' (blue)']
    venn_2 = ['Nodes from ' + onto2name + ': ' + str(nodesonto2) + ' (green)']
    venn_3 = ['Synonyms found in ' + onto1name + ': ' + str(topolo + sequen) + ' (Blue-green)']
    venn_4 = ['Resulted ontology nodes: ' + onto1name + ' nodes: ' + str(nodesonto1) + ' + added nodes: ' + str(nodes_add)]

    pre_donut = line4_1 + donut_ontology1_title + h.htmllist(donut_1 + donut_2 + donut_3) + donut_ontology2_title\
                + h.htmllist(donut_4 + donut_5 + donut_6)

    pre_venn = line4_2 + h.htmllist(venn_1 + venn_2 + venn_3 + venn_4)

    make.make_relatedfigures(graph1, graph2, onto1name, onto2name, sequen, topolo, notmat, nodes_add, nodesonto1,
                             sequen2, topolo2, notmat2, donut_name=file_name_output + 'donut_diagram.png',
                             square_name=file_name_output + 'fusion_square_plot.png', donut=True, squares=True)


    fig1 = h.align(h.insert_image(file_name_output + 'donut_diagram.png', width=640, height=480), 'left')



    fig2 = h.insert_image(file_name_output + 'fusion_square_plot.png', width=640, height=480)

    third_part = link4 + heading4 + pre_donut + fig1 + pre_venn + fig2

    line5 = h.add_box(h.heading('Additional results', number=2), type='block1')
    line5_1 = h.paragraph('Files with results on  detection of synonyms, graph expansion and sequence similarity matrix '
                          ' are available at: ' + root_dir + os.sep + 'fontcell_files' + os.sep)

    forth_part = line5 + line5_1

    body = h.body(first_part + second_part + third_part + forth_part)

    full_html = h.html(styles + body)

    doc.save_txt(full_html, file_name_output + 'FOntCell_' + onto1name + '_' + onto2name + '.html')

    return


def set_topologicalstate(simtopo, topological_cosine, topological_pearson, topological_euclidean):
    if not simtopo:
        topologicalstate = 'constraint'
    else:
        if topological_cosine:
            topologicalstate = 'cosine'
        elif topological_pearson:
            topologicalstate = 'Pearson'
        elif topological_euclidean:
            topologicalstate = 'euclidean'
        else:
            topologicalstate = 'Blondel'
    return topologicalstate


def clean_onto_name(name):
    listed_name = list(name)
    new_name = ''.join(list(filter(lambda a: a.isalpha(), listed_name)))
    return new_name
