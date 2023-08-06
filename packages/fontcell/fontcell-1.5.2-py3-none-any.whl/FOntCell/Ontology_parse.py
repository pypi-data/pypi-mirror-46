#######################################################################################################################
                                                # Import Libraries #
#######################################################################################################################
from . import doc_managing as doc

import numpy as np
from itertools import chain
import os.path

#######################################################################################################################
                                                    # Functions #
#######################################################################################################################


def splited(soup, t=False):
    x = list(chain(*list(map(lambda a:a.split('<'), soup.split('\n')))))

    y = list(chain(*list(map(lambda a:a.split('>'), x))))

    if t:
        var = list(chain(*list(map(lambda a:a.split(':'), y))))
    if not t:
        var = y

    final = list(map(lambda a:a.split(' '), var))
    return final


def splitlist(list, key):
    for i in range(len(list)):
        list[i] = list[i].split(key)
    return list


def search_ontology_name(ontology_splited):
    '''
    Find the 'name' of the ontology.
    '''
    names = []
    for i in range(ontology_splited.__len__()):
        if ontology_splited[i][0] == '!--':
            try:
                variable = ontology_splited[i][1].split('_')[0]
                name = str(variable.split('/')[-1]) + '_'
                try:
                    name = str(name.split('#')[1])
                    names.append(name)
                except:
                    names.append(name)
            except:
                continue

    repetitions = {}
    for j in range(len(names)):
        if names[j] not in repetitions:
            repetitions[names[j]] = 1
        elif names[j] in repetitions:
            value = repetitions[names[j]]
            repetitions[names[j]] = value + 1

    current_value = 0
    for key, value in repetitions.items():
        if value > current_value:
            current_value = value
            ontologyname = key

    return ontologyname


