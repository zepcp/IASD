# Eduardo Silva nr 69916 - MEAer
# José Pereira nr 70369 - MEAer
# Version: Python 3.4.1

import copy #To copy lists without using pointers
from time import time #To count computational time

#SET OF MICRO FUNCTIONS TO CHECK IF A GIVEN SENTENCE IS AN ATOM, NEGATION...

def isequi(sent):
    if sent[0]=='<=>': return 1
    return 0
def isimp(sent):
    if sent[0]=='=>': return 1
    return 0
def isneg(sent):
    if sent[0]=='not': return 1
    return 0
def isor(sent):
    if sent[0]=='or': return 1
    return 0
def isat(sent):
    if sent[0]!= '<=>' and sent[0]!= '=>' and sent[0]!= 'or' and sent[0]!= 'and' and sent[0]!= 'not':return 1
    return 0
def isand(sent):
    if sent[0]=='and': return 1
    return 0

# OPEN FUNCTION: Reads the file and stores it line by line
def open_file(file):
    with open(file) as f:
        read_file=[f.readline()]
        read_file[0]=read_file[0].strip('\n')
        aux=1
        while (aux != ''):
            aux=f.readline()
            aux=aux.strip('\n')
            read_file=read_file+[aux]  
    return read_file

# CONVERT FILE TO A LIST: PART B
def listit(t):
    return [listit(i) for i in t] if isinstance(t, (list,tuple)) else t

# CONVERT FILE TO A LIST: PART A
def file_to_list(read_file):
    lista=[]
    for i in range(len(read_file)-1):
        tupline=eval(read_file[i])
        lista.append(tupline)
    nlist=listit(lista)
    return nlist

# SOLVE EQUIVALENCE, get rid of equivalences (<=>)
def solve_equivalence(clause):
    if isat(clause): # Atom
        return clause # There are no (<=>), done, return itself
    if isimp(clause) or isand(clause) or isor(clause): # =>, or, and
        clause=[clause[0]]+[solve_equivalence(clause[1])]+[solve_equivalence(clause[2])] # Keep the symbol, recursively check the rest of the sentence
        return clause  
    if isneg(clause): # Not
        clause=[clause[0]]+[solve_equivalence(clause[1])] # Keep the 'not', recursively check the rest of the sentence
        return clause
    if isequi(clause): # Get rid of the equivalence, recursively check the rest of the sentence
        clause=['and', ['=>']+[solve_equivalence(clause[1])]+[solve_equivalence(clause[2])], ['=>']+[solve_equivalence(clause[2])]+[solve_equivalence(clause[1])]]
        return clause

# SOLVE IMPLICATION
def solve_implication(clause):
    if isat(clause): # Atom
        return clause # There are no (<=>), done, return itself  
    if isand(clause) or isor(clause): # or, and
        clause=[clause[0]]+[solve_implication(clause[1])]+[solve_implication(clause[2])] # Keep the symbol, recursively check the rest of the sentence
        return clause
    if isneg(clause): # Not
        clause=[clause[0]]+[solve_implication(clause[1])] # Keep the 'not', recursively check the rest of the sentence
        return clause
    if isimp(clause): # Get rid of the implication, recursively check the rest of the sentence
        clause=['or']+[['not']+[solve_implication(clause[1])]]+[solve_implication(clause[2])]
        return clause

# SOLVE NEGATION
def solve_negation(clause):
    if isneg(clause): # Not
        if isneg(clause[1]): # NotNot: Double negation, remove both
            clause=solve_negation(clause[1][1])
            return clause
        if isand(clause[1]): #NotAnd: Negate And (Or) and also negate both terms, recursively recheck the sentence
            clause=['or',['not',clause[1][1]],['not',clause[1][2]]]
            clause=solve_negation(clause)
            return clause
        if  isor(clause[1]): #NotOr: Negate Or (And) and also negate both terms, recursively recheck the sentence
            clause=['and',['not',clause[1][1]],['not',clause[1][2]]]
            clause=solve_negation(clause)
            return clause
    if isand(clause) or isor(clause): #And/Or: Keep the And/Or, recursively check the rest of the sentence
        clause[1]=solve_negation(clause[1])
        clause[2]=solve_negation(clause[2])
    return clause

