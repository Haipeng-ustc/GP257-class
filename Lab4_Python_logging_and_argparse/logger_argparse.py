# demonstration of Python's argparse module and logging module

import argparse
import logging


def main():

    pass


if __name__ == '__main__':

    # create a parser object
    parser = argparse.ArgumentParser(description='Demonstration of argparse module and logging module')

    # add a positional argument for math expression
    parser.add_argument('--exp', type=str, required=True, help='math expression')
    parser.add_argument('--outfile', type=str, required=True, help='file where the output is written')

    # add a mutually exclusive group
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-x', '--exclusive1', action='store_true', help='a mutually exclusive option')
    group.add_argument('-y', '--exclusive2', action='store_true', help='a mutually exclusive option')

    # parse the command line arguments
    args = parser.parse_args()

    # set up logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # log the command line arguments
    logging.debug('positional: %s' % args.positional)
    logging.debug('optional: %s' % args.optional)

    # call main()
    main()