def parse_ontology(file, take_synonyms=True, filter_by_keywords=None, ontologyName=None,
                   synonym_type=('owlNCBITaxon:synonym'), label_type= ('CELDA:commonName xml:lang="en"', 'CELDA:commonName', 'rdfs:label'),
                   relative_type=('owl:someValuesFrom'), input_folder=None, output_folder=None):
    # read the ontology and generate a full splited ontology
    # for organism filter is needed the name give as argument present in the ontology labels.
    #First name at: recover[i][0][0]
    if isinstance(synonym_type, str):
        synonym_type1 = [synonym_type]
    elif isinstance(synonym_type, tuple):
        synonym_type1 = list(synonym_type)
    elif isinstance(synonym_type, list):
        synonym_type1 = synonym_type
    else:
        raise ValueError('synonym_type not valid')

    if isinstance(label_type, str):
        label_type1 = [label_type]
    elif isinstance(label_type, tuple):
        label_type1 = list(label_type)
    elif isinstance(label_type, list):
        label_type1 = label_type
    else:
        raise ValueError('label_type not valid')

    if isinstance(relative_type, str):
        relative_type1 = [relative_type]
    elif isinstance(relative_type, tuple):
        relative_type1 = list(relative_type)
    elif isinstance(relative_type, list):
        relative_type1 = relative_type
    else:
        raise ValueError('relative_type not valid')

    with open(file, 'r') as f:
        soup = f.read()

    final_soup = splited(soup)

    recover = []
    clase = False
    for i in range(len(final_soup)):
        # print(i)
        if final_soup[i][0] == 'owl:Class':
            clase = True
            if take_synonyms:
                label = []
            ancest = []
            j = 0
            #labeled = False
            # print('class find at i: ' + str(i))

        while clase:
            # print(' ', j)
            # if i == 9516 and j == 59:
            # print()
            if i + j + 1 > len(final_soup):
                break
            # print('current i + j: ' + str(i+j))
            if final_soup[i + j][0] in relative_type1 and len(final_soup[i + j]) > 1:
                if str(final_soup[i + j][1]) != '':
                    ancest.append(final_soup[i + j][1])

            if final_soup[i + j][0] in label_type1: #and not labeled:
                if str(final_soup[i + j + 1]) != '':
                    if take_synonyms:
                        label.append(final_soup[i + j + 1])
                    else:
                        label = final_soup[i + j + 1]
                    #labeled = True
            if final_soup[i + j][0] in synonym_type1 and take_synonyms:
                if str(final_soup[i + j + 1]) != '':
                    label.append(final_soup[i + j + 1])

            if final_soup[i + j][0] == '/owl:Class':
                if label != '':
                    recover.append([label, ancest])
                    j = 0
                    label = ''
                    clase = False
                else:
                    j = 0
                    clase = False

            else:
                j = j + 1

    for i in range(len(recover)):
        for j in range(len(recover[i][0])):
            recover[i][0][j] = ' '.join(recover[i][0][j])
        try:
            # Remove 'rdf:resource='
            ascn = splitlist(recover[i][1], 'rdf:resource=')
            #ascn1 = list(map(lambda a:a.split('rdf:resource='), recover[i]))
            aux_list = []
            for j in range(len(ascn)):
                aux_list.append(ascn[j][1])
            ascn = aux_list
            # recover[i][1] = ascn

            # Remove '"'
            aux_list = []
            ascn = splitlist(ascn, '"')
            #ascn2 = list(map(lambda a:a.split('"'), ascn1))
            for k in range(len(ascn)):
                aux_list.append(ascn[k][1])
            ascn = aux_list
            # recover[i][1] = ascn

            # Remove '#' if there're
            for n in range(len(ascn)):
                try:
                    ascn[n] = ascn[n].split('#')[1]
                except:
                    ascn[n] = ascn[n]
            recover[i][1] = ascn

        except:
            recover[i][1] = recover[i][1]

        # print(recover[i])
    # print(len(recover))

    # Post processing: from list of list to a single sort list.
    final = np.zeros(len(recover), dtype=object)

    for i in range(len(recover)):
        auxiliar = [recover[i][0]]
        for k in range(len(recover[i][1])):
            auxiliar.append(recover[i][1][k])
        final[i] = auxiliar

    # print('Ontology parsed')
    if ontologyName == None:
        name = search_ontology_name(final_soup)
    else:
        name = ontologyName

    final = clearing_ascendants(final, name)
    # Check if a dictionary of IDs_label exist
    # return final
    # r_path = os.path.dirname(os.path.realpath(__file__))
    path_to_doc = output_folder
    # print(path_to_doc)
    if not os.path.exists(path_to_doc + name + 'Dictionary_IDS.ods'):
        print('Making ID\'s dictionary')
        IDs1 = makedictionary_ofIDs_onlyCurrentOntology(final_soup, name)
        doc.save_ods(IDs1, path_to_doc + name + 'Dictionary_IDS.ods')
        IDs = doc.import_ods(path_to_doc + name + 'Dictionary_IDS.ods', 'pyexcel sheet')
        IDs = parse_import_odsDict(IDs)
    else:
        try:
            print('Importing ID\'s dictionary')
            IDs = doc.import_ods(path_to_doc + name + 'Dictionary_IDS.ods', 'pyexcel sheet')
            IDs = parse_import_odsDict(IDs)
        except:
            print('Making ID\'s dictionary')
            IDs = makedictionary_ofIDs_onlyCurrentOntology(final_soup, name)
            doc.save_ods(IDs, path_to_doc + name + 'Dictionary_IDS.ods')

    # print('Setting ascendants labels')
    ontology = ID_to_label(final, IDs)
    # return ontology
    # print('Setting ascendant-descendant relation.')
    ontology_sorted = set_parent_son_relations(ontology)

    # set all .lower()
    for i in range(len(ontology_sorted)):
        if len(ontology_sorted[i]) == 1:
            ontology_sorted[i][0][0] = list(map(lambda a: a.lower(), ontology_sorted[i][0][0]))
        elif len(ontology_sorted[i]) == 2:
            ontology_sorted[i][0][0] = list(map(lambda a: a.lower(), ontology_sorted[i][0][0]))
            ontology_sorted[i][1][0] = list(map(lambda a: a.lower(), ontology_sorted[i][1][0]))
    # return ontology_sorted

    # return ontology_sorted
    if filter_by_keywords is not None:
        filter_by_keywords1 = list(filter_by_keywords)
        ontology_sorted = filter_bykeywords(ontology_sorted, filter_by_keywords1)
    # if filter_humanMouse:
    #      ontology_sorted = filter_human_mouse(ontology_sorted)
    # # return ontology_sorted
    return ontology_sorted, name


