import os
import shutil
import subprocess

import networkx as nx


def save_dot_file(dot_contents, outfilepath):
    tred = shutil.which("tred")
    dot = shutil.which("dot")

    if not tred or not dot:
        print(
            "Graph not drawn, please install graphviz and add it to "
            "your path.\nOn Windows this is done with "
            "`choco install graphviz.portable`.\n")

        return

    with open("temp.dot", 'w') as file:
        file.write(dot_contents)

    try:
        tred_process = subprocess.Popen(
            [tred, 'temp.dot'], stdout=subprocess.PIPE)
        data = tred_process.stdout.read()
        tred_process.wait()
        with open("temp_reduced.dot", 'wb') as file:
            file.write(data)

        output = subprocess.check_output(
            [dot, '-Tsvg', 'temp_reduced.dot', '-o', 'temp.svg'])

        shutil.move("temp.svg", outfilepath)
        shutil.move("temp_reduced.dot", os.path.splitext(
            outfilepath)[0] + ".dot")
    finally:
        os.remove("temp.dot")


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    else:
        return text


def get_levels(dependency_map):
    dag = dag_from_hashmap_of_lists(dependency_map)

    topological = list(nx.topological_sort(dag))

    level_map = {}
    for package in topological[::-1]:
        dependencies = nx.descendants(dag, package)
        levels = {0}
        for dependency in sorted(list(dependencies)):
            try:
                levels.add(level_map[dependency])
            except KeyError:
                pass
        max_level = max(levels)
        level_map[package] = max_level + 1

    levels = {
        level: []
        for level in range(max(level_map.values()) + 1)
    }
    for package, level in level_map.items():
        levels[level].append(package)

    return levels


def dag_from_hashmap_of_lists(dictionary):
    keys = list(dictionary.keys())
    keys.sort(reverse=True)

    dag = nx.DiGraph()

    for key in keys:
        values = sorted(dictionary[key], reverse=True)
        dag.add_node(key)
        dag.add_nodes_from(values)
        edge_tuples = [
            (key, value) for value in values
        ]
        dag.add_edges_from(edge_tuples)

    return dag


def remove_postfix(text, postfix):
    if text.endswith(postfix):
        return text[:-len(postfix)]
    else:
        return text


def convert_path_to_package(path):
    return remove_postfix(path.replace(os.sep, '.'), '.py')
