# -------------------------------------------------------------
# OPERATOR SUPER CLASS
# -------------------------------------------------------------
class Operator(object):
    def __init__(self, kind):
        self.kind = kind
    def __str__(self):
        return self.kind

# -------------------------------------------------------------
# UNARY OPERATORS
# -------------------------------------------------------------

# Unary Operator Parent class (for unary operations such as negation)
class UnaryOperator(Operator):
    def __init__(self, kind):
        super().__init__(kind)
        self.operand = None

# Negation operator (~) example :
# q ~q
# 0 1
# 1 0
class NegationOperator(UnaryOperator):
    def __init__(self):
        super().__init__("~")
    def __prec__(self):
        return 0
    def __eval__(self):
        return not self.operand.__eval__()

# -------------------------------------------------------------
# BINARY OPERATORS
# -------------------------------------------------------------

# Binary operator parent class for operations such as and,or,xor
class BinaryOperator(Operator):
    def __init__(self, kind):
        super().__init__(kind)
        self.left = None
        self.right = None

# Conjunction / And Operator
# p q r
# 0 0 0
# 0 1 0
# 1 0 0
# 1 1 1
class ConjunctionOperator(BinaryOperator):
    def __init__(self):
        super().__init__("&")
    def __prec__(self):
        return 1
    def __eval__(self):
        return self.left.__eval__() and self.right.__eval__()

# Disjunction / Or Operator
# p q r
# 0 0 0
# 0 1 1
# 1 0 1
# 1 1 1
class DisjunctionOperator(BinaryOperator):
    def __init__(self):
        super().__init__("|")
    def __prec__(self):
        return 1
    def __eval__(self):
        return self.left.__eval__() or self.right.__eval__()

# Implication Operator : p->q
# (~p | q)
# p q r
# 0 0 1
# 0 1 1
# 1 0 0
# 1 1 1
class ImplicationOperator(BinaryOperator):
    def __init__(self):
        super().__init__("->")
    def __prec__(self):
        return 2
    def __eval__(self):
        return not self.left.__eval__() or self.right.__eval__()

# Bi-implication operator p<->q
# (p & q) | (~p & ~q)
# p q r
# 0 0 1
# 0 1 0
# 1 0 0
# 1 1 1
class BiimplicationOperator(BinaryOperator):
    def __init__(self):
        super().__init__("<->")
    def __prec__(self):
        return 2
    def __eval__(self):
        left = self.left.__eval__() and self.right.__eval__()
        right = not self.left.__eval__() and not self.right.__eval__()
        return left or right

# Equivalence operator (equals)
# p q r
# 0 0 1
# 0 1 0
# 1 0 0
# 1 1 1
class EquivalenceOperator(BinaryOperator):
    def __init__(self):
        super().__init__("=")
    def __prec__(self):
        return 3
    def __eval__(self):
        return self.left.__eval__() == self.right.__eval__()

# Parenthesis (Grouping)
class LeftParen:
    def __repr__(self):
        return "("
class RightParen:
    def __repr__(self):
        return ")"
