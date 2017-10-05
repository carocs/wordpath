#!/usr/bin/python
import argparse
import os
import sys


def hamming_distance(word1, word2):
    """return the hamming distance between two words of the same length"""
    return sum(c1 != c2 for c1, c2 in zip(word1, word2))


def parse_dict(dic, root):
    """parse the dict file and create a dictionary object with each word and the Hamming distance to the root"""
    word_list = []
    rootlen = root.__len__()
    # read file line by line
    with open(dic) as f:
        for line in f.read().splitlines():
            # if a word has the same length as the root, add it to the dict the hamming distance to the root
            if line.__len__() == rootlen:
                word_list.append(line)
                # if not, ignore it.
    return word_list


def find_leaves(word_list, word):
    """find all leaves for a given word.
    in this context, leaves for a given node (word) are all the words with hamming distance 1 from the node."""
    for w in word_list:
        if hamming_distance(w, word) == 1:
            yield w


def generate_tree(word_list, root, target):
    """generates a tree graph from the word list from root to target with a defined maximum depth
    this tree is created breadth-first and is represented with an adjacency matrix,
    which is returned once it finds the target or hit the maximum depth"""
    tree = []
    max_depth = 10

    for depth in range(max_depth):
        if depth == 0:
            tree.append({})
            tree[depth][root] = set([])
        tree.append({})
        for word in tree[depth].keys():
            for leaf in find_leaves(word_list, word):
                if leaf in tree[depth + 1].keys():
                    tree[depth + 1][leaf].add(word)
                else:
                    tree[depth + 1][leaf] = set([word])
                if leaf == target:
                    return tree

    print ("Target word not found after %d iterations." % max_depth)
    sys.exit(1)


def find_path(tree, root, target):
    """bottom up path finder in a tree graph"""
    path = [target]
    node = target

    for level in reversed(range(tree.__len__())):
        if node is not root:
            node = tree[level][node].pop()
            path.append(node)

    return reversed(path)


def solve(dic, root, target):
    """solve the path problem, parsing the dictionary file and finding the bath between root and target"""
    # parse the dict
    word_list = parse_dict(dic, root)

    # find the path
    solving_path = find_path(generate_tree(word_list, root, target), root, target)

    return solving_path


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("dictfile",
                        help="dictionary file to be used")

    parser.add_argument("rootword",
                        help="word to be used as origin in the path")

    parser.add_argument("targetword",
                        help="word to be used as objective in the path")

    args = parser.parse_args()

    # validate inputs
    if not os.path.isfile(args.dictfile):
        print "Dictionary file does not exist"
        sys.exit(1)

    if args.rootword.__len__() != args.targetword.__len__():
        print "Non-existing path. \n"
        print "Since only substitutions are allowed, only words with the same length have paths. \n"
        sys.exit(1)

    # find a path between the words
    solution = solve(args.dictfile, args.rootword, args.targetword)

    # print the results
    print (' -> '.join(solution))


if __name__ == "__main__":
    main()
