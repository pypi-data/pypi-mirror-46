#######################################################################################################################
                                                ### LIBRARIES ###
#######################################################################################################################
import networkx as nx
import numpy as np
import stringdist as sd
from collections import OrderedDict
from scipy import spatial, stats

#######################################################################################################################
                                                ### FUNCTIONS ###
#######################################################################################################################


def similarity(string1, string2):
    if isinstance(string1, list) or isinstance(string1, np.ndarray):
        string1 = string1[0]
    if isinstance(string2, list) or isinstance(string2, np.ndarray):
        string2 = string2[0]

    distance = sd.levenshtein(string1, string2)
    maximum_len = max_len(string1, string2)
    similarity = (1 - (distance / maximum_len))
    return similarity


def similarity_synonyms(list1, list2):
    '''
    take the similarity index from a two list of synonyms
    '''
    current_index = 0.0

    for i in range(len(list1)):
        index = max(list(map(lambda a:similarity(a, list1[i]), list2)))
        if index > current_index:
            current_index = index
    return current_index


def max_len(string1, string2):
    if(len(string1) >= len(string2)):
        return len(string1)
    else:
        return len(string2)


def adjacent(graph):
    '''Calculate the adjacent matrix'''
    adjacent_matrix = np.zeros((graph.number_of_nodes(), graph.number_of_nodes()), dtype=int)

    e = numerate_nodes_in_edge(graph)
    edge = []
    for i in range(e.__len__()):
        edge.append((e[i][0], e[i][1]))

    for k in range(edge.__len__()):
       x = edge[k][0]-1
       y = edge[k][1]-1
       adjacent_matrix[x][y] = 1
    #print('adjacent matrix calculated')
    return adjacent_matrix


def numerate_nodes_in_edge(graph):
    '''
    :param graph: A networkx graph
    :return: the list of edges change label for number
    '''
    # print()
    try:
        edges = list(graph.edges)
        # print('TESTING')
    except:
        edges = graph

    used = []
    dictionary = {}
    x = 0
    # make a dictionary
    for i in range(edges.__len__()):
        for j in range(len(edges[i])):
            if edges[i][j] not in used:
                x = x + 1
                used.append(edges[i][j])
                dictionary.update({edges[i][j]: x})

    final_edges = []
    # make numerate edge
    for i in range(edges.__len__()):
        aux = (dictionary[edges[i][0]], dictionary[edges[i][1]])
        final_edges.append(aux)

    return final_edges


def g_similarity(G1, G2, convergence_threshold=0.0001, obtain_loops_number=False):
    '''
        Calculate the similarity between two graphs, return a similarity matrix(shape = G2.nodes x G1.nodes)
        This function works with graphs created through networkx library
        Code exemple for creating graphs:

        >> import networkx as nx
        >> import Tree_com as tc

        >> human = tc.import_ods(filedir1, sheet)
        >> H = nx.DiGraph()

        >> nodesH = tc.establish_node_list(human)
        >> Hedge = tc.numerate_nodes(human)
        >> H.add_edges_from(Hedge)

        Matrix shape:
            G1,     G1,     G1
        G2 value, value, value
        G2 value, value, value
        G2 value, value, value
        G2 value, value, value
    '''
    # Obtain Adjacent's matrix
    B = adjacent(G2)
    A = adjacent(G1)

    # Obtain Transpose matrix
    A_t = A.transpose()
    B_t = B.transpose()

    # Set a nodes iterable object
    nodes1 = list(G1.nodes)
    nodes2 = list(G2.nodes)

    # Similarity Algorithm
    Z = np.ones([nodes2.__len__(), nodes1.__len__()], dtype=float)
    i = 0
    Z_1 = Z
    # conver =[]
    C = 1
    event = True

    while C > convergence_threshold and event:
        i = i + 1
        # this solution takes a lot of time
        #Z = (np.matmul(np.matmul(B, Z), A_t) + np.matmul(np.matmul(B_t, Z), A)) / (np.linalg.norm((np.matmul(np.matmul(B, Z), A_t) + np.matmul(np.matmul(B_t, Z), A)), ord='fro'))

        n1 = np.matmul(B, Z)
        n2 = np.matmul(B_t, Z)
        num = np.matmul(n1, A_t) + np.matmul(n2, A)
        den = np.linalg.norm(num, ord='fro')
        Z = num / den

        if i % 2 == 0:
            C = np.linalg.norm(Z - Z_1)
            Z_1 = Z
            # conver.append(C)
        else:
            continue
        # Threshold too low, don't loop infinite times
        if i >= 1000:
            # print('too low threshold')
            # if print_convergence_graph:
            #     print('Showing convergence graph')
            #
            #     ko = np.zeros(conver.__len__()-1, dtype=int)
            #
            #     for k in range(ko.__len__()):
            #         ko[k] = k
            #     plt.plot(ko, conver[1:], 'o-')
            #     plt.show()
            event = False
    # print(i)
    if obtain_loops_number:
        return i
    else:
        return Z[0][0]


