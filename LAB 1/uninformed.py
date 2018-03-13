# Eduardo Silva nr 69916 - MEAer
# José Pereira nr 70369 - MEAer
# Version: Python 3.4.1

import copy #To copy lists without using pointers
from time import time #To count computational time

# OPEN FUNCTION: Reads the labyrinth from a file and saves in a matrix (map)
def open_file(file):
    with open(file) as f:
        lines, columns = [int(x) for x in f.readline().split()]
        map = [[int(x) for x in line.split()] for line in f]
    i=0 #ignore empty lines in the input file
    while i<lines:
        if map[i] == []:
            del (map[i])
            i=i-1
        i=i+1
    return lines, columns, map

# INITIAL POSITION FUNCTION: Searches for the initial position on the map to initialize the open list
def initial_position(lines, columns, map):
    global end
    x=0
    while x<columns:
        y=0
        while y<lines:
            if map[y][x] == 2: #If so, initial position found
                L_open=[[y,x,'',copy.deepcopy(map)]] # Set the open list (places to explore)
                L_closed=[] # Set the closed list (places already explored)
            y+=1
        x+=1

        end=1 # Initial position is never the final position (2!=3)

    return (L_open,L_closed)

# CHECK SWITCHES FUNCTION: Adds the switch option to the open list if it can open a door in the labyrinth 
def check_switches(length,L_open,lines,columns,map):
    j=0
    new=0
    while j < length:
        door=0
        if (map[L_open[j][0]][L_open[j][1]] > 99 and map[L_open[j][0]][L_open[j][1]] < 200):
            x=0
            while x<columns:
                y=0
                while y<lines:
                    if map[L_open[j][0]][L_open[j][1]] == L_open[j][3][y][x]-100:
                        door=1 #There is a closed door that will open if we push the switch
                    y+=1
                x+=1
        if door == 1: #So lets add to the open list a possibility of pushing the switch
            L_open=L_open+[[L_open[j][0],L_open[j][1],L_open[j][2]+'P',copy.deepcopy(L_open[j][3])]]
            x=0
            while x<columns:
                y=0
                while y<lines:
                    if L_open[j][3][y][x]-200 == map[L_open[j][0]][L_open[j][1]]:
                        L_open[length+new][3][y][x]=copy.deepcopy(L_open[j][3][y][x]-100) #Closes the door
                    if L_open[j][3][y][x]-100 == map[L_open[j][0]][L_open[j][1]]:
                        L_open[length+new][3][y][x]=copy.deepcopy(L_open[j][3][y][x]+100) #Opens the door                      
                    y+=1
                x+=1
            new+=1
        j+=1
    return L_open

# EXPAND NODES FUNCTION: Search possible paths and puts the actual/past positions in the closed list
def expand_nodes(list_lenght, L_open, L_closed, map):
    j=0 # Check for available paths without doors
    while j < list_lenght:
        if((map[L_open[j][0]+1][L_open[j][1]] != 0 and map[L_open[j][0]+1][L_open[j][1]] < 200)):
            L_open=L_open+[[L_open[j][0]+1,L_open[j][1],L_open[j][2]+'D',L_open[j][3]]]
        if((map[L_open[j][0]-1][L_open[j][1]] != 0 and map[L_open[j][0]-1][L_open[j][1]] < 200)):
            L_open=L_open+[[L_open[j][0]-1,L_open[j][1],L_open[j][2]+'U',L_open[j][3]]]
        if((map[L_open[j][0]][L_open[j][1]+1] != 0 and map[L_open[j][0]][L_open[j][1]+1] < 200)):
            L_open=L_open+[[L_open[j][0],L_open[j][1]+1,L_open[j][2]+'R',L_open[j][3]]]
        if((map[L_open[j][0]][L_open[j][1]-1] != 0 and map[L_open[j][0]][L_open[j][1]-1] < 200)):
            L_open=L_open+[[L_open[j][0],L_open[j][1]-1,L_open[j][2]+'L',L_open[j][3]]]
        j+=1
 
    j=0 # Check for available paths with open doors
    while j < list_lenght:
        if((L_open[j][3][L_open[j][0]+1][L_open[j][1]] > 299 and L_open[j][3][L_open[j][0]+1][L_open[j][1]] < 400)):
            L_open=L_open+[[L_open[j][0]+1,L_open[j][1],L_open[j][2]+'D',L_open[j][3]]]
        if((L_open[j][3][L_open[j][0]-1][L_open[j][1]] > 299 and L_open[j][3][L_open[j][0]-1][L_open[j][1]] < 400)):
            L_open=L_open+[[L_open[j][0]-1,L_open[j][1],L_open[j][2]+'U',L_open[j][3]]]
        if((L_open[j][3][L_open[j][0]][L_open[j][1]+1] > 299 and L_open[j][3][L_open[j][0]][L_open[j][1]+1] < 400)):
            L_open=L_open+[[L_open[j][0],L_open[j][1]+1,L_open[j][2]+'R',L_open[j][3]]]
        if((L_open[j][3][L_open[j][0]][L_open[j][1]-1] > 299 and L_open[j][3][L_open[j][0]][L_open[j][1]-1] < 400)):
            L_open=L_open+[[L_open[j][0],L_open[j][1]-1,L_open[j][2]+'L',L_open[j][3]]]
        j+=1

    j=0 #Put the previous node in the closed list (places already explored)
    while j < list_lenght:
        L_closed=L_closed+[L_open[0]]
        del (L_open[0])
        j+=1

    return (L_open, L_closed)

