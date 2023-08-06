import json
import logging
import os
from collections import deque

from util.models import Node, Category, Automaton, ExportedAutomaton

logger = logging.getLogger('main')


# Utility function to return the preorder list of the given K-Ary Tree
def preorder_traversal_dir(directory, root_node):
    stack = deque([])
    preorder = []
    preorder_nodes = []
    # 'preorder'-> contains all the visited nodes
    preorder.append(root_node.key)
    preorder_nodes.append(root_node)

    for child in root_node.children:
        stack.append(child)

    while len(stack) > 0:
        # 'flag' checks whether all the child nodes have been visited
        flag = 0
        # take top node from the stack
        top_node = stack[len(stack) - 1]

        # if the top_node contains a Category we get its children
        if type(top_node.val) is Category:
            top_node_name = top_node.val.name.strip() \
                    .replace(os.sep, "_") \
                    .replace(":", "_") \
                    .replace("?", "")
            for child in os.listdir(directory + os.sep + top_node.path + os.sep + top_node_name):
                # we only care about the json object files
                if not child.endswith('.json'):
                    continue

                # read json file into dict and create object
                child_dict = read_json_file(directory + os.sep + top_node.path + os.sep + top_node_name + os.sep + child)
                logger.debug(child_dict)
                if 'latestAutomatonVersion' in child_dict:
                    child_ob = Automaton(child_dict)
                elif 'automatonFlow' in child_dict:
                    child_ob = ExportedAutomaton(child_dict)
                else:
                    child_ob = Category(child_dict)

                # create Node to contain object and add to top_node children
                child_node = Node(child_ob.id, child_ob)
                child_node.path = top_node.path + os.sep + top_node_name
                top_node.children.append(child_node)

        # add top_node to visited list
        preorder.append(top_node.key)
        preorder_nodes.append(top_node)

        if len(top_node.children) == 0:
            # CASE 1- If top of the stack is a leaf node then remove it from the stack
            x = stack.pop()  # TODO do something with x?
        else:
            # CASE 2- If top of the stack is parent with children
            for child in top_node.children:
                if child.key not in preorder:
                    flag = 1
                    # As soon as an unvisited child is found (left to right) push it to stack and store it in preorder
                    # start again from CASE-1 to explore this newly visited child
                    stack.append(child)

            # If all child nodes from left to right of a parent have been visited then remove the parent from the stack
            if flag == 0:
                stack.pop()

    return preorder_nodes


def find_category_parent(category, tree):
    for node in tree:
        if node.id == category.parent_id:
            return node

    return None


def find_automaton_parent(automaton, tree):
    for node in tree:
        if node.key == automaton.val.categoryId:
            return node

    return None


def get_directory_tree(directory):
    logger.debug("Reading directory %s", directory)

    # create fake root node
    root_category = Category(
        {'name': 'automata_root', 'id': 'root', 'clientId': '', 'parentId': None, 'deleted': False})
    root_node = Node(root_category.id, root_category)
    root_node.path = directory

    for child in os.listdir(directory):
        if not child.endswith('.json'):
            continue

        parent = directory.split(os.sep)[-1]
        if parent == 'automata':
            parent = ''
        child_dict = read_json_file(directory + os.sep + child)
        logger.debug(child_dict)
        if 'latestAutomatonVersion' in child_dict:
            child_ob = Automaton(child_dict)
        elif 'automatonFlow' in child_dict:
            child_ob = ExportedAutomaton(child_dict)
        else:
            child_ob = Category(child_dict)

        child_node = Node(child_ob.id, child_ob)
        child_node.path = parent
        root_node.children.append(child_node)

    return preorder_traversal_dir(directory, root_node)


def read_json_file(file_name):
    with open(os.path.normpath(file_name)) as infile:
        logger.debug('<Reading file %s', os.path.normpath(file_name))
        data = json.load(infile)
        return data


def write_json_file(file_name, data):
    with open(file_name, 'w') as outfile:
        logger.debug('>Writing file %s', file_name)
        json.dump(data, outfile, indent=4, sort_keys=True)
