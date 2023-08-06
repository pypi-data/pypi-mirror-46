import os
import collections
import ast
import nltk


def collect_files_path(project_path, excludet_dir_names=None):
    """
    Collect all .py files path
    :param project_path: str
    :param excludet_dir_names: set
    :return: list
    """
    if excludet_dir_names is None:
        excludet_dir_names = {}
    pyfiles_path =[]
    for dirpath, dirrectories, filenames in os.walk(project_path, topdown=True):
        dirrectories[:] = [dir for dir in dirrectories if dir not in excludet_dir_names]
        for filename in filenames:
            if filename.endswith(".py"):
                pyfiles_path.append(os.path.join(dirpath, filename))
    return pyfiles_path


def get_trees(project_path, excludet_dir_names=None):
    """
    Parse all .py files in project into ast trees
    :param project_path: str
    :param excludet_dir_names: set
    :return: list
    """
    if excludet_dir_names is None:
        excludet_dir_names = {}
    trees = []
    pyfiles_path = collect_files_path(project_path, excludet_dir_names)
    for filename in pyfiles_path:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            file_content = attempt_handler.read()
        try:
            tree = ast.parse(file_content)
        except SyntaxError as e:
            print(e)
        else:
            trees.append(tree)
    return trees


def get_all_names(tree):
    """
    Collect all identifier names from ast tree
    :param tree: _ast.Module
    :return: list
    """
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_all_function_names(tree):
    """
    Collect all function names from ast tree
    :param tree: _ast.Module
    :return: list
    """
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and not (node.name.startswith('__') and node.name.endswith('__'))]


def extract_all_words_from_list_names(names_list):
    """
    Extract all words from list with snake case names
    :param names_list: list
    :return: list
    """
    word_list = []
    for name in names_list:
        word_list += name.split("_")
    return word_list


def is_verb(word):
    """
    Check if word is verb
    :param word: str
    :return: bool
    """
    if not word:
        return False
    pos_info = nltk.pos_tag([word])
    return pos_info[0][1] == 'VB'


def count_top_words_in_path(project_path, excludet_dir_names=None, limit_words=20):
    """
    Counting all words that uses in project
    :param project_path: str
    :param excludet_dir_names: set
    :param limit_words: int
    :return: list
    """
    if excludet_dir_names is None:
        excludet_dir_names = {}
    trees = get_trees(project_path, excludet_dir_names)
    path_words =[]
    for tree in trees:
        path_words += get_all_names(tree)
    print("Found {words} words, unique {uniq_words}".format(words=len(path_words), uniq_words=len(set(path_words))))
    return collections.Counter(extract_all_words_from_list_names(path_words)).most_common(limit_words)


def count_top_verbs_in_function_names(project_path, excludet_dir_names=None, limit_words=20):
    """
    Counting all verbs from function names that uses in project
    :param project_path: str
    :param excludet_dir_names: set
    :param limit_words: int
    :return: list
    """
    if excludet_dir_names is None:
        excludet_dir_names = {}
    trees = get_trees(project_path, excludet_dir_names)
    function_names_in_path = []
    for tree in trees:
        function_names_in_path += get_all_function_names(tree)
    print("Found {functions} functions".format(functions=len(function_names_in_path)))
    verbs = [word for word in extract_all_words_from_list_names(function_names_in_path) if is_verb(word)]
    return collections.Counter(verbs).most_common(limit_words)


def most_common_word(top_function_result):
    if top_function_result:
        return print("Most common is {word}, used {times} times".format(word=top_function_result[0][0], times=top_function_result[0][1]))
    return print("Result is empty")




