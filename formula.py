from operators import *
import sys

# get variable from string, will create new Variable with given name
class Variable:
    def parse(str):
        name = ""
        consumed = 0
        for ch in str:
            if ch.isalnum():
                name += ch
                consumed += 1
            else:
                break
        if consumed == 0:
            raise Exception(str+" is not a valid input string")
        return (Variable(name), str[consumed:])

    def __init__(self, name):
        self.name = name
        self.value = None

    def __str__(self):
        return self.name

    def __eval__(self):
        if self.value == None:
            raise Exception("Trying to evaulate a variable without any value")
        else:
            return self.value

# create new TruthFunction
class TruthFunction:

    def __init__(self, string):
        tokens = self.__tokenize__(string)
        self.__parse__(tokens)
        self.vars.sort(key=lambda v: v.name)

    def __tokenize__(self, formula):
        position = 0
        symbol_map = {
            "~": NegationOperator,
            "&": ConjunctionOperator,
            "|": DisjunctionOperator,
            "->": ImplicationOperator,
            "<->": BiimplicationOperator,
            "=": EquivalenceOperator,
            "(": LeftParen,
            ")": RightParen
        }
        symbols = symbol_map.keys()
        tokens = []
        while len(formula) != 0:
            if formula[0].isalnum():
                token, formula = Variable.parse(formula)
                token.position = position
                position += len(token.name)
                tokens.append(token)
            elif formula[0] in symbols:
                token = symbol_map[formula[0]]()
                token.position = position
                tokens.append(token)
                position += 1
                formula = formula[1:]
            elif formula[0:2] in symbols:
                token = symbol_map[formula[0:2]]()
                token.position = position
                tokens.append(token)
                position += 1
                formula = formula[2:]
            elif formula[0:3] in symbols:
                token = symbol_map[formula[0:3]]()
                token.position = position
                tokens.append(token)
                position += 1
                formula = formula[3:]
            elif formula[0] == " ":
                formula = formula[1:]
                position += 1
            else:
                raise Exception("UnexpectedSymbolAtPosition {}".format(position))
        return tokens

    def __parse__(self, tokens):
        vars = {}
        out = []
        operators = []
        for token in tokens:
            if isinstance(token, Variable):
                if token.name in vars:
                    out.append(vars[token.name])
                else:
                    vars[token.name] = token
                    out.append(token)
            elif isinstance(token, Operator):
                while len(operators) > 0 and isinstance(operators[-1], Operator) and operators[-1].__prec__() <= token.__prec__():
                    self.__add__operator(out, operators.pop(), False)
                operators.append(token)
            elif isinstance(token, LeftParen):
                operators.append(token)
            elif isinstance(token, RightParen):
                stack_token = operators.pop()
                while not isinstance(stack_token, LeftParen):
                    self.__add__operator(out, stack_token, False)
                    stack_token = operators.pop()
            else:
                raise Exception("UnknownToken Exception")

        for operator in operators[::-1]:
            if isinstance(operator, Operator):
                self.__add__operator(out, operator, False)
            else:
                raise Exception("ParensMismatch Exception")

        self.root = out.pop()
        if len(out) != 0:
            raise Exception("ERROR : UnconsumedVarsByOperators() Exception")
        self.vars = list(vars.values())

    def __eval__(self):
        return self.root.__eval__()

    def __add__operator(self, stack, operator, reverse_operands):
        if isinstance(operator, BinaryOperator):
            if len(stack) < 2:
                raise Exception(
                    "Binary operator at position {} doesn't have enough arguments".format(operator.position))
            operator.right, operator.left = stack.pop(), stack.pop()
            if reverse_operands:
                operator.right, operator.left = operator.left, operator.right
        elif isinstance(operator, UnaryOperator):
            if len(stack) < 1:
                raise Exception("Unary operator at position {} doesn't have an argument".format(operator.position))
            operator.operand = stack.pop()
        else:
            raise Exception("Not a binary or unary operator")
        stack.append(operator)

    def gen_table(self):
        
        formatString = "{{:0{}b}}: {{}}".format(len(self.vars))
        results = self.__eval___all()

        for x in self.vars:
            if isinstance(x, Variable):
                sys.stdout.write(str(x) + '   ')
        sys.stdout.write('r \n')

        statisfiable = False
        for k, v in results.items():
            to_print = formatString.format(k, v)
            flag = False
            for c in to_print:
                if c.isalnum():
                    if flag:
                        if c == 'F':
                            sys.stdout.write('0')
                        else:
                            sys.stdout.write('1')
                            statisfiable = True
                        sys.stdout.write('\n')
                        break;
                    sys.stdout.write(c + '    ')
                else:
                    flag = True

        if statisfiable:
            print("The compound proposition is statisfiable")
        else:
            print("The compound proposition is NOT statisfiable")

    def __eval___all(self):
        evaluation_results = {}
        for i in range(0, 2 ** len(self.vars)):
            evaluation_results[i] = self.__eval__bin(i)
        return evaluation_results
    def __eval__bin(self, bitset):
        values = []
        bitset += 2 ** len(self.vars)
        while bitset != 1:
            values.append(bitset % 2 == True)
            bitset //= 2
        values.reverse()
        return self.__eval__val(values)
    def __eval__val(self, values):
        if len(values) != len(self.vars):
            raise Exception("Incorrect variable value count when evaluating.")
        for (i, value) in enumerate(values):
            self.vars[i].value = value
        return self.__eval__()