def parse_import_odsDict(IDs):
    '''
    Parse the definitions format to set a list format instead of a 'str' format.
    '''
    new_IDs = np.zeros((len(IDs), 2), dtype=object)
    for i in range(len(new_IDs)):
        new_IDs[i][0] = IDs[i][0]
        # parse and delete '[' and ']'
        new_IDs[i][1] = IDs[i][1].split('\'')[1:-1]
        # delete ','
        new_IDs[i][1] = list(filter(lambda a: a != ', ', new_IDs[i][1]))
    return new_IDs


def makedictionary_ofIDs_onlyCurrentOntology(splited_ontology, ontology_name):
    # Only takes names for our current ontology at the IDs dictionary
    clase = False
    dictionary = []
    for i in range(len(splited_ontology)):
        if splited_ontology[i][0] == 'owl:Class':
            clase = True
            label = []
            ID = ''
            # j = 0
            # print('class find at i: ' + str(i))

        while clase:
            try:
                ID = ontology_name + splited_ontology[i][1].split(ontology_name)[1]
                ID = ID.split('"')[0]
                ID_onto = True
            except:
                clase = False
                ID_onto = False

            if ID_onto:
                fully_labeled = False
                j = 0
                while not fully_labeled:
                    if splited_ontology[i + j][0] == 'rdfs:label':
                        if str(splited_ontology[i + j + 1]) != '':
                            label.append(splited_ontology[i + j + 1])
                    if splited_ontology[i + j][0] == 'CELDA:commonName xml:lang="en"' or splited_ontology[i + j][0] == 'CELDA:commonName':
                        if str(splited_ontology[i + j + 1]) != '':
                            label.append(splited_ontology[i + j + 1])
                    if splited_ontology[i + j][0] == 'owlNCBITaxon:synonym':
                        if str(splited_ontology[i + j + 1]) != '':
                            label.append(splited_ontology[i + j + 1])
                    if splited_ontology[i + j][0] == '/owl:Class':
                        clase = False
                        ID_onto = False
                        fully_labeled = True
                        dictionary.append([ID, label])
                    j += 1

    for i in range(len(dictionary)):
        for j in range(len(dictionary[i][1])):
            aux = ''
            for k in range(len(dictionary[i][1][j])):
                aux = aux + ' ' + dictionary[i][1][j][k]
            dictionary[i][1][j] = aux.strip()

    return dictionary


def ID_to_label(onto_raw, dictionary):
    final = np.zeros(len(onto_raw), dtype=object)
    a = dictionary[:,0]
    b = dictionary[:,1]
    celda_Ids = list(a)
    id_names = list(b)

    for i in range(len(onto_raw)):
        current =  []
        for j in range(len(onto_raw[i])):
            # Add ID
            if onto_raw[i][j] in id_names:
                current.append([onto_raw[i][0], celda_Ids[id_names.index(onto_raw[i][j])]])
            # Add name
            if onto_raw[i][j] in celda_Ids:
                current.append([id_names[celda_Ids.index(onto_raw[i][j])], onto_raw[i][j]])
        final[i]=current
    return final


def clearing_ascendants(raw_ontology, name):
    for i in range(len(raw_ontology)):
        for j in range(len(raw_ontology[i])):
            if j > 0:
                try:
                    raw_ontology[i][j] = name + raw_ontology[i][j].split(name)[1]
                except:
                    continue
    return raw_ontology


def set_parent_son_relations(ascendant_relations):
    ascendant_relations1 = ascendant_relations.tolist()
    new_relation = []

    for i in range(len(ascendant_relations1)):
        if len(ascendant_relations1[i]) == 1:
            pass
        elif len(ascendant_relations1[i]) == 2:
            ascendant_relations1[i] = [ascendant_relations1[i][1],ascendant_relations1[i][0]]
        else:
            take = False
            for j in range(len(ascendant_relations1[i])):
                if j == 1 and j != 0:
                    to_substitute = [ascendant_relations1[i][j],ascendant_relations1[i][0]]
                    take = True
                elif j != 0 and j != 1:
                    new_relation.append([ascendant_relations1[i][j], ascendant_relations1[i][0]])
            if take:
                ascendant_relations1[i] = to_substitute
    final = ascendant_relations1 + new_relation
    return final

    new_relation = []
    for i in range(len(ascendant_relations)):
        if len(ascendant_relations[i]) == 1:
            pass
        else:
            for j in range(len(ascendant_relations[i][1])):
                if not [ascendant_relations[i][1], ascendant_relations[i][0]] in new_relation:
                    new_relation.append([ascendant_relations[i][1], ascendant_relations[i][0]])
    return new_relation


