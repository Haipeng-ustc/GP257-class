'''
This script demonstrates how to use the argparse module and logging module.

Author: Haipeng Li
Date: 2023-02-12
'''
 
import argparse
import logging
import operator
import numpy as np

import exp_parser


operations = {
    exp_parser.TokenType.T_PLUS: operator.add,
    exp_parser.TokenType.T_MINUS: operator.sub,
    exp_parser.TokenType.T_MULT: operator.mul,
    exp_parser.TokenType.T_DIV: operator.truediv
}


def compute(node, logger):
    # logger
    logger.debug('Enter compute function')

    if node.token_type == exp_parser.TokenType.T_NUM:
        return node.value
    left_result = compute(node.children[0], logger)
    right_result = compute(node.children[1], logger)
    operation = operations[node.token_type]
    
    return operation(left_result, right_result)


def check_exp_parser(exp):
    ''' This function is to check if the expression is valid. A valid expression 
    is consider to only contain 
        numeric digits from 0,1,2,3,4,5,6,7,8,9
        operations: '+', '-', '*', '/', '(', ')', 
        characters: 'f', 'i', 'l', 'e', which are used to represent file.

    Parameters
    ----------
    exp : str
        The expression to be checked
    
    Returns
    -------
    bool
        True if the expression is valid, False otherwise
    '''

    # set the legal characters
    file = ['f','i', 'l', 'e']
    num  = ['0','1','2','3','4','5','6','7','8','9']
    op   = ['+','-','*','/', '(', ')']

    # check if the expression is valid by looping through each character
    for i in exp: 
        if i not in file + num + op:
            return False

    return True


if __name__ == '__main__':
    '''
    This is the main function. It parses the command line arguments,
    sets up the logger, and calls the exp_parser to parse the expression. Then,
    it computes the result and writes the result to the output file.

    Example:
        $ python logger_argparse.py --exp file1+file2*file3 --outfile result.npz  --file1 labVec1.npz  --file2 labVec2.npz --file3 labVec3.npz
    '''

    # create a parser object
    parser = argparse.ArgumentParser(description='Demonstration of argparse module and logging module')

    # add a positional argument for math expression
    parser.add_argument('--exp',      type=str, required=True, help='math expression')
    parser.add_argument('--outfile',  type=str, required=True, help='file where the output is written')

    # add positional arguments for file names and the default value is empty string
    parser.add_argument('--file1', type=str, default='', required=False, help='file name for file 1')
    parser.add_argument('--file2', type=str, default='', required=False, help='file name for file 2')
    parser.add_argument('--file3', type=str, default='', required=False, help='file name for file 3')
    parser.add_argument('--file4', type=str, default='', required=False, help='file name for file 4')
    parser.add_argument('--file5', type=str, default='', required=False, help='file name for file 5')
    parser.add_argument('--file6', type=str, default='', required=False, help='file name for file 6')
    parser.add_argument('--file7', type=str, default='', required=False, help='file name for file 7')
    parser.add_argument('--file8', type=str, default='', required=False, help='file name for file 8')

    # create a logger object
    logger = logging.getLogger('my_logger')

    # set the logging level
    logger.setLevel(logging.DEBUG)

    # create a file handler
    fh = logging.FileHandler('my_logger.log', mode='w')
    fh.setLevel(logging.DEBUG)

    # create a stream handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.FATAL)

    # create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    # add the handler to the logger
    logger.addHandler(fh)
    logger.addHandler(sh)

    # parse the command line arguments
    args      = parser.parse_args()
    exp       = args.exp
    outfile   = args.outfile
    filenames = [args.file1, args.file2, args.file3, args.file4, 
                 args.file5, args.file6, args.file7, args.file8]

    # check if the expression is valid
    if not check_exp_parser(exp):
        logger.error('Invalid expression: {}'.format(exp))
        raise Exception('Invalid expression: {}'.format(exp))

    # perform the operation on files
    ast = exp_parser.parse(exp, filenames, logger)
    result = compute(ast, logger = logger)

    # write the result to a file
    try:
        np.savez(outfile, result)
        logger.info('The result is written to file {}'.format(outfile))
    except:
        logger.error('Failed to write the result to file {}'.format(outfile))
        raise Exception('Failed to write the result to file {}'.format(outfile))

    # logger ending message
    logger.info('This is the end of the program')
