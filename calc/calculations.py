import logging
import re
import math
import copy

constants =[
    {"name":"π","val":math.pi},
    {"name":"e","val":math.e}
]

functions = {
    "+":{
        "n":2,
        "func": lambda x,y: x+y,
        "level":2,
        "regex_name":"\+"
    },
    "-":{
        "n":2,
        "func": lambda x,y: x-y,
        "level":2,
        "regex_name":"-"
    },
    "*":{
        "n":2,
        "func":lambda x,y: x*y,
        "level":3,
        "regex_name":"\*"
    },
    "/":{
        "n":2,
        "func":lambda x,y:x/y,
        "level":3,
        "regex_name":"\/"
    },
    "^":{
        "n":2,
        "func":lambda x,y:x**y,
        "level":4,
        "regex_name":"\^"
    },
    "(":{
        "n":0,
        "func":None,
        "level":1,
        "regex_name":"\("
    },
    ")":{
        "n":0,
        "func":None,
        "level":1,
        "regex_name":"\)"
    },
    "sin":{
        "n":1,
        "func":lambda x:math.sin(x),
        "level":5,
        "regex_name":"sin"
    },
    "cos": {
        "n": 1,
        "func": lambda x: math.cos(x),
        "level": 5,
        "regex_name": "cos"
    },
    "tan": {
        "n": 1,
        "func": lambda x: math.tan(x),
        "level": 5,
        "regex_name": "tan"
    },
    "arcsin": {
        "n": 1,
        "func": lambda x: math.asin(x),
        "level": 5,
        "regex_name": "arcsin"
    },
    "arccos": {
        "n": 1,
        "func": lambda x: math.acos(x),
        "level": 5,
        "regex_name": "arccos"
    },
    "arctan": {
        "n": 1,
        "func": lambda x: math.atan(x),
        "level": 5,
        "regex_name": "arctan"
    }
}
unary_operators = {
    "-":{
            "n": 1,
            "func":lambda x: -x,
            "level":4.5,
            "regex_name":"&"
    },
    "+":{
            "n": 1,
            "func":lambda x: x,
            "level":4.5,
            "regex_name":"&"
    },
}

logger = logging.getLogger(__name__)

def parse_line(calc_line,evaluate=True,ans=None,x=None,anim_vars=None):
    """
    Parses a given equation by converting infix to reverse polish
    :param calc_line: The equation
    :param prev_ans: The value for ANS if it appears in the calc_line, defaults to None
    :return:
    """
    global functions,unary_operators
    f_stack = []
    rpn_line = []
    last_char = None
    # Construct regex to split on all operations
    regex_names = []
    for f_name,func in functions.items():
        regex_names.append(func["regex_name"])

    f_line = re.split("({})".format("|".join(regex_names)),calc_line)

    logger.info("Eval {}".format(f_line))

    i = 0
    while i < len(f_line):
        c = f_line[i]
        if c == "":
            i += 1
            continue
        logger.debug("Using {}".format(c))
        if c in functions:
            # Current item is a function
            if ((last_char in functions) and (last_char != ")") and (c in unary_operators)) or (last_char == None and c in unary_operators):
                # Current item is a unary operator
                logger.debug("Unary operator {}".format(c))
                rpn_line.append("{}{}".format(c,f_line[i+1]))
                last_char = f_line[i+1]
                i += 1
            elif c == "(":
                logger.debug("Adding ( to f_stack")
                f_stack.append(c)
                last_char = c
            elif c == ")":
                logger.debug("Closing bracket")
                while f_stack[-1] != "(":
                    rpn_line.append(f_stack.pop())
                f_stack.pop()
                logger.debug("f_stack after ')': {}".format(f_stack))
                last_char = c

            elif len(f_stack) == 0:
                logger.debug("Appending function {} to empty f_stack".format(c))
                f_stack.append(c)
                last_char = c

            elif functions[f_stack[-1]]["level"] < functions[c]["level"]:
                logger.debug("Appending function {} to f_stack".format(c))
                f_stack.append(c)
                last_char = c
            else:
                try:
                    while functions[f_stack[-1]]["level"] >= functions[c]["level"]:
                        logger.debug("Adding {} to rpn_line as higher than {}".format(f_stack[-1],c))
                        rpn_line.append(f_stack.pop())
                except IndexError:
                    # f_stack is empty
                    pass
                f_stack.append(c)
                logger.debug("Added {} to f_stack, now {}".format(c,f_stack))
                last_char = c
            logger.debug("f_stack at {}".format(f_stack))

        else:
            # Current item is an operand
            rpn_line.append(c)
            last_char = c

        i += 1

    while f_stack != []:
        rpn_line.append(f_stack.pop())

    logger.info("RPN line at end of parsing: {}".format(rpn_line))
    if evaluate:
        val = eval_rpn(rpn_line,x,anim_vars)
        return val
    else:
        return rpn_line


def eval_rpn(rpn_line,x,anim_vars=None):
    global functions,constants
    eval_stack = []
    all_vars = copy.copy(constants)
    # Don't add empty anim_vars to all_vars
    if not (anim_vars == [] or anim_vars == None):
        all_vars.append(*anim_vars)

    for c in rpn_line:
        if c in functions:
            logger.debug("Evaluating function {}".format(c))
            func = functions[c]
            args = []
            for i in range(0,func["n"]):
                # Retrieve required amount of arguments
                args.append(float(eval_stack.pop()))
            # Reverse args so first argument would be towards bottom of stack
            args = args[::-1]
            logger.debug("Using args: {}".format(args))
            val = func["func"](*args)
            eval_stack.append(val)
            logger.debug("Adding value from function {} to stack".format(val))
        else:

            logger.debug("Adding {} to eval_stack".format(c))
            # Replace any vars
            # TODO add ability to multiply vars together like AB
            for a_var in all_vars:
                if a_var["name"] in c:
                    c = c.replace(a_var["name"],str(a_var["val"]))

            if c.endswith("x"):
                if len(c) > 1:
                    c = str(float(c[:-1]) * x)
                else:
                    c = str(x)

            eval_stack.append(c)
            logger.debug("eval_stack at {}".format(eval_stack))

    return float(eval_stack[0])