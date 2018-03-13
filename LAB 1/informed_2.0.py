# Eduardo Silva nr 69916 - MEAer
# José Pereira nr 70369 - MEAer
# Version: Python 3.4.1

import copy #To copy lists without using pointers
from time import time #To count computational time

##########################################
# OPEN FUNCTION: Reads the labyrinth from a fiel and saves in a matrix (map)
##########################################
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

##########################################
# INITIAL POSITION FUNCTION FUNCTION: Searches for the initial position (2) in the map 
##########################################
def initial_position(lines, columns, map):
    global end
    x=0
    while x<columns:
        y=0
        while y<lines:
            if map[y][x] == 2: #If so, initial position found
                [x_goal, y_goal]=goal_position(lines, columns, map)
                initial_estimation=heuristic(x, y, x_goal, y_goal)
                L_open=[[y,x,'', initial_estimation ,copy.deepcopy(map)]] # Set the open list (places to explore)
                L_closed=[] # Set the closed list (places already explored)
            y+=1
        x+=1

        end=1 # Initial position is never the final position (2!=3)

    return (L_open,L_closed)
##########################################
# GOAL POSITION FUNCTION FUNCTION: Searches for the goal position (3) in the map 
##########################################
def goal_position(lines, columns, map):
    x=0
    while x<columns:
        y=0
        while y<lines:
            if map[y][x] == 3: #If so, goal position found
                x_goal=x
                y_goal=y
            y+=1
        x+=1

        end=1 # Initial position is never the final position (2!=3)

    return (x_goal,y_goal)
##########################################
# SAVE FUNCTION: Save in output file the labyrinth solution
##########################################
def save(lines, columns, solution, final_time, initial_time):
    time=final_time-initial_time
    f = open('output.txt', 'w')
    f.write('nr of lines=' + str(lines) + '\n' + 'nr of columns=' + str(columns))
    f.write('\nSolution:' + str(solution)+'\n'+'Computational Time: '+str(time))
    f.close() 
    return

##########################################
# HEURISTIC FUNCTION: Calculates the distance between two points, or other heuristic function.
##########################################
def heuristic(y1, x1, x2, y2):
    distance=((abs(x2-x1)**2+abs(y2-y1)**2)**0.5)
 #   distance=0
    return distance
##########################################
# DECISION FUNCTION: Verifies which node should be explored
##########################################
def decision(L_open):
    list_lenght=len(L_open)
    i=0
    a=0
    b=100000
    j=i
    while i<list_lenght:
        a=L_open[i][3]
        if a<b:
            b=a
            j=i
        i+=1
    return j

##########################################
# PUSH FUNCTION: Verifies if the nod is a buttom and if it should be pushed
##########################################
def push_switches(L_open, lines, columns, L_open_all):
    push =0
    if L_open[4][L_open[0]][L_open[1]]>99 and  L_open[4][L_open[0]][L_open[1]]<200:
        x=0
        while x<columns:
            y=0
            while y<lines:
                if L_open[4][y][x] == L_open[4][L_open[0]][L_open[1]]+100:
                    push=1 #there is a door that needs to be changed
                y+=1
            x+=1
    if push==1:
        aux=L_open[2]
        L_open=[L_open[0],L_open[1],L_open[2]+'P',L_open[3],copy.deepcopy(L_open[4])]

        x=0

        while x<columns:
            y=0
            while y<lines:
                if L_open[4][y][x]-200 == L_open[4][L_open[0]][L_open[1]]:
                    
                    L_open[4][y][x]=copy.deepcopy(L_open[4][y][x]-100) #Closes the door
                elif L_open[4][y][x]-100 == L_open[4][L_open[0]][L_open[1]]:
                    
                    L_open[4][y][x]=copy.deepcopy(L_open[4][y][x]+100) #Opens the door
                    
                y+=1
            x+=1
                   
    return L_open, L_open_all

##########################################
# FINISH FUNCTION: Verifies a nod 
##########################################
def finish(L_open):
    j=0
    end=0
    solution=''
    while j <len(L_open) and end==0:
   #Check if the goal was achieved, Goal test
        if L_open[j][4][L_open[j][0]][L_open[j][1]]==3:
            solution=L_open[j][2]
            end=1
        if L_open==[]: #it is impossible to finish, there are no nodes to explore
            solution='Solution not found'
            end=1           
        j+=1
    return (end, solution)
