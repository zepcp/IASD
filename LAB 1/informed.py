# Eduardo Silva nr 69916 - MEAer
# José Pereira nr 70369 - MEAer

##########################################
# XPTO FUNCTION: Check if any sequencie is inside another sequence
##########################################
def xpto(lopen,lclosed):
    aux1=str.split(lopen)
    aux2=str.split(lclosed)
    fii=0
    count=0
    check=0

    while fii<len(aux1):
        i=0
        while i<len(aux2):
            if int(aux1[fii])==int(aux2[i]):
                count+=1
            i+=1
        fii+=1
    if count ==len(aux1) and count !=0:
        check=1
    if len(aux1)==0 and len(aux2)==0:
        check=1
    return check
##########################################
# SWITCH FUNCTION: Check if any switch was pressed
##########################################
def switches(seq1,swet):
    fii=0
    aux1=str.split(swet)
    while fii<len(aux1):
        
        if int(aux1[fii])==int(seq1):
            return 1
        fii+=1
    return 0

##########################################
# SAVE FUNCTION: Save in output file the labyrinth solution
##########################################
def save(lines, columns, solution):
    f = open('output.txt', 'w')
    f.write('nr of lines=' + str(lines) + '\n' + 'nr of columns=' + str(columns))
    f.write('\nSolution:' + str(solution))
    f.close() 
    return

##########################################
# DISTANCE FUNCTION: Calculates the distance between two points
##########################################
def dist(x1, y1, x2, y2):
    distance=((abs(x2-x1)**2+abs(y2-y1)**2)**0.5)
    #distance=0
    return distance

"""##########################################"""
#______________MAIN FUNCTION_____________#
   ##########################################

with open('input2.txt') as f: # Save labyrinth in a matrix (map)
    lines, columns = [int(x) for x in f.readline().split()]
    map = [[int(x) for x in line.split()] for line in f]
    initial_map=map

solution='' #Still no solution found

x=0 #Search the initial position
while x<columns:
    y=0
    while y<lines:
        if map[y][x] == 2:
         x_initial=x
         y_initial=y
        y+=1
    x+=1
end=1 #Initial position is never the final position (2!=3)

x=0 #Search the position of the goal
while x<lines:
    y=0
    while y<columns:
        if map[y][x] == 3:  
         x_goal=x
         y_goal=y
        y+=1
    x+=1


initial_estimation=dist(x_initial, y_initial, x_goal, y_goal)
#print(initial_estimation)

#Set the open list (places to explore) and closed list (places already explored)
L_open=[[y_initial,x_initial, initial_estimation,'','']]
L_closed=[]
L_switch=[]

end=0 #Initial position is never the final position (2!=3)
iteration=0
switch=0

