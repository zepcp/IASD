# Eduardo Silva nr 69916 - MEAer
# José Pereira nr 70369 - MEAer
# Version: Python 3.4.1

# FINISH FUNCTION: Check if finish
def finish(value):
    global end
    end=1
    if value==3:
     end=0
    return end

# SAVE FUNCTION: Save in output file the labyrinth solution
def save(lines, columns, solution, time):
 f = open('output.txt', 'w')
 f.write('nr of lines='+str(lines)+'\n'+'nr of columns='+str(columns))
 f.write('\nSolution:'+str(solution)+'\n'+'Computational Time: '+str(time))
 f.close() 
 return

# DOOR CLOSED FUNCTION: Check if door closed was already switched
def door_closed_switcher(y,x,switches):
 door=0 #Door is closed
 j=0
 aux=str.split(switches)
 while j < len(aux):
  if int(aux[j]) == map[y][x]-100:
   door=1 #If switch already pushed, door is open
  j+=1
 return door

# DOOR OPEN FUNCTION: Check if door open wasnt switched
def door_open_switcher(y,x,switches):
 door=1 #Door is open
 j=0
 aux=str.split(switches)
 while j < len(aux):
  if int(aux[j]) == map[y][x]-200:
   door=0 #If switch was pushed, door is now closed
  j+=1
 return door

# CHECK SWITCHES FUNCTION: Check if the same switches were pushed
def check_switches(Lopen,Lclosed):
 aux1=str.split(Lopen)
 aux2=str.split(Lclosed)
 lenght_aux1=len(aux1)
 lenght_aux2=len(aux2)

 if lenght_aux1<lenght_aux2:
  aux3=aux1
  aux1=aux2
  aux2=aux3
  
 j=0
 count=0
 check=0
 while j < lenght_aux1:
  i=0
  while i < len(aux2):
   if int(aux1[j]) == int(aux2[i]):
    count+=1
#    del(aux2[i])
#    i=i-1
   i+=1
  j+=1
 if count == lenght_aux1 and count != 0:
  check=1
 if lenght_aux1 == 0 and lenght_aux2 == 0:
  check=1
 return check

# MAIN FUNCTION
from time import time #To count computational time
initial_time = time() #Initial time

with open('inputTest7.txt') as f: # Save labyrinth in a matrix (map)
    lines, columns = [int(x) for x in f.readline().split()]
    map = [[int(x) for x in line.split()] for line in f]

i=0 #ignore empty lines in the input file
while i<lines:
    if map[i] == []:
     del (map[i])
     i=i-1
    i=i+1

solution='' # Still no solution found
x=0 # Search the initial position
while x<columns:
    y=0
    while y<lines:
        if map[y][x] == 2:
         y_initial=y
         x_initial=x
        y+=1
    x+=1
end=1 # Initial position is never the final position (2!=3)

switches=[]# Look for switch cells that might need to be switched more than 1 time (if more than 1 door for one switch)
x=0 #First see all switches
while x<columns:
    y=0
    while y<lines:
        if map[y][x] > 99 and map[y][x] < 200:
         switches=switches+[[map[y][x],0]]
        y+=1
    x+=1

i=0 #Then check how many doors are affected by each switch
while i<len(switches):
 x=0
 while x<columns:
    y=0
    while y<lines:
        if map[y][x]-100 == switches[i][0] or map[y][x]-200 == switches[i][0]:
         switches[i][1]=switches[i][1]+1
        y+=1
    x+=1
 i=i+1

L_open=[[y_initial,x_initial,'',map]] # Set the open list (places to explore)
print(L_open)
L_closed=[] # Set the closed list (places already explored)

iteration=0
while iteration < 55:
 iteration =iteration+1

 i=0
 while i<len(L_open):
  if L_open[i][2] == 'DPRPURRDDDLLLDDDDDRRRRRRRRRPLLLLLLLLLUUUUURRRUUULLD':
   print (iteration, L_open[i])
  i=i+1

