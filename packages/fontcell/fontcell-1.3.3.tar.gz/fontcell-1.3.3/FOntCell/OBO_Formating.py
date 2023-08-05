'''
From the fusion resulted 'ontology' create a .txt with the new classes added in OBO format. CELDA fingerprint
'''

#############################
#         Libraries         #
#############################
from . import doc_managing as doc

import numpy as np
#############################
#         FUNCTIONS         #
#############################


def OBOFormat(resulted_ontology, old_ontology, IDs_dictionary, file_name='ontology_fused'):
    '''
    Main function to run the
    '''
    # We have to set [ID, label, synonyms, father]

    # Split ontology in two slice to put in the middle the new classes
    splitting_site = old_ontology.index('    // Classes\n') + 5
    old_ontology1 = old_ontology[:splitting_site]
    old_ontology2 = old_ontology[splitting_site:]

    # Create a dictionary from IDs_dictionary and a list of IDs to set the max id number
    id_list = []
    dictionary_of_IDs = {}
    IDs_dictionary_listed = list(IDs_dictionary)
    for i in range(len(IDs_dictionary_listed)):
        label =IDs_dictionary_listed[i]
        id = IDs_dictionary[IDs_dictionary_listed[i]]
        id_list.append(int(id.split('_')[1]))
        dictionary_of_IDs.update({label:id})
    main_ID = 'Fused#' + id.split('_')[0] + '_'
    number_characters = len(id.split('_')[1])
    max_ID = max(id_list)

    # Order nodes to son-father set
    edge = list(np.zeros([len(resulted_ontology), 2], dtype=object))

    for i in range(len(edge)):
        edge[i] = [eval(resulted_ontology[i][1]), eval(resulted_ontology[i][0])]

    dict_nodes_S_to_F = {}
    for k, v in edge:
        dict_nodes_S_to_F.setdefault(k, []).append(v)

    # split into new and old nodes
    old_nodes = []
    new_nodes = []
    for i in range(len(resulted_ontology)):
        if resulted_ontology[i][2] == 'new':
            if eval(resulted_ontology[i][0]) not in new_nodes and eval(resulted_ontology[i][0]) not in old_nodes:
                new_nodes.append(eval(resulted_ontology[i][0]))
            if eval(resulted_ontology[i][1]) not in new_nodes and eval(resulted_ontology[i][1]) not in old_nodes:
                new_nodes.append(eval(resulted_ontology[i][1]))
        else:
            if eval(resulted_ontology[i][0]) not in old_nodes:
                old_nodes.append(eval(resulted_ontology[i][0]))
            if eval(resulted_ontology[i][1]) not in old_nodes:
                old_nodes.append(eval(resulted_ontology[i][1]))
    # print()

    # Set IDs to the new nodes (in a dictionary) updating: dictionary_of_IDs
    for i in range(len(new_nodes)):
        # generate the new ID
        max_ID += 1
        current_ID = main_ID + setID_format(max_ID, number_characters)
        dictionary_of_IDs.update({new_nodes[i]:current_ID})

    # Build an array for these new nodes [ID, label, synonyms, father]

    for i in range(len(new_nodes)):
        # Take the label
        current_label = new_nodes[i][0]
        # Perform synonymous list
        current_synonyms = new_nodes[i][1:]
        if current_synonyms.__len__() == 0:
            current_synonyms = None
        # take father
        if new_nodes[i] in dict_nodes_S_to_F:
            current_father = list(map(lambda a: dictionary_of_IDs[a], dict_nodes_S_to_F[new_nodes[i]]))
            if current_father.__len__() == 0:
                current_father = None
        else:
            current_father = None
        #take ID
        current_ID = dictionary_of_IDs[new_nodes[i]]

        # TheArray[i] = [current_ID, current_label, current_synonyms, current_father]

        current_class = write_class(current_ID, current_label, current_synonyms, current_father)
        for i in range(len(current_class)):
            old_ontology1.append(current_class[i])

    ontology_formated = old_ontology1 + old_ontology2
    named_as = file_name + '.owl'
    doc.save_txt(ontology_formated, named_as)

    return


def write_class(ID, label, synonyms=None, father=None):
    '''
    write a class oin OBO format (inspired by CELDA ontology)
    :param ID: str ID of class
    :param label: str class label
    :param synonyms: list synonyms
    :param father: str ID of class father
    :return: a formated class
    '''

    if synonyms != None and father != None:

        all_fathers = ''
        for i in range(len(father)):
            all_fathers= all_fathers + father[i]

        new_class = ['\n',
                     '\n',
                     '\n',
                     '     <!--#' + ID + '-->\n',
                     '\n',
                     '     <owl:Class rdf:about="#' + ID +'">\n',
                     '         <rdfs:label>'+ label + '</rdfs:label>\n',
                     '         <rdfs:subClassOf>\n',
                     '         <owl:Restriction>\n',
                     '             <owl:onProperty rdf:resource="&purl;obo/develops_from"/>\n',
                     '             <owl:someValuesFrom rdf:resource="' + all_fathers + '"/>\n',
                     '         </owl:Restriction>\n']
        # loop for synonyms
        for i in range(len(synonyms)):
            new_class.append('         <ru-meta:synonym xml:lang="en">' + synonyms[i] + '</ru-meta:synonym>\n')

        new_class.append('        </rdfs:subClassOf>\n')
        new_class.append('     </owl:Class>\n')


    elif synonyms != None and father == None:
        new_class = ['\n',
                     '\n',
                     '\n',
                     '    <!--#' + ID + '-->\n',
                     '\n',
                     '    <owl:Class rdf:about="#' + ID + '">\n',
                     '        <rdfs:label>' + label + '</rdfs:label>\n']
        # loop for synonyms
        for i in range(len(synonyms)):
            new_class.append('        <ru-meta:synonym xml:lang="en">' + synonyms[i] + '</ru-meta:synonym>\n')
        new_class.append('    </owl:Class>\n')

    elif synonyms == None and father != None:

        all_fathers = ''
        for i in range(len(father)):
            all_fathers = all_fathers + father[i]

        new_class = ['\n',
                     '\n',
                     '\n',
                     '    <!--#' + ID + '-->\n',
                     '\n',
                     '    <owl:Class rdf:about="#' + ID + '">\n',
                     '        <rdfs:label>' + label + '</rdfs:label>\n',
                     '        <rdfs:subClassOf >\n',
                     '        <owl:Restriction>\n',
                     '            <owl:onProperty rdf:resource="&purl;obo/develops_from"/>\n',
                     '            <owl:someValuesFrom rdf:resource="' + all_fathers + '"/>\n',
                     '        </owl:Restriction>\n',
                     '        </rdfs:subClassOf>\n',
                     '    </owl:Class>\n']

    else:
        new_class = ['\n',
                     '\n',
                     '\n',
                     '    <!--#' + ID + '-->\n',
                     '\n',
                     '    <owl:Class rdf:about="#' + ID + '">\n',
                     '        <rdfs:label>' + label + '</rdfs:label>\n',
                     '    </owl:Class>\n']

    return new_class


def setID_format(number, characters_len):
    '''
    Generates a str ready to attach to the 'main core' of the ID
    :param number: int of the ID
    :param characters_len: number of characters that the 'int part' of the ID has to be
    :return: 'int part' of the ID
    '''
    id = ''
    for i in range(characters_len - len(str(number))):
        id = id + '0'
    id_to = id + str(number)
    return id_to