def g_similarity_noniterative(G1, G2, cosine, euclidean, pearson):
    '''
    Calculates the similarity between two graphs using cosine distance metrics
    :param G1: graph 1
    :param G2: graph 2
    :return: topological distance [0-1]
    '''
    # Obtain Adjacent's matrix
    A = adjacent(G1)[0]
    B = adjacent(G2)[0]
    # set the bigger and the smaller
    better_similarity = 0.0
    if A.__len__() >= B.__len__():
        # case: A>B
        loopings = A.__len__() - B.__len__() + 1
        if cosine:
            for j in range(loopings):
                current_similarity = 1 - spatial.distance.cosine(A[j:j+len(B)], B)
                if current_similarity > better_similarity:
                    better_similarity = current_similarity
        elif euclidean:
            for j in range(loopings):
                current_similarity = 0 - spatial.distance.euclidean(A[j:j + len(B)], B)
                if current_similarity > better_similarity:
                    better_similarity = current_similarity
        elif pearson:
            for j in range(loopings):
                current_similarity = stats.pearsonr(A[j:j + len(B)], B)[0]
                if current_similarity > better_similarity:
                    better_similarity = current_similarity
    else:
        # case B>A
        loopings = B.__len__() - A.__len__() + 1
        if cosine:
            for j in range(loopings):
                current_similarity = 1 - spatial.distance.cosine(A, B[j:j+len(A)])
                if current_similarity > better_similarity:
                    better_similarity = current_similarity
        if euclidean:
            for j in range(loopings):
                current_similarity = 0 - spatial.distance.euclidean(A, B[j:j + len(A)])
                if current_similarity > better_similarity:
                    better_similarity = current_similarity
        if pearson:
            for j in range(loopings):
                current_similarity = stats.pearsonr(A, B[j:j + len(A)])[0]
                if current_similarity > better_similarity:
                    better_similarity = current_similarity

    return better_similarity


def g_constraint_similarity(graph1, graphs2, node1_problem, nodes2_problem, sequential_dictionary, window, threshold=0.0):
    '''

    :param graphs1:
    :param graphs2:
    :param nodes1_problem:
    :param sequential_dictionary:
    :param window:
    :return:
    '''
    old_current = 0.0
    match = None
    for j in range(len(graphs2)):
        current = g_constraint_analysis(node1_problem, graph1, graphs2[j], sequential_dictionary, window)
        if current > old_current and current >= threshold:
            old_current = current
            match = nodes2_problem[j]
    return match, old_current


def g_constraint_analysis(node_problem1, graph1, graph2, sequential_dictionary, window):
    '''
    for graph1 and graph2 takes the assignations and give the value of constraint of each graphs
    '''
    nodes1 = list(graph1.nodes)
    nodes2 = list(graph2.nodes)
    nodes_with_equivalences = []
    for i in range(len(nodes1)):
        if nodes1[i] in sequential_dictionary:
            if sequential_dictionary[nodes1[i]] in nodes2:
                nodes_with_equivalences.append(nodes1[i])
            else:
                continue

    constraint = ponderation_stimation(node_problem1, nodes_with_equivalences, graph1, window) #/float(len(nodes1))

    return constraint


def ponderation_stimation(node_problem, equivalent_nodes, graph1, window):
    '''
    This function add the ponderation value to a graph
    '''

    # ponderation = window_weighting(window)
    ponderation_value = 0.0
    g = graph1.to_undirected()
    for i in range(len(equivalent_nodes)):
        try:
            value = len((nx.shortest_path(g, source=node_problem, target=equivalent_nodes[i])))-1
        except:
            value = len((nx.shortest_path(g, source=equivalent_nodes[i], target=node_problem)))-1
        if value != 0:
            ponderation_value = ponderation_value + (window + 1 + value)

    return ponderation_value


def window_weighting(window):
    '''
    :param window: window size
    :return: dictionary of ponderations
    '''
    dict_pond = {}
    ponderations = np.zeros([window, 1], dtype=object)
    for i in range(window+1):
        if i > 0:
            ponderations[-i] = (float(i))/10.0
    for j in range(len(ponderations)):
        dict_pond.update({j+1: ponderations[j]})
    # pond = set(ponderations)
    # return pond
    return dict_pond