def editGraph(ontology, file, output_file=None, ontoName=None):
    '''
    This tool create this 'ideal graph' for CELDA ontology (mouse or human).
    :param ontology: ontology filtered for human or mouse
    :param file: file path to a .txt with the info for modifying
        Code:
        'label'                 --> deletes the class that contains this label
        [[class1], [class2]]    --> add new relations between classes
        ID:'ID_number'          --> delete the classes with this ID
        f[[class1], [class2]]   --> Fuse two classes

    :return: an Ideal graph
    '''
    # Read the file

    for_clear, to_add, IDs_todelete, to_fuse, new_node = readFC(file)

    # Delete non clear cell types (or without relevant information about cell types, better say duplications) which
    # they are adams or they are in adam's graphs.Delete those nodes that has a very long character string.
    for i in range(len(ontology)):
        if not ontology[i]:
            continue
        if ontology[i][0][1] in IDs_todelete and ontology[i] == []:
            ontology[i] = []
            continue
        # father
        sentence = list(chain(*list(map(lambda a:a.split(), ontology[i][0][0]))))
        if 'derived' in sentence or not plausible_celltype(sentence):
            for k in range(len(ontology[i][0][0])):
                for_clear.append(ontology[i][0][0][k])
        # son
        if ontology[i].__len__() > 1:
            if ontology[i][1][1] in IDs_todelete:
                ontology[i] = []
                continue
            sentence = list(chain(*list(map(lambda a:a.split(), ontology[i][1][0]))))
            if 'derived' in sentence or not plausible_celltype(sentence):
                for k in range(len(ontology[i][1][0])):
                    for_clear.append(ontology[i][1][0][k])

    ontology_cleared = []

    for i in range(ontology.__len__()):
        if not ontology[i]:
            continue
        father = ontology[i][0][0]
        if ontology[i].__len__() > 1:
            son = ontology[i][1][0]
        else:
            son = []

        if len(set(father).intersection(for_clear)) == 0 and len(set(son).intersection(for_clear)) == 0:
            ontology_cleared.append(ontology[i])
    # add new_nodes

    for i in range(len(new_node)):
        ontology_cleared.append(new_node[i])

    # Create new relations

    full_ontology = np.zeros([(ontology_cleared.__len__() + to_add.__len__()), 2], dtype=object)

    for k in range(ontology_cleared.__len__()):
        full_ontology[k] = ontology_cleared[k]
    for n in range(to_add.__len__()):
        full_ontology[ontology_cleared.__len__()+n] = to_add[n]

    # Fuse classes:
    full_ontology = list(full_ontology)
    for i in range(len(to_fuse)):
        current = to_fuse[i][0] + to_fuse[i][1]
        for j in range(len(full_ontology)):
            if full_ontology[j][0][0] == to_fuse[i][0] or full_ontology[j][0][0] == to_fuse[i][1]:
                full_ontology[j][0][0] = current
            if full_ontology[j][1][0] == to_fuse[i][0] or full_ontology[j][1][0] == to_fuse[i][1]:
                full_ontology[j][1][0] = current
    # Clearing for re-compensate the ontology modified (deleting repetitions and autoassignations), delete loops too
    full_ontology = clear_ontology(full_ontology)
    # save_ods(full_ontology, '///home/ra/Documentos/testing_folder_output/test_celda.ods')

    # final check
    set_adams(full_ontology, output_file, ontoName)

    return full_ontology