# print (iteration, L_open)
#while end != 0: # Start Iterations
 # Check if any of the cells in the open list are a switch cell that might need to be switched
 j=0 # If so adds that possibility to the open list
 length=len(L_open)
 while j < length:
  if (map[L_open[j][0]][L_open[j][1]] > 99 and map[L_open[j][0]][L_open[j][1]] < 200):
   i=0
   door=0
   aux=str.split(L_open[j][3])
   while i < len(switches):
    if map[L_open[j][0]][L_open[j][1]] == int(switches[i][0]) and int(switches[i][1])>0:
     door=switches[i][1]
     k=0
     while k<len(aux):
      if int(aux[k]) == int(switches[i][0]):
       door=door-1
      k=k+1
    i+=1
   if door > 0:
    L_open=L_open+[[L_open[j][0],L_open[j][1],L_open[j][2]+'P',L_open[j][3]+' '+str(map[L_open[j][0]][L_open[j][1]])]]
    j+=1
  j+=1
  
 list_lenght=len(L_open)
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
 
 j=0 # Check for available paths with closed doors that were switched
 while j < list_lenght:
  if((map[L_open[j][0]+1][L_open[j][1]] > 199 and map[L_open[j][0]+1][L_open[j][1]] < 300 and L_open[j][3] != '')):
   door=door_closed_switcher(L_open[j][0]+1,L_open[j][1],L_open[j][3])
   if door==1:
    L_open=L_open+[[L_open[j][0]+1,L_open[j][1],L_open[j][2]+'D',L_open[j][3]]]
  if((map[L_open[j][0]-1][L_open[j][1]] > 199 and map[L_open[j][0]-1][L_open[j][1]] < 300 and L_open[j][3] != '')):
   door=door_closed_switcher(L_open[j][0]-1,L_open[j][1],L_open[j][3])
   if door==1:
    L_open=L_open+[[L_open[j][0]-1,L_open[j][1],L_open[j][2]+'U',L_open[j][3]]]
  if((map[L_open[j][0]][L_open[j][1]+1] > 199 and map[L_open[j][0]][L_open[j][1]+1] < 300 and L_open[j][3] != '')):
   door=door_closed_switcher(L_open[j][0],L_open[j][1]+1,L_open[j][3])
   if door==1:
    L_open=L_open+[[L_open[j][0],L_open[j][1]+1,L_open[j][2]+'R',L_open[j][3]]]
  if((map[L_open[j][0]][L_open[j][1]-1] > 199 and map[L_open[j][0]][L_open[j][1]-1] < 300 and L_open[j][3] != '')):
   door=door_closed_switcher(L_open[j][0],L_open[j][1]-1,L_open[j][3])
   if door==1:
    L_open=L_open+[[L_open[j][0],L_open[j][1]-1,L_open[j][2]+'L',L_open[j][3]]]
  j+=1

 j=0 # Check for available paths with open doors that werent switched
 while j < list_lenght:
  if((map[L_open[j][0]+1][L_open[j][1]] > 299 and map[L_open[j][0]+1][L_open[j][1]] < 400)):
   door=door_open_switcher(L_open[j][0]+1,L_open[j][1],L_open[j][3])
   if door==1:
    L_open=L_open+[[L_open[j][0]+1,L_open[j][1],L_open[j][2]+'D',L_open[j][3]]]
  if((map[L_open[j][0]-1][L_open[j][1]] > 299 and map[L_open[j][0]-1][L_open[j][1]] < 400)):
   door=door_open_switcher(L_open[j][0]-1,L_open[j][1],L_open[j][3])
   if door==1:
    L_open=L_open+[[L_open[j][0]-1,L_open[j][1],L_open[j][2]+'U',L_open[j][3]]]
  if((map[L_open[j][0]][L_open[j][1]+1] > 299 and map[L_open[j][0]][L_open[j][1]+1] < 400)):
   door=door_open_switcher(L_open[j][0],L_open[j][1]+1,L_open[j][3])
   if door==1:
    L_open=L_open+[[L_open[j][0],L_open[j][1]+1,L_open[j][2]+'R',L_open[j][3]]]
  if((map[L_open[j][0]][L_open[j][1]-1] > 299 and map[L_open[j][0]][L_open[j][1]-1] < 400)):
   door=door_open_switcher(L_open[j][0],L_open[j][1]-1,L_open[j][3])
   if door==1:
    L_open=L_open+[[L_open[j][0],L_open[j][1]-1,L_open[j][2]+'L',L_open[j][3]]]
  j+=1

 j=0 #Put the previous node in the closed list (places already explored)
 while j < list_lenght:
  L_closed=L_closed+[L_open[0]]
  del (L_open[0])
  j+=1

 if iteration == 49:
     print ('Antes')
     print (L_open)
 print(iteration) 
 j=0 #Check if this node is in the same place as a node in past iterations
 list_lenght_open=len(L_open)
 list_lenght_closed=len(L_closed)
 while j < list_lenght_open:
  i=0
  while i < list_lenght_closed:
   if L_open != []:
    if (L_open[j][0] == L_closed[i][0] and L_open[j][1] == L_closed[i][1]):
 #    if len(L_open[j][3])==len(L_closed[i][3]):
      check=check_switches(L_open[j][3],L_closed[i][3])
      if check == 1:
       del(L_open[j])
       list_lenght_open=list_lenght_open-1
       if j>0:
        j=j-1
   i+=1
  j+=1
  
 if iteration == 49:
     print ('Depois')
     print (L_open)
     
 j=0 #Check if this node didn't generate repeated solution
 list_lenght_open=len(L_open)
 while j < list_lenght_open:
  i=0
  while i < list_lenght_open:
   if (L_open != [] and i != j):
    if (L_open[j][0] == L_open[i][0] and L_open[j][1] == L_open[i][1]):
     if len(L_open[j][3])==len(L_open[i][3]):
      check=check_switches(L_open[j][3],L_open[i][3])
      if check == 1:
       del(L_open[i])
       list_lenght_open=list_lenght_open-1
       i=i-1
   i+=1
  j+=1

 j=0 #Check if finish, otherwise iterate again
 while j < len(L_open) and end != 0:
  end=finish (map[L_open[j][0]][L_open[j][1]])
  if end == 0:
   solution=solution+'\n'+L_open[j][2]
  j+=1

 #Check if it's still possible to finish, if not -> Solution Not Found
 if L_open == [] and list_lenght == 0 and list_lenght_open == 0:
  print ('There is no possible solution')
  solution='Not Found'
  end=0

final_time = time() #Final Time 
save(lines, columns, solution, final_time-initial_time)
print ('Computation Time:'+str(final_time-initial_time)+' sec')
print ('Labyrinth Solution:'+solution)
