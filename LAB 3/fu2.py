# Eduardo Silva nr 69916 - MEAer
# José Pereira nr 70369 - MEAer
# Version: Python 3.4.1

import copy #To copy lists without using pointers
import fu #From last assignment, in order to use the function "simplifies_one"
from time import time #To count computational time

#Check Inputs
#Description: Check if there is any mistake in the given inputs
#Inputs: KB and alpha
#Outputs: Flag signing the need to prove the theorem
def check_inputs(alpha_cnf, kb_cnf,f):
    result=-1
    need_to_prove=1
    foo=0
    while foo<len(alpha_cnf):
        if alpha_cnf[foo][0]=='I':
            result=1
            need_to_prove=0
            print('Alpha Impossible')
            f.write('\nAlpha Impossible\n')
        if alpha_cnf[foo][0]=='U':
            if result!=1:
                result=0
            del(alpha_cnf[foo])
            foo=foo-1
            if alpha_cnf==[]:
                need_to_prove=0
        foo=foo+1
    foo=0
    while foo<len(kb_cnf):
        if kb_cnf[foo][0]=='I':
            need_to_prove=0
            result=2
        if kb_cnf[foo][0]=='U':
            del(kb_cnf[foo])
            foo=foo-1
        foo=foo+1
    return need_to_prove, result
#Remove
#Description: Remove less constrained and repeated clauses
#Inputs: Whole list (KB and not alpha) 
#Outputs: List simplified
def remove(clause):
    for i in range(len(clause)): #all clauses, clause[i] is more restrict clause
        other=[j for j in range(len(clause))]
        other.pop(i)
        for j in other: #all other clauses, clause[j] more general clause
            foo=0
            for k in range(len(clause[i])):
                foo+=clause[j].count(clause[i][k])
            if foo==len(clause[i]): #clause[j] is unnecessary
                clause.pop(j)
                clause=remove(clause) #recursive to ensure that all contrained /repeated clauses are removed.
                return clause
    return clause

#Order
#Description:Ordenates the list with clauses to put the smaller elements as the first elements of the list
#Inputs: Whole disorganized list (KB and not alpha) 
#Outputs: Organized list, from smaller to larger number of literals (literals in the first elements)
def order(clause):
    ordered=[]
    foo=len(clause)
    while len(ordered)<foo:
        value=len(clause[0])
        entry=0
        for i in range(len(clause)):
            if value>len(clause[i]):
                value=len(clause[i])
                entry=i
        ordered.append(clause[entry])
        clause.pop(entry)
    return ordered

#Find Pairs
#Description: Finds Complementary Pairs (!A and A) in different clauses
#Inputs: Whole list (KB and not alpha) and a position in the list (i and j)
#Outputs: clauses with the complementary pairs
def find_pairs(lista,i,j):
    for i2 in range(len(lista)):
        for j2 in range(len(lista[i2])):
            if lista[i][j][0]=='not':
                if [lista[i2][j2]]==lista[i][j][1:]:
                    return i2,j2,1
            if lista[i2][j2][0]=='not':
                if [lista[i][j]]==lista[i2][j2][1:]:
                    return i2,j2,1
    return 0,0,0

# Resolution
#Description: Performs Resolution to all the pairs found (Also organize and simplify clauses)
#Inputs: Whole list (KB and not alpha) 
#Outputs: Whole list (KB and not alpha) after resolution
def resolution(lista): #choose following unit preference
    lista=order(lista) #Order clauses
    i=0
    while i<len(lista):
        j=0
        while j<len(lista[i]):
            i2,j2,flag=find_pairs(lista,i,j)
            if flag==1: #Complementary Literals found
                aux1=list(lista[i])
                aux2=list(lista[i2])
                aux1.pop(j)
                aux2.pop(j2)
                if aux1==[] and aux2==[]:
                    new=[]
                elif aux1==[]:
                    new=aux2
                elif aux2==[]:
                    new=aux1
                else:
                    new=[aux1]+[aux2]
                    for k in range(len(aux2)):
                        new.append(aux2[k])
                    new=new[0]
                lista.append(new)
                foo=0
                while foo<len(lista):
                    lista[foo]=fu.simplifies_one([lista[foo]])
                    if lista[foo][0]=='I':
                        return [],0
                    if lista[foo][0]!='U':
                        lista[foo]=lista[foo][0]
                    else: #If finds unitary condition remove it from the list
                        del(lista[foo])
                        if lista==[]: #If its the only condition theorem shouldnt be removed
                            lista=['Unitary']# And theorem prover must end
                            return lista,1
                    foo=foo+1
                lista=remove(lista) #Remove less constrained and repeated clauses
                if new==[] or lista==[]: #If so, empty clause -> alpha proved
                    return lista,0
            j=j+1
        i+=1
    return lista,1