def set_adams(ontology, outfolder, name):
    '''
    for 'Adam' we understand a root node, a node with no father. The ideal, in a biological cell type context, graph or
    simulation only has one root node.
    Whit this tool you can see whats are the adams in your graph for clear them (adding it to some branch or clear them
    if they don't have relevant information)
    '''
    adams = []
    for i in range(len(ontology)):
        sit = False
        for j in range(len(ontology)):
            descen = ontology[j][1:]
            if ontology[i][0] in descen:
                sit = True
            else:
                continue
        if not sit and ontology[i][0] not in adams:
            adams.append(ontology[i][0])
    if len(adams) > 1:
        print('More than one plausible root')
        # print(adams)
        f = open(outfolder + os.sep + name + '_plausibles_roots.txt', 'w')
        for i in range(len(adams)):
            f.write(str(adams[i]) + '\n')
        print('Data save as "plausibles_roots.txt" at output folder')
        o = open(outfolder + os.sep + name + '_ontology_with_various_roots.txt', 'w')
        for i in range(len(ontology)):
            o.write(str(ontology[i]) + '\n')
        print('Created adittional document at output folder with the ontology parsed named as: '
              '"ontology_with_various_roots.txt"')
        o.close()
        f.close()
    return


def clear_ontology(ontology):

    # Clear autoassignations
    no_rep = np.zeros((ontology.__len__(),2),dtype=object)
    for i in range(len(ontology)):
        if ontology[i].__len__()>1:
            if ontology[i][0] != ontology[i][1]:
                no_rep[i][0] = ontology[i][0]
                no_rep[i][1] = ontology[i][1]
        else:
            no_rep[i][0] = ontology[i][0]

    cleared =  []
    for i in range(len(no_rep)):
        if no_rep[i][0] != 0 and no_rep[i][1] != 0:
            row = [no_rep[i][0], no_rep[i][1]]
            cleared.append(row)
        elif no_rep[i][0] != 0 and no_rep[i][1] == 0:
            row = no_rep[i][0]
            cleared.append(row)
        else:
            continue

    # Clear double assignations
    final_cleared= []
    deleted = []
    for i in range(len(cleared)):
        repeat = False
        count = 0
        for j in range(len(cleared)):
            if cleared[i] == cleared[j] and cleared[j] not in deleted:
                if count == 1:
                    repeat = True
                    deleted.append(cleared[j])
                    break
                else:
                     count = 1
        if not repeat:
            final_cleared.append(cleared[i])

    # clear loops


    return final_cleared


def plausible_celltype(list_of_string):
    celltype = False
    for i in range(len(list_of_string)):
        try:
            test = list_of_string[i].split('cyte')
            celltype = True
            break
        except:
            celltype = False
        try:
            test = list_of_string[i].split('blast')
            celltype = True
            break
        except:
            celltype = False
    return celltype


def readFC(file_path):
    '''
    From a txt, takes the 'to delete' and the 'to add' to the final ontology graph.
    :return: to delete, to add
    '''
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    to_delete = []
    to_add =[]
    IDs = []
    to_fuse = []
    new_node = []
    for i in range(lines.__len__()):
        if lines[i][0] == '[':
            to_add.append(eval(lines[i]))
        elif lines[i][0] == '\'':
            to_delete.append(eval(lines[i]))
        elif lines[i][0] == 'I':
            IDs.append(eval(lines[i][3:]))
        elif lines[i][0] == 'f':
            to_fuse.append(eval(lines[i][1:]))
        elif lines[i][0] == 'n':
            new_node.append(eval(lines[i][1:]))
    return to_delete, to_add, IDs, to_fuse, new_node


