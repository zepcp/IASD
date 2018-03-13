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

 if len(aux1)<len(aux2):
  auxiliar=aux1
  aux1=aux2
  aux2=auxiliar
  
 j=0
 count=0
 check=0
 while j < len(aux1):
  i=0
  while i < len(aux2):
   if int(aux1[j]) == int(aux2[i]):
    count+=1
   i+=1
  j+=1
 if count == len(aux1) and count != 0:
  check=1
 if len(aux1) == 0 and len(aux2) == 0:
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


L_open=[[y_initial,x_initial,'','']] # Set the open list (places to explore)
L_closed=[] # Set the closed list (places already explored)

while end != 0: # Start Iterations
 # Check if any of the cells in the open list are a switch cell that wasnt switched
 j=0 # If so adds that possibility to the open list
 length=len(L_open)
 while j < length:
  if (map[L_open[j][0]][L_open[j][1]] > 99 and map[L_open[j][0]][L_open[j][1]] < 200):
   i=0
   door=0
   aux=str.split(L_open[j][3])
   while i < len(aux):
    if map[L_open[j][0]][L_open[j][1]] == int(aux[i]):
     door=1
    i+=1
   if door == 0:
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
 
 j=0 #Check if this node is in the same place as a node in past iterations
 list_lenght_open=len(L_open)
 list_lenght_closed=len(L_closed)
 while j < list_lenght_open:
  i=0
  while i < list_lenght_closed:
   if L_open != []:
    if (L_open[j][0] == L_closed[i][0] and L_open[j][1] == L_closed[i][1]):
     check=check_switches(L_open[j][3],L_closed[i][3])
     if check == 1:
      del(L_open[j])
      list_lenght_open=list_lenght_open-1
      if j>0:
       j=j-1
   i+=1
  j+=1

 j=0 #Check if this node didn't generate repeated solution
 list_lenght_open=len(L_open)
 while j < list_lenght_open:
  i=0
  while i < list_lenght_open:
   if (L_open != [] and i != j):
    if (L_open[j][0] == L_open[i][0] and L_open[j][1] == L_open[i][1]):
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
