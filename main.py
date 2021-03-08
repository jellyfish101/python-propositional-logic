from formula import *
from operators import *

if __name__ == "__main__":

    print("\nYou can use all these operators :\n")
    print("& : Conjunction / And Operator")
    print("| : Disjunction / Or Operator")
    print("-> : Implication Operator")
    print("<-> : Bi-Implication Operator")
    print("= : Equivalence Pperator")
    print("() : Parenthesis (Grouping)")
        
    while(1):      
        str = input("\nformula ? ==> ")
        formula = TruthFunction(str)
        formula.gen_table()