def parseSubClass_onto(final_soup, name, path):
    '''
    From a ontology with owl format, take the classes and they subclasses has a edge-like structure
    :param final_soup: oa splitted and computed ontology
    :return: edge-like structure
    '''
    lpath = path.split(os.sep)[:-1]
    path=''
    for i in range(len(lpath)):
        if i > 0:
            path = path + os.sep + lpath[i]
    recover = []
    clase = False
    for i in range(len(final_soup)):
        # print(i)
        if final_soup[i][0] == 'owl:Class':
            clase = True
            label = ''
            ancest = []
            j = 0
            # labeled = False
            # print('class find at i: ' + str(i))

        while clase:
            # print(' ', j)
            # if i == 9516 and j == 59:
            # print()
            if i + j + 1 > len(final_soup):
                break
            # print('current i + j: ' + str(i+j))
            if final_soup[i + j][0] == 'rdfs:subClassOf' and len(final_soup[i + j]) > 1:
                if str(final_soup[i + j][1]) != '':
                    ancest.append(final_soup[i + j][1])

            if final_soup[i + j][0] == 'rdfs:label':  # and not labeled:
                if str(final_soup[i + j + 1]) != '':
                    label = final_soup[i + j + 1]
                    # labeled = True

            if final_soup[i + j][0] == '/owl:Class':
                if label != '':
                    recover.append([label, ancest])
                    j = 0
                    label = ''
                    clase = False
                else:
                    j = 0
                    clase = False

            else:
                j = j + 1

    for i in range(len(recover)):
        aux = ''
        for k in range(len(recover[i][0])):
            if k > 0:
                aux = aux + ' ' + recover[i][0][k]
            else:
                aux = recover[i][0][k]
        recover[i][0] = aux

        try:
            # Remove 'rdf:resource='
            ascn = splitlist(recover[i][1], 'rdf:resource=')
            aux_list = []
            for j in range(len(ascn)):
                aux_list.append(ascn[j][1])
            ascn = aux_list
            # recover[i][1] = ascn

            # Remove '"'
            aux_list = []
            ascn = splitlist(ascn, '"')
            for k in range(len(ascn)):
                aux_list.append(ascn[k][1])
            ascn = aux_list
            # recover[i][1] = ascn

            # Remove '#' if there're
            for n in range(len(ascn)):
                try:
                    ascn[n] = ascn[n].split('#')[1]
                except:
                    ascn[n] = ascn[n]
            recover[i][1] = ascn

        except:
            recover[i][1] = recover[i][1]

        # print(recover[i])
    # print(len(recover))

    # Post processing: from list of list to a single sort list.
    final = np.zeros(len(recover), dtype=object)

    for i in range(len(recover)):
        auxiliar = []
        auxiliar.append(recover[i][0])
        for k in range(len(recover[i][1])):
            auxiliar.append(recover[i][1][k])
        final[i] = auxiliar
    # print('Ontology parsed')
    # name = search_ontology_name(final_soup)

    final = clearing_ascendants(final, name)
    # Check if a dictionary of IDs_label exist

    IDs = makedictionary_ofIDs_onlyCurrentOntology(final_soup, name)
    doc.save_ods(IDs, path + name + 'Dictionary_IDS.ods')

    # print('Setting ascendants labels')

    ontology1 = ID_to_label(final, IDs)

    # print('Setting ascendant-descendant relation.')
    ontology_sorted = set_parent_son_relations(ontology1)

    return ontology_sorted