# CHECK REPEATED FUNCTION: Check for repeated/past members on the open list
def check_repeated(list_lenght_1, list_lenght_2, L_1, L_2):
    j=0
    while j < list_lenght_1:
        i=0
        while i < list_lenght_2:
            if L_1 != []:
                if i != j or L_1 != L_2: #Because L_1 can be L_2 (when searching for repeated nodes in L_open)
                    if (L_1[j][0] == L_2[i][0] and L_1[j][1] == L_2[i][1] and L_1[j][3] == L_2[i][3]):
                        if len(L_1[j][2])>=len(L_2[i][2]):
                            del(L_1[j])
                            list_lenght_1=list_lenght_1-1
                            if L_1 == L_2:
                                list_lenght_2=list_lenght_2-1                 
                            if j>0:
                                j=j-1
                        else:
                            del(L_2[i])
                            list_lenght_2=list_lenght_2-1
                        if L_1 == L_2:
                            list_lenght_1=list_lenght_1-1                 
                        if i>0:
                            i=i-1
                        
            i+=1
        j+=1
    return L_1

# FINISH FUNCTION: Check if finish, otherwise iterate again
def finish(L_open):
    global solution
    path_len=10000
    j=0
    end=1
    while j < len(L_open):
        if map[L_open[j][0]][L_open[j][1]]==3:
            end=0
            if len(L_open[j][2])<path_len: #Ensures fastest solution
                solution=L_open[j][2]
                path_len=len(solution)
        if L_open == []: #If so, it's impossible to finish (there is no nodes to expand)
            print ('There is no possible solution')
            solution='Not Found'
            end=0
        j+=1
    return end

# SAVE FUNCTION: Save in output file the labyrinth solution and prints in the terminal
def save(file, lines, columns, solution, time, len_open, len_closed):
    f = open(file, 'w')
    f.write('Nr of lines='+str(lines)+'\nNr of columns='+str(columns))
    f.write('\nSolution:'+str(solution)+'\nComputational Time: '+str(time))
    f.write('\nDepth:'+str(len(solution))+'\nNodes expanded:'+str(len_closed)+'\nChild Nodes:'+str(len_open))
    f.close()
    print('Nr of lines='+str(lines)+'\nNr of columns='+str(columns))
    print('Solution:'+str(solution)+'\nComputational Time: '+str(time))
    print('Depth:'+str(len(solution))+'\nNodes expanded:'+str(len_closed)+'\nChild Nodes:'+str(len_open))
    return

# MAIN FUNCTION - Independent Part of the Algorithm
initial_time = time() #Initial time
[lines, columns, map] = open_file('input.txt') #Reads info given about the labyrinth in input file

[L_open, L_closed]=initial_position(lines, columns, map) #Searches for the initial position

while end != 0: # Start Iterations - Breadth-first search Method (Depth=1)

    # Check if any of the cells in the open list are a switch cell that might need to be switched
    L_open=check_switches(len(L_open),L_open,lines,columns,map)#If so adds that possibility to the open list

    #Expand nodes, search possible paths and puts the actual/past positions in the closed list
    [L_open, L_closed] = expand_nodes(len(L_open), L_open, L_closed, map)

    #Check if this node is in the same place as a node in past iterations
    L_open=check_repeated(len(L_open),len(L_closed), L_open, L_closed)
            
    #Check if this node didn't generate repeated solution
    L_open=check_repeated(len(L_open),len(L_open), L_open, L_open)
    
    #Check if finish, otherwise iterate again
    end=finish(L_open)

final_time = time() #Final Time
save('output.txt', lines, columns, solution, final_time-initial_time, len(L_open), len(L_closed)) #Save solution and time in output file
