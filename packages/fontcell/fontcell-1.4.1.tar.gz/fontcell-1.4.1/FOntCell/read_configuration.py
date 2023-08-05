
import os.path


def control_inputs_numerical(variable, limitup, limitdown, variable_name):
    if isinstance(variable, float):
        if variable > limitup:
            raise ValueError(variable_name + 'exceed the up limit of' + str(limitup))
        if variable < limitdown:
            raise ValueError(variable_name + 'exceed the down limit of' + str(limitup))
    elif isinstance(variable, int):
        if variable > limitup:
            raise ValueError(variable_name + 'exceed the up limit of' + str(limitup))
        if variable < limitdown:
            raise ValueError(variable_name + 'exceed the down limit of' + str(limitup))
    else:
        raise ValueError(variable_name + 'must be numerical')
    return


def checktuples(check_current):
    current = check_current[1].split(',')
    if current.__len__() == 1:
        result_check = [eval(current[0])]
    else:
        result_check = list(map(lambda a: eval(a), current))
    tuple_check = tuple(result_check)
    return tuple_check


def establish_topological(topological):
    topological = eval(topological)
    if topological == 'blondel' or topological == 'Blondel':
        topological_test = True
        topological_cosine = False
        topological_pearson = False
        topological_euclidean = False
    elif topological == 'constraint' or topological == 'constraint':
        topological_test = False
        topological_cosine = False
        topological_pearson = False
        topological_euclidean = False
    elif topological == 'cosine' or topological == 'Cosine':
        topological_test = True
        topological_cosine = True
        topological_pearson = False
        topological_euclidean = False
    elif topological == 'pearson' or topological == 'Pearson':
        topological_test = True
        topological_cosine = False
        topological_pearson = True
        topological_euclidean = False
    elif topological == 'euclidean' or topological == 'Euclidean':
        topological_test = True
        topological_cosine = False
        topological_pearson = False
        topological_euclidean = True
    else:
        raise ValueError("topological_similarity must be: 'blondel','constraint', 'cosine', 'pearson' or 'euclidean'")
    return topological_test, topological_cosine, topological_pearson, topological_euclidean


def parse_and_check(current_value, line, variable_str, data_type, data_type_str, special_parse=None, up_lim=None,
                    down_lim=None):
    if special_parse is None:
        if line[0][1:] == variable_str and line[1] != '\n':
            new_variable = eval(line[1])
            if not isinstance(new_variable, data_type) and new_variable is not None:
                raise ValueError(variable_str + ' must be ' + data_type_str)
            return new_variable
        else:
            return current_value
    else:
        if special_parse == 'tuple':
            if line[0][1:] == variable_str and line[1] != '\n':
                new_variable = checktuples(line)
                return new_variable
            else:
                return current_value
        elif special_parse == 'numerical':
            if line[0][1:] == variable_str and line[1] != '\n':
                new_variable = eval(line[1])
                control_inputs_numerical(new_variable, up_lim, down_lim, variable_str)
                return new_variable
            else:
                return current_value
        else:
            return current_value