def evaluate_toadds(clearedontology, toadd):
    '''
    Tool for change the names of toadd to a clearedontology format
    '''
    all_types = np.zeros([clearedontology.__len__() * 2],dtype=object)
    number = 0
    while number+1 <= all_types.__len__():
        print(number)
        all_types[number] = clearedontology[int(number//2)][0]
        all_types[number+1] = clearedontology[int(number/2)][1]
        number += 2
    all_types = np.unique(all_types)

    for i in range(len(toadd)):
        for j in range(len(all_types)):
            if toadd[i][0] in all_types[j]:
                toadd[i][0] = all_types[j]
            if toadd[i][1] in all_types[j]:
                toadd[i][1] = all_types[j]
    return toadd


def filter_human_mouse(ontology):
    # filter human or mouse nodes
    filter_ontology = []
    for i in range(len(ontology)):
        event = False
        event1 = False
        if len(ontology[i]) >= 1:
            if ontology[i][0][0].__len__() == 1:
                words = list(chain(*list(map(lambda a: a.split(), ontology[i][0][0]))))
                if 'human' in words or 'mouse' in words:
                    ontology[i][0][0] = [' '.join(list(map(lambda a: a.split(), ontology[i][0][0]))[0][1:])]
                    event = True
                    event1 = True
                if ontology[i].__len__() >1:
                    words = list(chain(*list(map(lambda a: a.split(), ontology[i][1][0]))))
                    if 'human' in words or 'mouse' in words:
                        ontology[i][1][0] = [' '.join(list(map(lambda a: a.split(), ontology[i][1][0]))[0][1:])]
                        event = True
                        event1 = True
            else:
                words = list(chain(*list(map(lambda a: a.split(), ontology[i][0][0]))))
                #for j in range(len(words)):
                if 'human' in words or 'mouse' in words:
                    event = True
        if event and not event1:
            # delete 'human' or 'mouse' labeled synonyms and make .unique() to synonyms and to a 'class_list'
            synonyms = []

            if len(ontology[i]) == 1:
                for j in range(len(ontology[i][0][0])):
                    if 'human' not in ontology[i][0][0][j] and 'mouse' not in ontology[i][0][0][j]:
                        synonyms.append(ontology[i][0][0][j])
                ontology[i][0][0] = synonyms

            # if we found descendants
            if len(ontology[i]) > 1:
                synonyms= []
                for j in range(len(ontology[i][0][0])):
                    if 'human' not in ontology[i][0][0][j] and 'mouse' not in ontology[i][0][0][j]:
                        synonyms.append(ontology[i][0][0][j])
                if not synonyms:
                    ontology[i][0][0] = [' '.join(list(map(lambda a: a.split(), ontology[i][0][0]))[0][1:])]
                else:
                    ontology[i][0][0] = synonyms
                synonyms = []
                # son
                for k in range(len(ontology[i][1][0])):
                    if 'human' not in ontology[i][1][0][k] and 'mouse' not in ontology[i][1][0][k]:
                        synonyms.append(ontology[i][1][0][k])
                if not synonyms:
                    ontology[i][1][0] = [' '.join(list(map(lambda a: a.split(), ontology[i][1][0]))[0][1:])]
                else:
                    ontology[i][1][0] = synonyms

            # delete empty cells if there're
            if not synonyms:
                pass
            else:

                filter_ontology.append(ontology[i])
                # print(i, ontology[i])
        elif event and event1:
            filter_ontology.append(ontology[i])
            # print(i, ontology[i])
    return filter_ontology


def filter_bykeywords(ontology, words_for_filter):
    # filter human or mouse nodes
    filter_ontology = []
    words_set = set(words_for_filter)
    for i in range(len(ontology)):
        event = False
        event1 = False
        if len(ontology[i]) >= 1:
            if ontology[i][0][0].__len__() == 1:
                words = list(chain(*list(map(lambda a: a.split(), ontology[i][0][0]))))
                if words_set.intersection(words).__len__() > 0:
                    ontology[i][0][0] = [' '.join(list(map(lambda a: a.split(), ontology[i][0][0]))[0][1:])]
                    event = True
                    event1 = True
                if ontology[i].__len__() >1:
                    words = set(chain(*list(map(lambda a: a.split(), ontology[i][1][0]))))
                    if words_set.intersection(words).__len__() > 0:
                        ontology[i][1][0] = [' '.join(list(map(lambda a: a.split(), ontology[i][1][0]))[0][1:])]
                        event = True
                        event1 = True
            else:
                words = list(chain(*list(map(lambda a: a.split(), ontology[i][0][0]))))
                #for j in range(len(words)):
                if words_set.intersection(words).__len__() > 0:
                    event = True
        if event and not event1:
            # delete word_set labeled synonyms and make '.unique()' to synonyms and to a 'class_list'
            synonyms = []

            if len(ontology[i]) == 1:
                for j in range(len(ontology[i][0][0])):
                    if words_set.intersection(ontology[i][0][0][j].split()).__len__() == 0:
                        synonyms.append(ontology[i][0][0][j])
                ontology[i][0][0] = synonyms

            # if we found descendants
            if len(ontology[i]) > 1:
                synonyms = []
                for j in range(len(ontology[i][0][0])):
                    if words_set.intersection(ontology[i][0][0][j].split()).__len__() == 0:
                        synonyms.append(ontology[i][0][0][j])
                if not synonyms:
                    ontology[i][0][0] = [' '.join(list(map(lambda a: a.split(), ontology[i][0][0]))[0][1:])]
                else:
                    ontology[i][0][0] = synonyms
                synonyms = []
                # son
                for k in range(len(ontology[i][1][0])):
                    if words_set.intersection(ontology[i][1][0][k].split()).__len__() == 0:
                        synonyms.append(ontology[i][1][0][k])
                if not synonyms:
                    ontology[i][1][0] = [' '.join(list(map(lambda a: a.split(), ontology[i][1][0]))[0][1:])]
                else:
                    ontology[i][1][0] = synonyms

            # delete empty nodes if there're
            if not synonyms:
                pass
            else:

                filter_ontology.append(ontology[i])
                # print(i, ontology[i])
        elif event and event1:
            filter_ontology.append(ontology[i])
            # print(i, ontology[i])
    return filter_ontology
