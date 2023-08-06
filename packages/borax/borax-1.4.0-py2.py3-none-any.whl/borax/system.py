# coding=utf8
import os
import sys


def load_class(s):
    """Import a class
    :param s: the full path of the class
    :return:
    """
    path, class_ = s.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, class_)


def check_path_variables(execute_filename):
    try:
        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    except KeyError:
        user_paths = []
    for item in user_paths:
        if os.path.exists(os.path.join(item, execute_filename)):
            return True
    os_paths_list = os.environ['PATH'].split(';')
    for item in os_paths_list:
        if os.path.exists(os.path.join(item, execute_filename)):
            return True
    return False
