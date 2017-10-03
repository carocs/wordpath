#!/usr/bin/python
import argparse
import os
import sys


def hamming_distance(word1, word2):
    """return the hamming distance between two words of the same length"""
    return sum(c1 != c2 for c1, c2 in zip(word1, word2))


def parse_dict(dict, root):
    """parse the dict file and create a dictionary object with each word and the Hamming distance to the root"""
    word_dict = {}
    rootlen = root.__len__()
    # read file line by line
    with open(dict) as f:
        for line in f.read().splitlines():
            # if a word has the same length as the root, add it to the dict the hamming distance to the root
            if line.__len__() == rootlen:
                word_dict[line] = hamming_distance(root, line)
            # if not, ignore it.

    return word_dict


def find_path(word_dict, root, target):
    """find a path from root to target, using a dictionary with hamming distance between words"""
    path = []

    return path


def solve(dict, root, target):
    """solve the path problem, parsing the dictionary file and finding the bath between root and target"""
    solving_path = []

    # parse the dict
    word_dict = parse_dict(dict, root)

    # find the path
    solving_path = find_path(word_dict, root, target)

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
    print solution


if __name__ == "__main__":
    main()