while end!=1:
    #print('Iteration number: ', iteration)
    iteration+=1

    #Choose which one has the smaller distance
    list_lenght=len(L_open)
    i=0
    a=0
    j=i
    while i<list_lenght:
        b=a
        a=L_open[i][2]
        if a<b:
            j=i
        i+=1

    #print(L_open)
    #print(L_closed)
    #Check if the current node is a switch and needs to be pushed
   
    if map[L_open[j][0]][L_open[j][1]]>99 and map[L_open[j][0]][L_open[j][1]]<200:
        x=0
        while x<lines:
            y=0
            while y<columns:
                if map[y][x] == map[L_open[j][0]][L_open[j][1]]+100:
                    L_open[j][4]=L_open[j][4]+' '+str(map[L_open[j][0]][L_open[j][1]] )
                    L_open[j][3]=L_open[j][3]+'P'
                y+=1
            x+=1
   

    #print(L_open[j])
            
    #Check if the goal was achieved, Goal test
    if map[L_open[j][0]][L_open[j][1]]==3:
        solution=L_open[j][3]
        print(L_open[j][4])
        end=0
        break
    else:
        #Path and switch handling
        if((map[L_open[j][0]+1][L_open[j][1]] != 0 and map[L_open[j][0]+1][L_open[j][1]] < 200)):
            distance=dist(L_open[j][0]+1,L_open[j][1], x_goal, y_goal )
            L_open=L_open+[[L_open[j][0]+1,L_open[j][1],distance,L_open[j][3]+'D', L_open[j][4]+'']]
            
       
        if((map[L_open[j][0]-1][L_open[j][1]] != 0 and map[L_open[j][0]-1][L_open[j][1]] < 200)):
            distance=dist(L_open[j][0]-1,L_open[j][1], x_goal, y_goal )
            L_open=L_open+[[L_open[j][0]-1,L_open[j][1], distance,L_open[j][3]+'U',L_open[j][4]+'']]
   
        if((map[L_open[j][0]][L_open[j][1]+1] != 0 and map[L_open[j][0]][L_open[j][1]+1] < 200)):
            distance=dist(L_open[j][0],L_open[j][1]+1, x_goal, y_goal )
            L_open=L_open+[[L_open[j][0],L_open[j][1]+1, distance,L_open[j][3]+'R', L_open[j][4]+'']]
     
        if((map[L_open[j][0]][L_open[j][1]-1] != 0 and map[L_open[j][0]][L_open[j][1]-1] < 200)):
            distance=dist(L_open[j][0],L_open[j][1]-1, x_goal, y_goal )
            L_open=L_open+[[L_open[j][0],L_open[j][1]-1,distance,L_open[j][3]+'L', L_open[j][4]+'']]
   
        #Door handling
            
        if(map[L_open[j][0]+1][L_open[j][1]] <300 and switches(str(map[L_open[j][0]+1][L_open[j][1]]-100),L_open[j][4])!=0 and map[L_open[j][0]+1][L_open[j][1]] >199):      
            distance=dist(L_open[j][0]+1,L_open[j][1], x_goal, y_goal )
            L_open=L_open+[[L_open[j][0]+1,L_open[j][1],distance,L_open[j][3]+'D', L_open[j][4]+'']]

        if((map[L_open[j][0]+1][L_open[j][1]] > 299) and switches(str(map[L_open[j][0]+1][L_open[j][1]]-200),L_open[j][4])==0):
            distance=dist(L_open[j][0]+1,L_open[j][1], x_goal, y_goal)
            L_open=L_open+[[L_open[j][0]+1,L_open[j][1],distance,L_open[j][3]+'D', L_open[j][4]+'']]


       
        if(map[L_open[j][0]-1][L_open[j][1]] <300 and switches(str(map[L_open[j][0]-1][L_open[j][1]]-100),L_open[j][4])!=0 and map[L_open[j][0]-1][L_open[j][1]] >199):
            distance=dist(L_open[j][0]-1,L_open[j][1], x_goal, y_goal )
            L_open=L_open+[[L_open[j][0]-1,L_open[j][1], distance,L_open[j][3]+'U', L_open[j][4]+'']]

        if((map[L_open[j][0]-1][L_open[j][1]] > 299) and switches(str(map[L_open[j][0]-1][L_open[j][1]]-200),L_open[j][4])==0):
            distance=dist(L_open[j][0]-1,L_open[j][1], x_goal, y_goal )
            L_open=L_open+[[L_open[j][0]-1,L_open[j][1],distance,L_open[j][3]+'U', L_open[j][4]+'']]    


        if(map[L_open[j][0]][L_open[j][1]+1] <300 and switches(str(map[L_open[j][0]][L_open[j][1]+1]-100),L_open[j][4])!=0 and map[L_open[j][0]][L_open[j][1]+1] >199):
            distance=dist(L_open[j][0],L_open[j][1]+1, x_goal, y_goal )
            L_open=L_open+[[L_open[j][0],L_open[j][1]+1, distance,L_open[j][3]+'R', L_open[j][4]+'']]
           

        if((map[L_open[j][0]][L_open[j][1]+1] > 299) and switches(str(map[L_open[j][0]][L_open[j][1]+1]-200),L_open[j][4])==0):
            distance=dist(L_open[j][0],L_open[j][1]+1, x_goal, y_goal )
            L_open=L_open+[[L_open[j][0],L_open[j][1]+1, distance,L_open[j][3]+'R', L_open[j][4]+'']]
           
     
        if(map[L_open[j][0]][L_open[j][1]-1] <300 and switches(str(map[L_open[j][0]][L_open[j][1]-1]-100),L_open[j][4])!=0 and map[L_open[j][0]][L_open[j][1]-1] >199):
            distance=dist(L_open[j][0],L_open[j][1]-1, x_goal, y_goal )
            L_open=L_open+[[L_open[j][0],L_open[j][1]-1,distance,L_open[j][3]+'L', L_open[j][4]+'']]    

        if((map[L_open[j][0]][L_open[j][1]-1] > 299) and switches(str(map[L_open[j][0]][L_open[j][1]-1]-200),L_open[j][4])==0):
            distance=dist(L_open[j][0],L_open[j][1]-1, x_goal, y_goal )
            L_open=L_open+[[L_open[j][0],L_open[j][1]-1,distance,L_open[j][3]+'L', L_open[j][4]+'']]    


    #print(L_open[j])
    L_closed=L_closed+[L_open[j]]
    del L_open[j]
      
     #Check if the node in iteration 'n' is the same place as the node in past iterations and if the same number of buttons was pressed,only if it is in the same position and it has the same number of buttons it will be deleted
    foo=0
    list_lenght_open=len(L_open)
    list_lenght_closed=len(L_closed)

 
   
    while foo < list_lenght_open:
     i=0
     while i < list_lenght_closed:
      if L_open != []:
   
       if (L_open[foo][0] == L_closed[i][0] and L_open[foo][1] == L_closed[i][1]):
        if xpto(L_open[foo][4],L_closed[i][4])==1:
          #print('delete'+str(L_open[foo]))
          del(L_open[foo])
          list_lenght_open=list_lenght_open-1
          foo=foo-1
      i+=1
     foo+=1
     
    

  
    

    

#save(lines, columns, solution)
print('##########SUCESSO##########')
print(solution)
print(iteration)
#print(iteration)
