# ########## Libraries ########## #
from . import ontology_fusion as of
from . import Ontology_parse as op
from . import read_configuration as rc
from . import doc_managing as doc

import os
# ########## Functions ########## #


def fontcell(path_to_config, demo):
    '''
    # For set some argument by default add a '#' at line start
    :param: FOntCell_folder=''

    # Parallelization
    :param: parallelization=False
    :param: proc=1

    # # Ontology_parse
    :param: parse_ontology1=False
    :param: parse_ontology2=False

    # # # Ontology 1 # Only if parse_ontology1 == True
    :param: file1='///home/ra/Documentos/JavierCabau/Ontologies/CELDA_import.owl'
    :param: take_synonyms1=True
    :param: filter_by_keywords1='human', 'mouse'
    :param: ontologyName1=None
    :param: synonym_type1='owlNCBITaxon:synonym'
    :param: label_type1='CELDA:commonName xml:lang="en"', 'CELDA:commonName', 'rdfs:label'
    :param: relative_type1='owl:someValuesFrom'
    :param: edit_graph1=True
    # # # Ontology1 parsed path # only if parse_ontology1 == False
    :param: ontology1_path='parse_Celda.ods'
    :param: ontology1_name='CELDA'

    # # # Ontology 2 # Only if parse_ontology2 == True
    :param: file2=None
    :param: take_synonyms2=True
    :param: filter_by_keywords2='human', 'mouse'
    :param: ontologyName2=None
    :param: synonym_type2='owlNCBITaxon:synonym'
    :param: label_type2='rdfs:label')
    :param: relative_type2='owl:someValuesFrom'
    :param: edit_graph2=True
    # # # Ontology2 parsed path # only if parse_ontology2 == False
    :param: ontology2_path='Lifemap_syn.ods'
    :param: ontology2_name='Lifemap'

    # # ontology_fusion
    :param: onto1_fuseclasses=True
    :param: onto2_fuseclasses=True
    :param: onto1_restriction=False
    :param: onto2_restriction=True
    :param: onto1_list_clear='cell', 'cells'
    :param: onto2_list_clear='cell', 'cells'
    :param: synonyms=True
    :param: text_process=True
    :param: split_from1=None
    :param: split_since1=None
    :param: split_from2=None
    :param: split_since2=None
    :param: windowsize=4
    :param: globalthreshold=0.85
    :param: localthreshold=0.7
    :param: save_internals=True
    :param: OBO_format_result=False
    :param: save_internals_equiv=True
    :param: folder=''
    :param: draw_circular=True
    :param: constraint_threshold=0.0
    :param: topological_similarity='blondel'
    '''

    # read configurations
    root_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = root_dir + os.sep + 'fontcell_files'

    input_folder, output_folder, parallelization, proc, parse_ontology1, parse_ontology2, file1, \
    file_clean_ontology1, take_synonyms1, filter_by_keywords1, ontologyname1, synonym_type1, label_type1, \
    relative_type1, ontology1_path, ontology1_name, file2, file_clean_ontology2, take_synonyms2, \
    filter_by_keywords2, ontologyname2, synonym_type2, label_type2, relative_type2, ontology2_path, \
    ontology2_name, onto1_fuseclasses, onto2_fuseclasses, onto1_restriction, onto2_restriction, onto1_list_clear, \
    onto2_list_clear, synonyms, text_process, split_from1, split_since1, split_from2, split_since2, windowsize, \
    globalthreshold, localthreshold, topological_test, constraint_threshold, topological_cosine, topological_pearson,\
    topological_euclidean, topological_threshold = rc.read_conf(path_to_config, demo=demo)

    # perform a ontology parse
    if parse_ontology1:
        ontology1, onto_name1 = parser(file1, take_synonyms1, filter_by_keywords1, ontologyname1, synonym_type1,
                                       label_type1, relative_type1, file_clean_ontology1, input_folder=input_folder,
                                       output_folder=output_folder)
    else:
        path1 = input_folder + ontology1_path
        ontology1 = doc.import_ods(path1)
        onto_name1 = ontology1_name

    if parse_ontology2:
        ontology2, onto_name2 = parser(file2, take_synonyms2, filter_by_keywords2, ontologyname2, synonym_type2,
                                       label_type2, relative_type2, file_clean_ontology2, input_folder=input_folder,
                                       output_folder=output_folder)
    else:
        path2 = input_folder + ontology2_path
        ontology2 = doc.import_ods(path2)
        onto_name2 = ontology2_name

    # run parallelization
    if parallelization:
        # generates a csv of both ontologies and a parallel_configurations.txt
        config_path = os.path.join(root_dir, 'fusion_parallelized.py')
        doc.save_csv(ontology1, project_path + os.sep + 'onto1_for_parallel.csv')
        doc.save_csv(ontology2, project_path + os.sep + 'onto2_for_parallel.csv')
        list_of_variables = [onto_name1, onto_name2, file1, onto1_fuseclasses, onto2_fuseclasses, onto1_restriction,
                             onto2_restriction, onto1_list_clear, onto2_list_clear, synonyms, text_process, split_from1,
                             split_since1, split_from2, split_since2, windowsize, globalthreshold, localthreshold,
                             parallelization, constraint_threshold, topological_threshold, topological_cosine,
                             topological_pearson, topological_euclidean, output_folder]

        list_of_variables_str = list(map(lambda a: str(a)+'\n', list_of_variables))
        doc.save_txt(list_of_variables_str, project_path + os.sep + 'parallelization_config.txt')
        print('parallelizing')
        # launch a subprocess with mpirun and the parallelization (adding proc variable)
        cmd = "mpirun --allow-run-as-root -np " + str(proc) + " python3 " + config_path
        os.system(cmd)

    else:
        # doc.save_ods(ontology1, output_folder + os.sep +'CELDA_parsed.ods')
        # perform the align and merge/fusion
        of.fuseOntologies3(ontology1, ontology2, onto_name1, onto_name2,
                        onto1_path=file1,
                        onto1_fuseclasses=onto1_fuseclasses,
                        onto2_fuseclasses=onto2_fuseclasses,
                        onto1_restriction=onto1_restriction,
                        onto2_restriction=onto2_restriction,
                        onto1_list_clear=onto1_list_clear,
                        onto2_list_clear=onto2_list_clear,
                        synonyms=synonyms,
                        text_process=text_process,
                        split_from1=split_from1,
                        split_since1=split_since1,
                        split_from2=split_from2,
                        split_since2=split_since2,
                        windowsize=windowsize,
                        globalthreshold=globalthreshold,
                        localthreshold=localthreshold,
                        constraint_threshold=constraint_threshold,
                        topological_threshold=topological_threshold,
                        parallelization=parallelization,
                        topological_test=topological_test,
                        topological_cosine=topological_cosine,
                        topological_pearson=topological_pearson,
                        topological_euclidean=topological_euclidean,
                        output_folder=output_folder)
    return


def parser(file, take_synonyms, filter_by_keywords, ontologyname, synonym_type, label_type, relative_type,
           file_for_clean=None, input_folder=None, output_folder=None):
    ontology_parsed, ontology_name = op.parse_ontology(file, take_synonyms, filter_by_keywords, ontologyname, synonym_type,
                                                    label_type, relative_type, input_folder=input_folder,
                                                    output_folder=output_folder)
    if file_for_clean is not None:
        ontology_edited = op.editGraph(ontology_parsed, input_folder + file_for_clean, output_file=output_folder,
                                    ontoName=ontology_name)
        return ontology_edited, ontology_name
    else:
        return ontology_parsed, ontology_name
