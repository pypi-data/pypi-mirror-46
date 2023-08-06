import argparse
import sys

from code_parser.config import config
from code_parser.core import count_top_verbs_in_function_names, count_top_words_in_path, most_common_word


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='project path to analyze', default= config['CURRENT_DIR'], type=str)
    parser.add_argument('-e', '--exclude', help='dirs you need to exclude', default=config['IGNORED_DIRS'], type=str)
    return parser.parse_args(sys.argv[1:])


def main():
    args = parse_args()
    most_common_word(count_top_verbs_in_function_names(args.path, set(args.exclude.split(','))))
    most_common_word(count_top_words_in_path(args.path, set(args.exclude.split(','))))


if __name__ == '__main__':
    main()