def node_father(node, ontology):
    '''
    Function for search the fathernode from a node.
    :param node: node problem
    :param ontology: a relational ontology
    :return: The node father.
    '''

    for i in range(len(ontology)):
        if node in ontology[i]:
            return ontology[i][0]
        else:
            continue


def set_edges_nodes(ontology):
    '''
    with a 'ontology' we set the edges and nodes for a graphicate
    :param ontology: a document with relations of paternity: [father, son1, son2, son3] [father 2, son1, son2...] ...
    :return: 2D array with Father-son and , nodes list
    '''
    edges = []
    for i in range(ontology.__len__()):
        for j in range(ontology[i].__len__()):
            if j > 0:
                edges.append((str(ontology[i][0]), str(ontology[i][j])))
    nodes = np.zeros(ontology.__len__(), dtype=object)
    for i in range(len(ontology)):
        nodes[i] = str(ontology[i][0])

    return edges, nodes


def rootTree(graph):
    '''
    Get the graph's root.
    '''
    root = ''
    token = 0
    edges = np.array(graph.edges)
    descend = np.zeros(edges.__len__(),dtype=object)
    tokenized = []
    for i in range(len(edges)):
        descend[i] = edges[i][1]
    for j in range(len(edges)):
        if edges[j][0] not in descend and edges[j][0] not in tokenized:
            root = edges[j][0]
            token += 1
            tokenized.append(edges[j][0])
    if token == 0:
        print('not found root (cicle)')
        return
    elif token >= 2:
        print('multiple root, get the last founded')
    # print(tokenized)
    return root


def buildDiGraph(descendants_relation):
    '''
    :param descendants_relation: a matrix with: [[father1, son1, son2, ...], [father2, son1, son2], ...] the numbers of
    sons of every father doesn't matter
    :return: a DiGraph object built by networkx.
    '''
    G = nx.DiGraph()
    Gedges, Gnodes = set_edges_nodes(descendants_relation)
    # print(Gedges.__len__())
    # for i in range(Gnodes.__len__()):
    #     G.add_node(Gnodes[i])

    G.add_edges_from(Gedges)
    # print('Gnodes', G.nodes.__len__())
    return G


def takecolumn(array, column):
    '''
    :param array: a iterable array
    :return: the selected column as a list
    '''
    column_as_list = list(map(lambda a: a[:][column], array))

    for i in range(len(column_as_list)):
        try:
            column_as_list[i] = tuple(column_as_list[i])
        except:
            pass

    return column_as_list


def clearOntology_labels(ontology_labels, word_list_to_clear, synonyms=False, split_from=None, split_since=None):
    '''
    A Tool for clearing the ontology labels in order to improve the sequential match
    :param ontology_labels: list of ontology classes labels
    :param word_list_to_clear: a list of words to clear from ontology
    :param synonyms: if the 'ontology labels' is a single label or a group of labels (Synonyms)
    :param split_from: a list of words to split the labels. We take the second slice
    :param split_since: a list of words to split the labels. We take the first slice
    :return: a treated ontology_labels (in same order)
    '''
    # pre-treatment
    # ontology_labels1 = list(map(lambda a:eval(a), ontology_labels))
    ontology_labels1 = ontology_labels

    if synonyms:
        for i in range(len(ontology_labels1)):
            for j in range(len(word_list_to_clear)):
                ontology_labels1[i] = list(map(lambda a:' '.join(a.replace(word_list_to_clear[j], '').split()), ontology_labels1[i]))

                if split_from != None:
                    for k in range(len(split_from)):
                        ontology_labels1[i] = list(map(lambda a:a.split(split_from[k])[1], ontology_labels1[i]))
                if split_since != None:
                    for n in range(len(split_since)):
                        ontology_labels1[i] = list(map(lambda a:a.split(split_since[n])[0], ontology_labels1[i]))

    if not synonyms:
        for j in range(len(word_list_to_clear)):
            ontology_labels1 = list(map(lambda a:' '.join(a.replace(word_list_to_clear[j], '').split()), ontology_labels1))

        if split_from != None:
            for k in range(len(split_from)):
                ontology_labels1 = list(map(lambda a: a.split(split_from[k])[1], ontology_labels1))
        if split_since != None:
            for n in range(len(split_since)):
                ontology_labels1 = list(map(lambda a: a.split(split_since[n])[0], ontology_labels1))

    return ontology_labels1


