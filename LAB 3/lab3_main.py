# Eduardo Silva nr 69916 - MEAer
# José Pereira nr 70369 - MEAer
# Version: Python 3.4.1

import copy #To copy lists without using pointers
from time import time #To count computational time
import fu #From last assignment, in order to put in the CNF form
import fu2 #To invoce the functions to prove the theorem
import os

## MAIN FUNCTION
#Description: executes the convertion between a logical sentence in the format:('=>', 'Mythical', 'Immortal'),from a file, to the CNF format.
#Reads from input_file.txt, and writes output to comant line and output.txt.
#Inputs: NONE
#Outputs: NONE
read_kb= fu.open_file('kbx.txt') #Reads info given in input file, by line
read_alpha= fu.open_file('alphax.txt') #Reads info given in input file, by line
kb=fu.file_to_list(read_kb) #Convert lines of the file into a list
alpha=fu.file_to_list(read_alpha) #Convert lines of the file into a list
f = open('output_file.txt', 'w') #Initiate Damp File, that will store everything
step1, step2, step3, step4, step5, kb_cnf=fu.CNF_converter(kb) #Conversion Step by Step
step1, step2, step3, step4, step5, alpha_cnf=fu.CNF_converter(alpha) #Conversion Step by Step
 
flag=1
while flag==1: #MENU : CHOOSE AN OPTION
    print('Artificial Intelligence and Decision Systems (IASD)')
    print('Assignment #3 - Version: Python 3.4.1')
    print('Eduardo Silva nr 69916 - MEAer')
    print('José Pereira nr 70369 - MEAer')
    print('\nOptions:\n\t1: List KB and alpha before theorem prover')
    print('\t2: Theorem Prover - List it Step-by-Step\n\t3: Exit')
    opt1=input('Choose an option [1, 2 or 3]\n')
    initial_time = time() #Set initial time

    if opt1=='1': #If chooses '1', prints kb and alpha
        fu.print_steps('List kb:', kb_cnf, f) #Print Sentences
        fu.print_steps('List alpha:', alpha_cnf, f) #Print Sentences
      
    elif opt1=='2': #If chooses '2', proves theorem step-by-step
        need_to_prove, result=fu2.check_inputs(alpha_cnf, kb_cnf,f)
###############################################
        if need_to_prove==1:
            step=0
            while step<len(alpha) and result!=1:
                not_alpha='not', alpha[step]
                step1, step2, step3, step4, step5, not_alpha_cnf=fu.CNF_converter([not_alpha]) #Conversion Step by Step
                done=0
                if not_alpha_cnf[0][0]=='I':
                    del(not_alpha_cnf)
                    done=1
                elif not_alpha_cnf[0][0]=='U':
                    del(not_alpha_cnf)
                    result=1
                    done=1
                if done!=1:
                    kb_cnf=not_alpha_cnf+kb_cnf
                    foo=0
                    lista=[]
                    while foo<len(kb_cnf):# Puts all the KB in the same line/clause
                        lista=lista+kb_cnf[foo]
                        foo=foo+1

                    print('Before Conversion, Step:'+str(step)+' (line in alpha)')
                    f.write('\nBefore Conversion Step:'+str(step)+' (line in alpha)\n')
                    fu.print_sentences(lista, f) #Prints whole list (KB and not alpha) before conversion  
                    lista=fu2.remove(lista) #Simplifies list
                    print('Simplified, Step:'+str(step)+' (line in alpha)') 
                    f.write('\nSimplified, Step:'+str(step)+' (line in alpha)\n')
                    fu.print_sentences(lista, f) #Prints simplified list (KB and not alpha)
                    lista=fu2.order(lista) #Puts list in order
                    print('Ordered, Step:'+str(step)+' (line in alpha)') 
                    f.write('\nOrdered, Step:'+str(step)+' (line in alpha)\n')
                    fu.print_sentences(lista, f) #Prints organized list (KB and not alpha)
                    check_changes=[]
                    result=1
                    while lista!=check_changes and result!=0: #Performs resolution
                        check_changes=lista[:]
                        lista,result=fu2.resolution(lista)
                        print('Resolution for all possible clauses, Step:'+str(step)+' (line in alpha)\n(Finds all the complementary pairs)')
                        f.write('\nResolution for all possible clauses, Step:'+str(step)+' (line in alpha)\n(Finds all the complementary pairs)\n')
                        fu.print_sentences(lista, f) #Prints list (KB and not alpha) after performing resolution
                step=step+1
############################################                
        print('The theorem prover has ended successfully')
        f.write('\nThe theorem prover has ended successfully')
        if result==0:
            print('Empty Clause -> Alpha Proved!')
            f.write('\nEmpty Clause -> Alpha Proved!\n')
        if result==1:
            print('Cannot Improve More -> Nothing Can Be Conclude!')
            f.write('\nCannot Improve More -> Nothing Can Be Conclude!\n')
        if result==2:
            print('KB given invalid, Impossible clause included!')
            f.write('\nKB given invalid, Impossible clause included!\n')
        flag=0

    elif opt1=='3': #If chooses '3' Exits
        flag=0

    else: #If neither of the four options chosen, user asked to choose again
        print('Unknown option, please choose again')
        
    computational_time=time()-initial_time #Computational Time
    print('\nComputational Time: '+str(computational_time)+' seconds') #Prints Computational Time after each option
    print('---------------------------------------------------------')
    f.write('\nComputational Time: '+str(computational_time)+' seconds')
    f.write('\n---------------------------------------------------------\n')
    if flag==0:
        f.close()