# SOLVE DISJUNCTION
def solve_disjunction(clause):
    if isor(clause): #Or
        if isand(clause[1]) and isand(clause[2]): #OrAnd()And(): Apply distributive
            aux0=['and', ['or', clause[1][1], clause[2][1]], ['or', clause[1][1], clause[2][2]]]
            aux1=['and', ['or', clause[1][2], clause[2][1]], ['or', clause[1][2], clause[2][2]]]
            clause=['and', solve_disjunction(aux0), solve_disjunction(aux1)]
            if solve_disjunction(aux0) == solve_disjunction(aux1): #Simplifies, prevents clauses with the same atom to appear
                return solve_disjunction(aux0)
            return clause
        if isand(clause[1]): #OrAnd..: Apply distributive
            aux0=['or', clause[1][1], clause[2]]
            aux1=['or', clause[1][2], clause[2]]
            clause=['and', solve_disjunction(aux0), solve_disjunction(aux1)]
            if solve_disjunction(aux0) == solve_disjunction(aux1): #If repeated, Simplify
                return solve_disjunction(aux0)
            return clause
        if isand(clause[2]): #Or..And: Apply distributive
            aux0=['or', clause[1], clause[2][1]]
            aux1=['or', clause[1], clause[2][2]]
            if solve_disjunction(aux0) == solve_disjunction(aux1): #If repeated, Simplify
                return solve_disjunction(aux0)
            clause=['and', solve_disjunction(aux0), solve_disjunction(aux1)]
            return clause
        if isor(clause[1]) or isor(clause[2]): #OrOr, keep it, recursively check the rest of the sentence
            aux=solve_disjunction(clause[1])
            aux1=solve_disjunction(clause[2])
            clause=['or',aux,aux1]
            if isand(aux) or isand(aux1):
                clause=solve_disjunction(clause)
            return clause
    if isand(clause): #And, keep it, recursively check the rest of the sentence
        aux1=solve_disjunction(clause[1])
        aux2=solve_disjunction(clause[2])
        if aux1 == aux2: #If repeated, Simplify
            return aux1
        return ['and',aux1,aux2]
    return clause

#SIMPLIFY ORS, while converting to cnf clauses
def simplify_ors(clause):
    i=0
    while i<len(clause):
        j=0
        while j<len(clause[i]):
            if isor(clause[i]): #Simplifies (A or B), (B or A) then (A or B), also  (A or B), A then A, also (A or A) then A
                if clause[i][1]==clause[i][2]:#A or A then A
                    clause[i]=simplify_ors(clause[i][1])
                    return clause
                auxi=i
                i=0
                while i<len(clause):
                    if clause[i] == [clause[auxi][1]] or clause[i] == [clause[auxi][2]]: #Simplifies (A or B), A, then, A
                        del(clause[auxi])
                        return simplify_ors(clause) #Always recursively
                    if isor(clause[i]) and i != auxi: #Simplifies (A or B), (B or A), then, (A or B)
                        if clause[auxi][1]==clause[i][1] and clause[auxi][2]==clause[i][2]:
                            del(clause[i])
                            return simplify_ors(clause) #Always recursively
                        elif clause[auxi][1]==clause[i][2] and clause[auxi][2]==clause[i][1]:
                            del(clause[i])
                            return simplify_ors(clause) #Always recursively
                        return clause
                    i=i+1
                i=auxi
            j=j+1
        i=i+1
    return clause

# CONVERT TO CNF CLAUSES
def convert_clauses(clause):
    new1=[]
    convert_aux1(clause,new1) #removes ands
    new1=simplify_ors(new1) #simplify ors, before remove them
    new2=[[] for i in range(len(new1))]
    for i in range(len(new1)): #remove ors
        convert_aux2(new1[i], i,new2)
    return new2

# AUXILIAR ONE of convert to cnf clauses (remove ands from notation)
def convert_aux1(clause, new):
    if isand(clause): 
        convert_aux1(clause[1], new)
        convert_aux1(clause[2], new)
    elif isneg(clause):
        new.append(clause)
    else:
        new.append(clause)
    return 0   
   
# AUXILIAR TWO of convert to cnf clauses (remove ors from notation)
def convert_aux2(foo,i,new1):
    if isor(foo):
        convert_aux2(foo[1], i, new1)
        convert_aux2(foo[2], i, new1)
    elif isneg(foo):
        new1[i].append(foo)
    else:  
        new1[i].append(foo)
    return 0

# SIMPLIFIES CNF CLAUSES TO THE IRREDUCIBLE FORM
def simplifies_one(clause):
    i=0
    while i<len(clause):
        j=0
        while j<len(clause[i]):
            if isat(clause[i]):  #Simplifies repeated atoms (A or A), then, A
                auxj=j
                j=0
                while j<len(clause[i]):
                    if clause[i][auxj]==clause[i][j] and j!=auxj:
                        del (clause[i][j])
                        return simplifies_one(clause) #Always recursively
                    j=j+1
                j=auxj
            if isneg(clause[i][j]): #Simplifies Impossible, cannot be satisfied (=0)
                auxi=i
                auxj=j
                i=0
                while i<len(clause):
                    j=0
                    while j<len(clause[i]):
                        if clause[auxi][auxj][1]==clause[i][j] and (i!=auxi or j!=auxj):
                            aux=clause[auxi][:]
                            del(aux[auxj])
                            aux1=clause[i][:]
                            del(aux1[j])
                            if aux==aux1:
                                clause='Impossible, cannot satisfy both: '+str(clause[auxi])+' and '+str([clause[i][j]])
                                return simplifies_one(clause) #Always recursively
                        j=j+1
                    i=i+1
                i=auxi
                j=auxj
            if isneg(clause[i][j]): #Simplifies Unitary, if only clause then always satisfiable (=1)
                auxj=j
                j=0
                while j<len(clause[i]):
                    if clause[i][auxj][1]==clause[i][j]:
                        aux=clause[i]
                        del(clause[i])
                        if clause==[]:
                            return 'Unitary, always satisfiable: '+str(aux)
                        return simplifies_one(clause) #Always recursively
                    j=j+1
                j=auxj
            j=j+1
        i=i+1
    return clause
        
