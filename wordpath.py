#!/usr/bin/python
import argparse
import os
import sys

ROOT = ''
TARGET = ''


def hamming_distance(word1, word2):
    """return the hamming distance between two words of the same length"""
    return sum(c1 != c2 for c1, c2 in zip(word1, word2))


def parse_dict(dic):
    """parse the dict file and create a list object with each word with the same length as the root"""
    word_list = []
    rootlen = ROOT.__len__()

    # read file line by line
    with open(dic) as f:
        for line in f.read().splitlines():
            # if a word has the same length as the root, add it to the list
            if line.__len__() == rootlen:
                word_list.append(line)

    if ROOT not in word_list:
        print ("The word %s is not in the dictionary file." % ROOT)
        sys.exit(1)

    if TARGET not in word_list:
        print ("The word %s is not in the dictionary file." % TARGET)
        sys.exit(1)

    return word_list


def find_leaves(word_list, word):
    """find all leaves for a given word.
    in this context, leaves for a given node (word) are all the words with hamming distance 1 from the node."""
    for w in word_list:
        if hamming_distance(w, word) == 1:
            yield w


def generate_tree(word_list):
    """generates a tree graph from the word list from root to target with a maximum depth equal to the length
    of the words squared. this tree is created breadth-first and is represented with an adjacency matrix,
    which is returned once it finds the target or hit the maximum depth"""
    tree = []
    max_depth = ROOT.__len__() ** 2

    for depth in range(max_depth):
        if depth == 0:
            tree.append({})
            tree[depth][ROOT] = set([])
        tree.append({})
        for word in tree[depth].keys():
            for leaf in find_leaves(word_list, word):
                if leaf in tree[depth + 1].keys():
                    tree[depth + 1][leaf].add(word)
                else:
                    tree[depth + 1][leaf] = {word}
                if leaf == TARGET:
                    return tree

    print ("Target word not found after %d letter substitutions." % max_depth)
    sys.exit(1)


def find_path(tree):
    """bottom-up path finder in a tree graph"""
    node = TARGET
    path = [node]

    for level in reversed(range(tree.__len__())):
        if node is not ROOT:
            node = tree[level][node].pop()
            path.append(node)

    return reversed(path)


def solve(dic, root, target):
    """solve the path problem, parsing the dictionary file and finding the path between root and target"""
    global ROOT
    global TARGET
    ROOT = root
    TARGET = target

    # parse the dict
    word_list = parse_dict(dic)

    # find the path
    solving_path = find_path(generate_tree(word_list))

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
        print ("Dictionary file does not exist")
        sys.exit(1)

    if args.rootword.__len__() != args.targetword.__len__():
        print ("Non-existing path.")
        print ("Since only substitutions are allowed, only words with the same length have paths.")
        sys.exit(1)

    # find a path between the words and print it
    solution = solve(args.dictfile, args.rootword, args.targetword)

    print (' -> '.join(solution))


if __name__ == "__main__":
    main()