def subGraphGenerator(G, node, windowsize):
    '''
    :param G: networkx Graph
    :param node: node 'x' the center of the subgraph
    :param windowsize: must be integer (windowsize % 2 = 0)
    :return: a subgraph from Graph %G, with siez of %windowsize with a central node %node.
    '''

    # taking edges and nodes for the new subgraph
    S = nx.DiGraph()
    edges = []
    nodes = [[node]]
    node_problem = node
    nodes_visited = []

    edge_list = np.array(G.edges()).tolist()
    for i in range(len(edge_list)):
        edge_list[i] = list(map(lambda a:eval(a), edge_list[i]))


    # FIRST USE
    new_nodes = []
    new_edges = []
    # Edges
    for i in range(len(edge_list)):
        if node_problem in edge_list[i]:
            new_edges.append(edge_list[i])

    # Nodes
    for i in range(len(new_edges)):
        if new_edges[i][0] not in new_nodes:
            new_nodes.append(new_edges[i][0])
        if new_edges[i][1] not in nodes:
            new_nodes.append(new_edges[i][1])

    node_problem = new_nodes

    nodes.append(new_nodes)
    edges.append(new_edges)

    nodes_visited.append(node_problem)

    #Loop

    i = 1
    if windowsize > 1:
        while i <= windowsize:
            # Searching on each node:
            for j in range(len(node_problem)):
                new_nodes = []
                new_edges = []

                # Edges
                for k in range(len(edge_list)):
                    for t in range(len(node_problem)):
                        if node_problem[t] in edge_list[k]:
                            new_edges.append(edge_list[k])

                # Nodes
                for k in range(len(new_edges)):
                    if new_edges[k][0] not in new_nodes:
                        new_nodes.append(new_edges[k][0])
                    if new_edges[k][1] not in new_nodes:
                        new_nodes.append(new_edges[k][1])

            nodes.append(new_nodes)
            edges.append(new_edges)

            # Control and re-loop setting
            nodes_visited.append(node_problem)
            for n in range(len(nodes)):
                if nodes[n] not in nodes_visited:
                    node_problem = nodes[n]
                    break
                else:
                    continue

            i += 1

    # Make readable nodes and edges

    node_listed = []
    edge_listed = []
    for i in range(len(nodes)):
        for j in range(len(nodes[i])):
            if nodes[i][j] not in node_listed:
                node_listed.append(nodes[i][j])

    for i in range(len(edges)):
        for j in range(len(edges[i])):
                edge_listed.append(edges[i][j])


    # print('node_listed ', node_listed)
    final_nodes = list(map(lambda a: tuple(a), node_listed))
    final_edges = []
    for i in range(len(edge_listed)):
        final_edges.append(list(map(lambda a:tuple(a), edge_listed[i])))
    S.add_nodes_from(final_nodes)
    S.add_edges_from(final_edges)

    return S


def readOntologyparsed(ontology):
    '''
    :param ontology: the input from a .ods
    :return: the ontology computed
    '''
    for i in range(len(ontology)):
        ontology[i] = list(map(lambda a: eval(a), ontology[i]))

    return ontology


def makeDigraph_fromOntology(ontology, fuse_classes=False, restriction=False, split_secondary_info=True):
    '''
    :param ontology: input from a .ods parse ontology
    :param fuse_classes: fuse the classes from an ontology which has the same 'first synonym' equal
    :param restriction: True if we want only fuse those classes with equal secondary info
    :return: a related graph object to the ontology, and a list of secondary info
    '''
    if len(ontology[0]) > 2:
        ontology1 = list(map(lambda a: a[0:2], ontology))
        print('DISCLAIMER: using a fused-graph has a result, Info related to Ontology ID will not be added')
        graph =buildDiGraph(ontology1)
        return graph, []

    elif ontology[0][0][0] == '[':
        ontology1 = readOntologyparsed(ontology)
    else:
        ontology1 = ontology

    if fuse_classes:
        secondary, ontology3 = fuseClasses(ontology1, restriction)
        ontology4 = list(ontology3)
    elif split_secondary_info:
        secondary, ontology4 = splitSecondaryInfo(ontology1)
    else:
        ontology4 = np.zeros([len(ontology1), 2], dtype=object)
        for i in range(len(ontology1)):
            ontology4[i][0]=eval(ontology1[i][0])
            ontology4[i][1]=eval(ontology1[i][1])
        # ontology4 = ontology1
        secondary = []
        graph = buildDiGraph(list(ontology4))
        return graph, secondary
    for i in range(len(ontology4)):
        if ontology4[i][1] == 0:
            ontology4[i] = [tuple(ontology4[i][0])]
        else:
            ontology4[i] = [tuple(ontology4[i][0]), tuple(ontology4[i][1])]
    graph = buildDiGraph(ontology4)
    return graph, secondary