##########################################
# EXPAND FUNCTION: Verifies the child nodes of a specific node and creates them putting them in the open list 
##########################################
def expand_nodes(L_open, L_open_foo, L_closed, x_goal, y_goal):
        
        #handling 1 and switches
        if(L_open_foo[4][L_open_foo[0]+1][L_open_foo[1]] != 0 and L_open_foo[4][L_open_foo[0]+1][L_open_foo[1]] < 200):
            heu=heuristic(L_open_foo[0]+1,L_open_foo[1], x_goal, y_goal )
            L_open=L_open+[[L_open_foo[0]+1,L_open_foo[1],L_open_foo[2]+'D',heu,copy.deepcopy( L_open_foo[4])]]
        if(L_open_foo[4][L_open_foo[0]-1][L_open_foo[1]] != 0 and L_open_foo[4][L_open_foo[0]-1][L_open_foo[1]] < 200):
            heu=heuristic(L_open_foo[0]-1,L_open_foo[1], x_goal, y_goal )
            L_open=L_open+[[L_open_foo[0]-1,L_open_foo[1],L_open_foo[2]+'U', heu,copy.deepcopy(L_open_foo[4])]]
        if(L_open_foo[4][L_open_foo[0]][L_open_foo[1]+1] != 0 and L_open_foo[4][L_open_foo[0]][L_open_foo[1]+1] < 200):
            heu=heuristic(L_open_foo[0],L_open_foo[1]+1, x_goal, y_goal )
            L_open=L_open+[[L_open_foo[0],L_open_foo[1]+1, L_open_foo[2]+'R',heu,copy.deepcopy( L_open_foo[4])]]
        if(L_open_foo[4][L_open_foo[0]][L_open_foo[1]-1] != 0 and L_open_foo[4][L_open_foo[0]][L_open_foo[1]-1] < 200):
            heu=heuristic(L_open_foo[0],L_open_foo[1]-1, x_goal, y_goal )
            L_open=L_open+[[L_open_foo[0],L_open_foo[1]-1,L_open_foo[2]+'L',heu,copy.deepcopy( L_open_foo[4])]]
   
        #Door handling
        if(L_open_foo[4][L_open_foo[0]+1][L_open_foo[1]] > 299 and L_open_foo[4][L_open_foo[0]+1][L_open_foo[1]] < 400):
            heu=heuristic(L_open_foo[0]+1,L_open_foo[1], x_goal, y_goal )
            L_open=L_open+[[L_open_foo[0]+1,L_open_foo[1],L_open_foo[2]+'D',heu,copy.deepcopy(L_open_foo[4])]]
        if(L_open_foo[4][L_open_foo[0]-1][L_open_foo[1]] > 299 and L_open_foo[4][L_open_foo[0]-1][L_open_foo[1]] < 400):
            heu=heuristic(L_open_foo[0]-1,L_open_foo[1], x_goal, y_goal )
            L_open=L_open+[[L_open_foo[0]-1,L_open_foo[1],L_open_foo[2]+'U', heu,copy.deepcopy(L_open_foo[4])]]
        if(L_open_foo[4][L_open_foo[0]][L_open_foo[1]+1] > 299 and L_open_foo[4][L_open_foo[0]][L_open_foo[1]+1] < 400):
            heu=heuristic(L_open_foo[0],L_open_foo[1]+1, x_goal, y_goal )
            L_open=L_open+[[L_open_foo[0],L_open_foo[1]+1, L_open_foo[2]+'R',heu,copy.deepcopy( L_open_foo[4])]]
        if(L_open_foo[4][L_open_foo[0]][L_open_foo[1]-1] > 299 and L_open_foo[4][L_open_foo[0]][L_open_foo[1]-1] < 400):
            heu=heuristic(L_open_foo[0],L_open_foo[1]-1, x_goal, y_goal )
            L_open=L_open+[[L_open_foo[0],L_open_foo[1]-1,L_open_foo[2]+'L',heu,copy.deepcopy( L_open_foo[4])]]

        L_closed=L_closed+[L_open_foo]
        del(L_open_foo)


        return (L_open, L_closed)

            
##########################################
# CHECK REPEATED FUNCTION: Verifies the recently created nodes in the 
##########################################
def check_repeated(L_1, L_2):
    j=0
    list_lenght_1=len(L_1)
    list_lenght_2=len(L_2)
    while j < list_lenght_1:
        i=0
        while i < list_lenght_2:
            if L_1 != []:
                if i != j or L_1 != L_2: #Because L_1 can be L_2 (when searching for repeated nodes in L_open)
                    if (L_1[j][0] == L_2[i][0] and L_1[j][1] == L_2[i][1] and L_1[j][4] == L_2[i][4]):
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
"""##########################################"""
#______________MAIN FUNCTION_____________#
   ##########################################
initial_time=time() #initial time of the process

#feitos: 1,2,3, 5, 6, 8, 9
[lines, columns, map]=open_file('input.txt')#reads information given from the map


[L_open, L_closed]=initial_position(lines, columns, map)
[x_goal, y_goal]=goal_position(lines, columns, map)

end=0


while end!=1: #Begins the search iterations - Method depending on the heuristic used
    
    foo= decision(L_open)#Choose which one has the smaller distance
  
    [L_open[foo], L_open]=push_switches(L_open[foo], lines, columns, L_open)#Check if the current node is a switch and needs to be pushed
    
    [L_open, L_closed]=expand_nodes(L_open, L_open[foo], L_closed, x_goal, y_goal)

    L_open=check_repeated(L_open, L_closed)

    L_open=check_repeated(L_open, L_open)

    [end, solution]=finish(L_open)

final_time=time() #Final Time

save(lines, columns, solution, final_time, initial_time)
print('##########SUCESSO##########')
print('Labyrinth Solution: '+solution)
print ('Computation Time: '+str(final_time-initial_time)+' sec')
print('Nodes expanded: '+str(len(L_closed))+'\nDepth:'+str(len(solution)))
