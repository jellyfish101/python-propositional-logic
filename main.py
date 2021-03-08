from parser import *
from synthax import *

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
        func = TruthFunction(str)
        func.gen_table()
