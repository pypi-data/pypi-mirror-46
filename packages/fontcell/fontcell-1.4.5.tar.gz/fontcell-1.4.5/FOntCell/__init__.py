from . import fontcell_main as fm

import os
import shutil


def current_version():
    """
    :return: the current version of FOntCell
    """
    print('FOntCell version: 1.4.5')
    return


def run(config_path, demo=False):
    print()
    current_version()
    print()
    # where_I_am()
    root_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isdir(root_dir + os.sep + 'fontcell_demo' + os.sep + 'results'):
        os.mkdir(root_dir + os.sep + 'fontcell_demo' + os.sep + 'results')
    if not os.path.isdir(root_dir + os.sep + 'fontcell_files'):
        os.mkdir(root_dir + os.sep + 'fontcell_files')
    if config_path[0] == os.sep:
        conf = str(config_path)
    elif config_path[0:4] == 'file':
        conf = str(config_path.split('file:')[1])
    else:
        raise ValueError('Path-to-configuration must be a real path or a path-to-file, and be surrounded by \'\'')
    fm.fontcell(conf, demo)
    # clean()
    return


def run_demo():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = root_dir + os.sep + 'fontcell_demo'
    print('running: FOntCell.run(\'' + 'file:' + project_path + os.sep + 'demo_configurations.txt\')')
    run('file:' + project_path + os.sep + 'demo_configurations.txt', demo=True)
    print('output data at: ' + project_path + os.sep + 'results')
    return


def clean():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = root_dir + os.sep + 'fontcell_files'
    try:
        shutil.rmtree(project_path)
        print('old files deleted')
    except:
        print('There is no internal files yet')
    return


def where_I_am():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    return print(root_dir + os.sep)