def splitSecondaryInfo(ontology):
    '''
    take the 'secondary info' in a set and take the 'principal info'(synonyms) at a list of lists
    '''

    info = {}
    new_ontology = np.zeros([len(ontology), 2], dtype=object)
    for i in range(len(ontology)):
        # father
        father = ontology[i][0][0] # Interest in that variable
        info.update({tuple(father):ontology[i][0][1]})
        # son
        if ontology[i].__len__() == 2:
            son = ontology[i][1][0]
            info.update({tuple(son):ontology[i][1][1]})

            new_ontology[i][1]=son
        new_ontology[i][0] = father
    new_ontology = list(new_ontology)

    return info, new_ontology


def fuseClasses(ontology, restriction):
    '''
    This function fuse the classes from an ontology which has the same 'first synonym' equal.
    :param ontology: [[synonyms1]], [[synonyms2]]
    :param restriction: True if we want only fuse those classes with equal secondary info
    :return: [[synonyms1, synonyms2]]
    '''
    new_ontology = np.zeros([ontology.__len__(), 2], dtype=object)
    # first_synonyms = np.zeros([ontology.__len__(), 2], dtype=object)
    father_synonyms = np.zeros([ontology.__len__(), 1], dtype=object)
    son_synonyms = np.zeros([ontology.__len__(), 1], dtype=object)
    for j in range(len(ontology)):
        # first_synonyms[j][0] = ontology[j][0][0][0]
        father_synonyms[j] = ontology[j][0][0][0]
        # first_synonyms[j][1] = ontology[j][1][0][0]
        if ontology[j].__len__() == 2:
            son_synonyms[j] = ontology[j][1][0][0]
        else:
            son_synonyms[j] = []
    info = {}
    for i in range(len(ontology)):
        father = ontology[i][0][0]
        # check all the occurrences of the 1st synonyms == 1st synonyms (possible classes to fuse)
        ocurrences_ff = list(map(lambda a:father_synonyms[i] in a, father_synonyms))
        indexes_ff = [k for k, x in enumerate(ocurrences_ff) if x]

        ocurrences_sf = list(map(lambda a: father_synonyms[i] in a, son_synonyms))
        indexes_sf = [k for k, x in enumerate(ocurrences_sf) if x == True]

        indexes_father = indexes_ff + indexes_sf

        son = ontology[i][1][0]
        # check all the occurrences of the 1st synonyms == 1st synonyms (possible classes to fuse)
        ocurrences_fs = list(map(lambda a: son_synonyms[i] in a, father_synonyms))
        indexes_fs = [k for k, x in enumerate(ocurrences_fs) if x == True]

        ocurrences_ss = list(map(lambda a: son_synonyms[i] in a, son_synonyms))
        indexes_ss = [k for k, x in enumerate(ocurrences_ss) if x == True]

        indexes_son = indexes_fs + indexes_ss
        # Check the conditions and fuse
        # > Father
        for j in range(len(indexes_father)):
            if ontology[i][0] != ontology[indexes_father[j]][0]:
                # check restriction
                if restriction:
                    if ontology[i][0][1] == ontology[indexes_father[j]][0][1]:
                        father = father + ontology[indexes_father[j]][0][0]
                elif not restriction:
                    father = father + ontology[indexes_father[j]][0][0]

        father_to_attach = list(OrderedDict.fromkeys(father))
        if tuple(father_to_attach) not in info:
            info.update({tuple(father_to_attach): ontology[i][0][1]})
        new_ontology[i][0] = father_to_attach

        # > Son
        for j in range(len(indexes_son)):
            if ontology[i][1] != ontology[indexes_son[j]][0]:
                # check restriction
                if restriction:
                    if ontology[i][1][1] == ontology[indexes_son[j]][0][1]:
                        son = son + ontology[indexes_son[j]][0][0]
                elif not restriction:
                    son = son + ontology[indexes_son[j]][0][0]

        son_to_attach = list(OrderedDict.fromkeys(son))
        if tuple(son_to_attach) not in info:
            info.update({tuple(son_to_attach): ontology[i][1][1]})
        new_ontology[i][1] = son_to_attach

        # print(i)

    return info, new_ontology
