'''
The code below is modified by Haipeng Li for the purpose of the course. The 
original code is from: https://github.com/gnebehay/parser

Modified by Haipeng Li
2023.02.12
'''

import enum
import numpy as np
import re

class TokenType(enum.Enum):
    T_NUM = 0
    T_PLUS = 1
    T_MINUS = 2
    T_MULT = 3
    T_DIV = 4
    T_LPAR = 5
    T_RPAR = 6
    T_END = 7


class Node:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value
        self.children = []


def lexical_analysis(s, files, logger):

    # logger
    logger.debug('Lexical analysis starts')

    mappings = {
        '+': TokenType.T_PLUS,
        '-': TokenType.T_MINUS,
        '*': TokenType.T_MULT,
        '/': TokenType.T_DIV,
        '(': TokenType.T_LPAR,
        ')': TokenType.T_RPAR}
    
    # modified by Haipeng Li for the purpose of the course
    tokens = []
    for c in s:
        if c in mappings:
            token_type = mappings[c]
            token = Node(token_type, value=c)
        elif re.match(r'\d', c):
            # load the file if the character is a digit corresponding to a file
            file = files[int(c)-1]
            try: 
                value = np.load(file)['arr_0']
                logger.info('File {} has been loaded'.format(file))
            except:
                logger.error('File {} cannot be found or loaded'.format(file))
                raise Exception('File {} cannot be found or loaded'.format(file))
            
            # create a token for the file
            token = Node(TokenType.T_NUM, value=value)

        elif c in ['f','i', 'l', 'e']:
            continue
        else:
            raise Exception('Invalid token: {}'.format(c))
        tokens.append(token)
    tokens.append(Node(TokenType.T_END))

    return tokens


def match(tokens, token, logger):

    # logger
    logger.debug('Matching starts')

    if tokens[0].token_type == token:
        return tokens.pop(0)
    else:
        raise Exception('Invalid syntax on token {}'.format(tokens[0].token_type))


def parse_e(tokens, logger):

    # logger
    logger.debug('Parsing starts (parse_e)')

    left_node = parse_e2(tokens, logger)

    while tokens[0].token_type in [TokenType.T_PLUS, TokenType.T_MINUS]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e2(tokens, logger))
        left_node = node

    return left_node


def parse_e2(tokens, logger):

    # logger
    logger.debug('Parsing starts (parse_e2)')

    left_node = parse_e3(tokens, logger)

    while tokens[0].token_type in [TokenType.T_MULT, TokenType.T_DIV]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e3(tokens, logger))
        left_node = node

    return left_node


def parse_e3(tokens, logger):

    # logger
    logger.debug('Parsing starts (parse_e3)')

    if tokens[0].token_type == TokenType.T_NUM:
        return tokens.pop(0)

    match(tokens, TokenType.T_LPAR, logger)
    expression = parse_e(tokens, logger)
    match(tokens, TokenType.T_RPAR, logger)

    return expression


def parse(inputstring, files, logger):

    # logger
    logger.debug('Entering parse function, with inputstring: {}, and files'.format(inputstring, files))

    tokens = lexical_analysis(inputstring, files, logger)
    ast = parse_e(tokens, logger)
    match(tokens, TokenType.T_END, logger)
    
    return ast