def read_conf(path_to_config, demo):
    # set default values:
    input_folder = ''
    output_folder = ''
    parallelization = False
    proc = 1
    # # Ontology_parse
    parse_ontology1 = True
    parse_ontology2 = True
    # # # Ontology 1
    file1 = None
    file_clean_ontology1 = ''
    take_synonyms1 = True
    filter_by_keywords1 = None
    ontologyname1 = None
    synonym_type1 = tuple(['owlNCBITaxon:synonym'])
    label_type1 = tuple(['rdfs:label'])
    relative_type1 = tuple(['owl:someValuesFrom'])

    ontology1_file = ''
    ontology1_name = ''

    # # # Ontology 2
    file2 = None
    file_clean_ontology2 = ''
    take_synonyms2 = True
    filter_by_keywords2 = None
    ontologyname2 = None
    synonym_type2 = tuple(['owlNCBITaxon:synonym'])
    label_type2 = tuple(['rdfs:label'])
    relative_type2 = tuple(['owl:someValuesFrom'])

    ontology2_file = ''
    ontology2_name = ''

    # # ontology_fusion
    onto1_fuseclasses = True
    onto2_fuseclasses = True
    onto1_restriction = False
    onto2_restriction = False
    onto1_list_clear = None
    onto2_list_clear = None
    synonyms = False
    text_process = False
    split_from1 = None
    split_since1 = None
    split_from2 = None
    split_since2 = None
    windowsize = 4
    globalthreshold = 0.85
    localthreshold = 0.7
    topological_test = True
    constraint_threshold = 0.0
    topological_cosine = False
    topological_pearson = False
    topological_euclidean = False
    topological_threshold = 0.0

    # read the txt

    if demo:
        root_dir = os.path.dirname(os.path.realpath(__file__))
        project_demo_path = root_dir + os.sep + 'fontcell_demo'
        input_folder = project_demo_path + os.sep
        output_folder = project_demo_path + os.sep + 'results' + os.sep

    with open(path_to_config) as f:
        lines = f.readlines()
        f.close()
    for i in range(len(lines)):
        if lines[i][0] == '>':
            current = lines[i].split('=', 1)
            # set default values:
            if not demo:
                input_folder = parse_and_check(input_folder, current, 'input_folder', str, 'string')
                output_folder = parse_and_check(output_folder, current, 'output_folder', str, 'string')
            parallelization = parse_and_check(parallelization, current, 'parallelization', bool, 'boolean')
            proc = parse_and_check(proc, current, 'proc', int, 'integer')

            # # Ontology_parse
            parse_ontology1 = parse_and_check(parse_ontology1, current, 'parse_ontology1', bool, 'boolean')
            parse_ontology2 = parse_and_check(parse_ontology2, current, 'parse_ontology2', bool, 'boolean')

            # # # Ontology 1
            if parse_ontology1:
                file1 = parse_and_check(file1, current, 'file1', str, 'string')
                file_clean_ontology1 = parse_and_check(file_clean_ontology1, current, 'file_clean_ontology1', str,
                                                       'string')
                take_synonyms1 = parse_and_check(take_synonyms1, current, 'take_synonyms1', bool, 'boolean')
                filter_by_keywords1 = parse_and_check(filter_by_keywords1, current, 'filter_by_keywords1', '', '',
                                                      special_parse='tuple')
                ontologyname1 = parse_and_check(ontologyname1, current, 'ontologyname1', str, 'string')
                synonym_type1 = parse_and_check(synonym_type1, current, 'synonym_type1', '', '', special_parse='tuple')
                label_type1 = parse_and_check(label_type1, current, 'label_type1', '', '', special_parse='tuple')
                relative_type1 = parse_and_check(relative_type1, current, 'relative_type1', '', '',
                                                 special_parse='tuple')
            elif not parse_ontology1:
                ontology1_file = parse_and_check(ontology1_file, current, 'ontology1_file', str, 'string')
                ontology1_name = parse_and_check(ontology1_name, current, 'ontology1_name', str, 'string')

            # # # Ontology 2
            if parse_ontology2:
                file2 = parse_and_check(file2, current, 'file2', str, 'string')
                file_clean_ontology2 = parse_and_check(file_clean_ontology2, current, 'file_clean_ontology2',
                                                       str, 'string')
                take_synonyms2 = parse_and_check(take_synonyms2, current, 'take_synonyms2', bool, 'boolean')
                filter_by_keywords2 = parse_and_check(filter_by_keywords2, current, 'filter_by_keywords2', '', '',
                                                      special_parse='tuple')
                ontologyname2 = parse_and_check(ontologyname2, current, 'ontologyname2', str, 'string')
                synonym_type2 = parse_and_check(synonym_type2, current, 'synonym_type2', '', '', special_parse='tuple')
                label_type2 = parse_and_check(label_type2, current, 'label_type2', '', '', special_parse='tuple')
                relative_type2 = parse_and_check(relative_type2, current, 'relative_type2', '', '',
                                                 special_parse='tuple')
            elif not parse_ontology2:
                ontology2_file = parse_and_check(ontology2_file, current, 'ontology2_file', str, 'string')
                ontology2_name = parse_and_check(ontology2_name, current, 'ontology2_name', str, 'string')

            # # ontology_fusion
            onto1_fuseclasses = parse_and_check(onto1_fuseclasses, current, 'onto1_fuseclasses', bool, 'boolean')
            onto2_fuseclasses = parse_and_check(onto2_fuseclasses, current, 'onto2_fuseclasses', bool, 'boolean')
            onto1_restriction = parse_and_check(onto1_restriction, current, 'onto1_restriction', bool, 'boolean')
            onto2_restriction = parse_and_check(onto2_restriction, current, 'onto2_restriction', bool, 'boolean')
            onto1_list_clear = parse_and_check(onto1_list_clear, current, 'onto1_list_clear', '', '',
                                               special_parse='tuple')
            onto2_list_clear = parse_and_check(onto2_list_clear, current, 'onto2_list_clear', '', '',
                                               special_parse='tuple')
            synonyms = parse_and_check(synonyms, current, 'synonyms', bool, 'boolean')
            text_process = parse_and_check(text_process, current, 'text_process', bool, 'boolean')
            split_from1 = parse_and_check(split_from1, current, 'split_from1', str, 'string')
            split_since1 = parse_and_check(split_since1, current, 'split_since1', str, 'string')
            split_from2 = parse_and_check(split_from2, current, 'split_from2', str, 'string')
            split_since2 = parse_and_check(split_since2, current, 'split_since2', str, 'string')
            windowsize = parse_and_check(windowsize, current, 'windowsize', '', '', special_parse='numerical',
                                         up_lim=9, down_lim=1)
            globalthreshold = parse_and_check(globalthreshold, current, 'globalthreshold', '', '',
                                              special_parse='numerical', up_lim=1.0, down_lim=0.0)
            localthreshold = parse_and_check(localthreshold, current, 'localthreshold', '', '',
                                             special_parse='numerical', up_lim=1.0, down_lim=0.0)
            if current[0][1:] == 'topological_similarity' and current[1] != '\n':
                topological_test, topological_cosine, topological_pearson, topological_euclidean = \
                    establish_topological(current[1])
            topological_threshold = parse_and_check(topological_threshold, current, 'topological_threshold', '', '',
                                                    special_parse='numerical', up_lim=1.0, down_lim=0.0)

    if ontologyname1 == '':
        ontologyname1 = None
    if ontologyname2 == '':
        ontologyname2 = None
    if file_clean_ontology1 == '':
        file_clean_ontology1 = None
    if file_clean_ontology2 == '':
        file_clean_ontology2 = None
    if file1 is not None and input_folder is not None and input_folder != '':
        file1 = input_folder + file1
    if file2 is not None and input_folder is not None and input_folder != '':
        file2 = input_folder + file2


    print('input data: ' + input_folder)
    print('output data: ' + output_folder)

    return input_folder, output_folder, parallelization, proc, parse_ontology1, parse_ontology2, file1,\
           file_clean_ontology1,take_synonyms1, filter_by_keywords1, ontologyname1, synonym_type1, label_type1,\
           relative_type1, ontology1_file, ontology1_name, file2, file_clean_ontology2, take_synonyms2,\
           filter_by_keywords2, ontologyname2, synonym_type2, label_type2, relative_type2, ontology2_file,\
           ontology2_name, onto1_fuseclasses, onto2_fuseclasses, onto1_restriction, onto2_restriction, onto1_list_clear,\
           onto2_list_clear, synonyms, text_process, split_from1, split_since1, split_from2, split_since2, windowsize, \
           globalthreshold, localthreshold, topological_test, constraint_threshold, topological_cosine, \
           topological_pearson, topological_euclidean, topological_threshold
