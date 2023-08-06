# Libraries #
from FOntCell import ontology_fusion as of
from FOntCell import doc_managing as doc

from mpi4py import MPI
import os
# ######### #

def read_variables(variable):
    try:
        vari = eval(variable)
    except:
        vari = variable
    return vari

# Read the configurations
def import_and_delete():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = root_dir + os.sep + 'fontcell_files' + os.sep

    list_of_variables = doc.import_txt(project_path + 'parallelization_config.txt')
    ontology1 = doc.import_csv(project_path + 'onto1_for_parallel.csv')
    ontology2 = doc.import_csv(project_path + 'onto2_for_parallel.csv')



    onto_name1 = read_variables(list_of_variables[0])
    onto_name2 = read_variables(list_of_variables[1])
    file1 = read_variables(list_of_variables[2])
    onto1_fuseclasses = read_variables(list_of_variables[3])
    onto2_fuseclasses = read_variables(list_of_variables[4])
    onto1_restriction = read_variables(list_of_variables[5])
    onto2_restriction = read_variables(list_of_variables[6])
    onto1_list_clear = read_variables(list_of_variables[7])
    onto2_list_clear = read_variables(list_of_variables[8])
    synonyms = read_variables(list_of_variables[9])
    text_process = read_variables(list_of_variables[10])
    split_from1 = read_variables(list_of_variables[11])
    split_since1 = read_variables(list_of_variables[12])
    split_from2 = read_variables(list_of_variables[13])
    split_since2 = read_variables(list_of_variables[14])
    windowsize = read_variables(list_of_variables[15])
    globalthreshold = read_variables(list_of_variables[16])
    localthreshold = read_variables(list_of_variables[17])
    parallelization = True
    constraint_threshold = read_variables(list_of_variables[19])
    topological_threshold = read_variables(list_of_variables[20])
    topological_cosine = read_variables(list_of_variables[21])
    topological_pearson = read_variables(list_of_variables[22])
    topological_euclidean = read_variables(list_of_variables[23])
    output_folder = read_variables(list_of_variables[24])

    return ontology1, ontology2, onto_name1, onto_name2, file1, onto1_fuseclasses, onto2_fuseclasses,\
           onto1_restriction, onto2_restriction, onto1_list_clear, onto2_list_clear, synonyms,\
           text_process, split_from1, split_since1, split_from2, split_since2, windowsize,\
           globalthreshold, localthreshold, parallelization, constraint_threshold, topological_cosine,\
           topological_pearson, topological_euclidean, topological_threshold, output_folder


# Perform the fusion parallelizing
def ontology_fusion_parallelized():
    ontology1, ontology2, onto_name1, onto_name2, file1, onto1_fuseclasses, onto2_fuseclasses,\
    onto1_restriction, onto2_restriction, onto1_list_clear, onto2_list_clear, synonyms,\
    text_process, split_from1, split_since1, split_from2, split_since2, windowsize,\
    globalthreshold, localthreshold, parallelization, constraint_threshold, topological_cosine,\
    topological_pearson, topological_euclidean, topological_threshold, output_folder = import_and_delete()

    of.fuseOntologies3(ontology1, ontology2, onto_name1, onto_name2, onto1_path=file1,
                       onto1_fuseclasses=onto1_fuseclasses, onto2_fuseclasses=onto2_fuseclasses,
                       onto1_restriction=onto1_restriction, onto2_restriction=onto2_restriction,
                       onto1_list_clear=onto1_list_clear, onto2_list_clear=onto2_list_clear, synonyms=synonyms,
                       text_process=text_process, split_from1=split_from1, split_since1=split_since1,
                       split_from2=split_from2, split_since2=split_since2, windowsize=windowsize,
                       globalthreshold=globalthreshold, localthreshold=localthreshold,
                       constraint_threshold=constraint_threshold, topological_threshold=topological_threshold,
                       parallelization=parallelization, topological_cosine=topological_cosine,
                       topological_pearson=topological_pearson, topological_euclidean=topological_euclidean,
                       output_folder=output_folder)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0:
        root_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep
        project_path = root_dir + 'fontcell_files' + os.sep
        try:
            os.remove(project_path + 'parallelization_config.txt')
            os.remove(project_path + 'onto1_for_parallel.csv')
            os.remove(project_path + 'onto2_for_parallel.csv')
            os.remove(root_dir + 'graph.gv')
            # os.remove(root_dir + 'graph.gv.pdf')
            os.remove(root_dir + 'graph.gv.plain')
            # os.remove(project_path + 'graph_viz_coord.ods')
        except:
            return
    return


if __name__ == '__main__':
    ontology_fusion_parallelized()