#CNF CONVERTER FUNCTION
def CNF_converter(sentences):
    i=0
    step1=[]
    step2=[]
    step3=[]
    step4=[]
    step5=[]
    step6=[]
    while i<len(sentences):
        step1=step1+[solve_equivalence(sentences[i][:])] #Does Step1, get rid of equivalences (<=>)
        step2=step2+[solve_implication(step1[i][:])] #Does Step2, get rid of implications (=>)
        step3=step3+[solve_negation(step2[i][:])] #Does Step3, move negations inwards (not)
        step4=step4+[solve_disjunction(step3[i][:])] #Does Step4, apply the distributive to disjunctions (or)
        step5=step5+[convert_clauses(step4[i][:])] #Does Step5, put CNF as a set of disjunctions
        step6=step6+[simplifies_one(step5[i][:])] #Does Step6, simplifies [[not, A],A] to 1
        i=i+1
    return step1, step2, step3, step4, step5, step6 #Returns the sentences in all the steps of conversion

# PRINT SENTENCES FUNCTION, runs all the lines and prints it
def print_sentences(mylist, f):
    i=0
    while i<len(mylist[:]):
        f.write('Nr'+str(i+1)+': '+str(mylist[i])+('\n'))
        print('Nr'+str(i+1)+': '+str(mylist[i]))
        i=i+1
    return

# PRINT STEPS FUNCTION, explains what list is printing and prints it
def print_steps(Explanation, mylist, f):
    print(Explanation)
    f.write(Explanation+'\n')
    print_sentences(mylist, f) #Invoces print_sentences to print list
    return

# MAIN FUNCTION
read_file = open_file('input_file.txt') #Reads info given in input file, by line
sentences=file_to_list(read_file) #Convert lines of the file into a list
f = open('output_file.txt', 'w') #Initiate Damp File, that will store everything

flag=1
while flag==1: #MENU : CHOOSE AN OPTION
    print('Artificial Intelligence and Decision Systems (IASD)')
    print('Assignment #2 - Version: Python 3.4.1')
    print('Eduardo Silva nr 69916 - MEAer')
    print('José Pereira nr 70369 - MEAer')
    print('\nOptions:\n\t1: List sentences before conversion')
    print('\t2: CNF converter - List One Sentence Step-by-Step')
    print('\t3: CNF converter - List All Sentences\n\t4: Exit')
    opt1=input('Choose an option [1, 2, 3 or 4]\n')
    initial_time = time() #Set initial time

    if opt1=='1': #If chooses '1', print sentences before conversion
        print_steps('List sentences before conversion:', sentences, f) #Print Sentences
      
    elif opt1=='2': #If chooses '2', asks which sentence to convert to CNF form
        print('Which sentence, from (input_file.txt), do you want to convert?')
        f.write('\nWhich sentence, from (input_file.txt), do you want to convert?\n')
        print_sentences(sentences, f)
        opt2=0
        while (int(opt2) < 1 or int(opt2) > len(sentences)):
               opt2=input('Choose the number of the sentence, from (input_file.txt), to convert\n')
               if (int(opt2) < 1 or int(opt2) > len(sentences)):
                   print("That sentence doesn't exist, please choose again")
        f.write('\nSentence Chosen:'+opt2+'\n')
        initial_time = time() #Reset initial time, needed to wait for user's response
        step1, step2, step3, step4, step5, step6=CNF_converter([sentences[int(opt2)-1]]) #Conversion Step by Step
        print_steps('Step1, get rid of equivalences (<=>):', step1, f) #Print Step1
        print_steps('Step2, get rid of implications (=>):', step2, f) #Print Step2
        print_steps('Step3, move negations inwards (not):', step3, f) #Print Step3
        print_steps('Step4, apply the distributive to disjunctions (or):', step4, f) #Print Step4
        print_steps('Step5, CNF as a set of disjunctions:', step5, f) #Print Step5
        print_steps('Step6, Simplifies clause:', step6, f) #Print Step6

    elif opt1=='3': #If chooses '3', converts every sentence to CNF form
        step1, step2, step3, step4, step5, step6=CNF_converter(sentences) #Conversion done Step by Step as well
        print_steps('\nConverted Sentences to the CNF form:', step6, f) #Print Converted Sentences

    elif opt1=='4': #If chooses '4', closes Damp File and Exits
        flag=0
        f.close() #Close Damp File

    else: #If neither of the four options chosen, user asked to choose again
        print('Unknown option, please choose again')
        
    computational_time=time()-initial_time #Computational Time
    print('\nComputational Time: '+str(computational_time)+' seconds') #Prints Computational Time after each option
    print('---------------------------------------------------------')
    if flag==1: #If file still open (doesn't make sense to compute time to exit [0 seconds])
        f.write('\nComputational Time: '+str(computational_time)+' seconds')
        f.write('\n---------------------------------------------------------\n')
