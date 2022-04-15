# -*- coding: utf-8 -*-
from __future__ import print_function
import time
import random
import paho.mqtt.client as mqtt
"""Copy of P'Toon of astar.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1boKMzkxMnpKKD_OsmNE__TW9XB6UMltj

# **What???**
"""

import pandas as pd
from operator import itemgetter
import random

# 0 are free path whereas 1's are obstacles
grid = [[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]]

# print(grid.shape)

init = [6, 0]
# goal = [len(grid)-1, len(grid[0])-1] #all coordinates are given in format [y,x]
goal = [6, 6]

cost = 1

# the cost map which pushes the path closer to the goal
heuristic = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
for i in range(len(grid)):
    for j in range(len(grid[0])):
        heuristic[i][j] = abs(i - goal[0]) + abs(j - goal[1])

# the actions we can take
delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right


# function to search the path
def search(grid, init, goal, cost, heuristic):
    closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]  # the referrence grid
    closed[init[0]][init[1]] = 1
    action = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]  # the action grid

    x = init[0]
    y = init[1]
    g = 0

    f = g + heuristic[init[0]][init[0]]
    cell = [[f, g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False  # flag set if we can't find expand

    while not found and not resign:
        if len(cell) == 0:
            resign = True
            return "FAIL"
        else:
            cell.sort()  # to choose the least costliest action so as to move closer to the goal
            cell.reverse()
            next = cell.pop()
            x = next[2]
            y = next[3]
            g = next[1]
            f = next[0]

            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):  # to try out different valid actions
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            f2 = g2 + heuristic[x2][y2]
                            cell.append([f2, g2, x2, y2])
                            closed[x2][y2] = 1
                            action[x2][y2] = i
    invpath = []
    x = goal[0]
    y = goal[1]
    invpath.append([x, y])  # we get the reverse path from here
    while x != init[0] or y != init[1]:
        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        x = x2
        y = y2
        invpath.append([x, y])

    path = []
    for i in range(len(invpath)):
        path.append(invpath[len(invpath) - 1 - i])
    #print("ACTION MAP")
    for i in range(len(action)):
       #print(action[i])

        return path


a = search(grid, init, goal, cost, heuristic)
#for i in range(len(a)):
#print(a[i])

"""# **MQTT Input**"""

pos_patience = "2,3,1|3,1,3|1,4,2|2,5,1|1,2,3"
pos = pos_patience.split('|')
#print(pos)
#print(pos[0])

cool = []
for i in pos:
    i = i.split(',')
    cool.append(i)
#print(cool)

cool = sorted(cool, key=itemgetter(2))
cool

#print(int(cool[0][0]))

position = []
for i in range(0, 5):
    for j in range(0, 3):
        abc = int(cool[i][j])
        position.append(abc)
#print(position)

position[12:14]

"""# **Function**"""

Initial_point_Y = 6
Initial_point_X = 3
patient_Gonnadie_X = position[13]
patient_Gonnadie_Y = position[12]
patient_ICU_X = position[10]
patient_ICU_Y = position[9]
patient_Ambulance_X = position[7]
patient_Ambulance_Y = position[6]
patient_Self_isolate_X = position[4]
patient_Self_isolate_Y = position[3]
patient_Smile_X = position[1]
patient_Smile_Y = position[0]

# Add more place

init_goal_pairs = [((Initial_point_Y, Initial_point_X), (patient_Gonnadie_Y, patient_Gonnadie_X)),
                   ((patient_Gonnadie_Y, patient_Gonnadie_X), (patient_ICU_Y, patient_ICU_X)),
                   ((patient_ICU_Y, patient_ICU_X), (patient_Ambulance_Y, patient_Ambulance_X)),
                   ((patient_Ambulance_Y, patient_Ambulance_X),
                    (patient_Self_isolate_Y, patient_Self_isolate_X)),
                   ((patient_Self_isolate_Y, patient_Self_isolate_X), (patient_Smile_Y, patient_Smile_X)),
                   ((patient_Smile_Y, patient_Smile_X), (Initial_point_Y, Initial_point_X))]
list_sum_path = []


def create_sring(delta_x, delta_y):
    if delta_x == -1 and delta_y == 0:
        data = "go up"
    if delta_x == 0 and delta_y == -1:
        data = "go left"
    if delta_x == 1 and delta_y == 0:
        data = "go down"
    if delta_x == 0 and delta_y == 1:
        data = "go right"
    return data


def state_check(previous, next):
    if previous == next:
        data = "forward" "forward"
    if previous == "go right" and previous == next:
        data = "forward"
    if previous == "go left" and previous == next:
        data = "forward"
    if previous == "go down":
        data = "turn around"


for init, goal in init_goal_pairs:
    path = search(grid, init, goal, cost, heuristic)
    #print("this is path", path)
    # print(len(path))
    list_path = []
    for i in range(len(path) - 1):
        x = path[i]
        x1 = x[0]
        x2 = x[1]
        # print(x1 , x2)
        y = path[i + 1]
        y1 = y[0]
        y2 = y[1]
        # print(y1 , y2)

        delta_x = y1 - x1
        delta_y = y2 - x2
        # print(delta_x)
        # print(delta_y)
        command = create_sring(delta_x, delta_y)

        list_path.append(command)
        # list_path.append(([delta_x,delta_y]))
    # list_path.append("heal")
    list_sum_path.append(list_path)


def state_check2(previous, next):
    data = ""
    if previous == "go up" and next == "go up":
        data = ["FW"]
    if previous == "go up" and next == "go right":
        data = ["RW", "FW"]
    if previous == "go up" and next == "go left":
        data = ["LW", "FW"]
    if previous == "go up" and next == "go down":
        data = ["TA", "FW"]
    if previous == "go down" and next == "go down":
        data = ["FW"]
    if previous == "go down" and next == "go right":
        data = ["LW", "FW"]
    if previous == "go down" and next == "go left":
        data = ["RW", "FW"]
    if previous == "go down" and next == "go up":
        data = ["TA", "FW"]
    if previous == "go right" and next == "go right":
        data = ["FW"]
    if previous == "go right" and next == "go up":
        data = ["LW", "FW"]
    if previous == "go right" and next == "go down":
        data = ["RW", "FW"]
    if previous == "go right" and next == "go left":
        data = ["TA", "FW"]
    if previous == "go left" and next == "go left":
        data = ["FW"]
    if previous == "go left" and next == "go up":
        data = ["RW", "FW"]
    if previous == "go left" and next == "go down":
        data = ["LW", "FW"]
    if previous == "go left" and next == "go right":
        data = ["TA", "FW"]
    if previous == "go up" and next == "heal":
        data = ["heal left 30"]
    if previous == "go down" and next == "heal":
        data = ["heal right 90"]
    if previous == "go right" and next == "heal":
        data = ["heal left 90"]
    if previous == "go left" and next == "heal":
        data = ["heal right 30"]

    # filled code
    if previous == 'heal' and next == 'go left':
        data = []
    if previous == 'heal' and next == 'go up':
        data = []
    if previous == 'heal' and next == 'go down':
        data = []
    if previous == 'heal' and next == 'go right':
        data = []
    return data


list_path

list_sum_path

list_sum_path[0][::-1][0]

"""# **Create pathplanning**"""

tmp = "go up"
list_command1 = []

for j in range(len(list_sum_path[0])):

    # print(tmp)
    x = state_check2(tmp, list_sum_path[0][j])
    if len(x) == 1:
        list_command1.append(x[0])
    if len(x) == 2:
        list_command1.append(x[0])
        list_command1.append(x[1])
    # tmp = list_sum_path[i][j]
    # print(x)
    # list_command.append(x)
    if x == "heal right 30" or x == "heal right 90" or x == "heal left 30" or x == "heal left 90":
        continue
    else:
        #print(tmp, list_sum_path[0][j])
        tmp = list_sum_path[0][j]

list_command1

tmp = "go left"
list_command2 = []

for j in range(len(list_sum_path[1])):

    # print(tmp)
    x = state_check2(tmp, list_sum_path[1][j])
    if len(x) == 1:
        list_command2.append(x[0])
    if len(x) == 2:
        list_command2.append(x[0])
        list_command2.append(x[1])
    # tmp = list_sum_path[i][j]
    # print(x)
    # list_command.append(x)
    if x == "heal right 30" or x == "heal right 90" or x == "heal left 30" or x == "heal left 90":
        continue
    else:
        #print(tmp, list_sum_path[1][j])
        tmp = list_sum_path[1][j]

list_command2

tmp = "go left"
list_command3 = []

for j in range(len(list_sum_path[2])):

    # print(tmp)
    x = state_check2(tmp, list_sum_path[2][j])
    if len(x) == 1:
        list_command3.append(x[0])
    if len(x) == 2:
        list_command3.append(x[0])
        list_command3.append(x[1])
    # tmp = list_sum_path[i][j]
    # print(x)
    # list_command.append(x)
    if x == "heal right 30" or x == "heal right 90" or x == "heal left 30" or x == "heal left 90":
        continue
    else:
        #print(tmp, list_sum_path[2][j])
        tmp = list_sum_path[2][j]

list_command3

tmp = "go up"
list_command4 = []

for j in range(len(list_sum_path[3])):

    # print(tmp)
    x = state_check2(tmp, list_sum_path[3][j])
    if len(x) == 1:
        list_command4.append(x[0])
    if len(x) == 2:
        list_command4.append(x[0])
        list_command4.append(x[1])
    # tmp = list_sum_path[i][j]
    # print(x)
    # list_command.append(x)
    if x == "heal right 30" or x == "heal right 90" or x == "heal left 30" or x == "heal left 90":
        continue
    else:
        #print(tmp, list_sum_path[3][j])
        tmp = list_sum_path[3][j]

list_command4

tmp = "go down"
list_command5 = []

for j in range(len(list_sum_path[4])):

    # print(tmp)
    x = state_check2(tmp, list_sum_path[4][j])
    if len(x) == 1:
        list_command5.append(x[0])
    if len(x) == 2:
        list_command5.append(x[0])
        list_command5.append(x[1])
    # tmp = list_sum_path[i][j]
    # print(x)
    # list_command.append(x)
    if x == "heal right 30" or x == "heal right 90" or x == "heal left 30" or x == "heal left 90":
        continue
    else:
        #print(tmp, list_sum_path[4][j])
        tmp = list_sum_path[4][j]

list_command5

tmp = "go left"
list_command6 = []

for j in range(len(list_sum_path[5])):

    # print(tmp)
    x = state_check2(tmp, list_sum_path[5][j])
    if len(x) == 1:
        list_command6.append(x[0])
    if len(x) == 2:
        list_command6.append(x[0])
        list_command6.append(x[1])
    # tmp = list_sum_path[i][j]
    # print(x)
    # list_command.append(x)
    if x == "heal right 30" or x == "heal right 90" or x == "heal left 30" or x == "heal left 90":
        continue
    else:
        #print(tmp, list_sum_path[5][j])
        tmp = list_sum_path[5][j]

list_command6

tmp = "go up"
list_command = []
for i in range(len(list_sum_path)):
    for j in range(len(list_sum_path[i])):

        # print(tmp)
        x = state_check2(tmp, list_sum_path[i][j])
        if len(x) == 1:
            list_command.append(x[0])
        if len(x) == 2:
            list_command.append(x[0])
            list_command.append(x[1])
        # tmp = list_sum_path[i][j]
        # print(x)
        # list_command.append(x)
        if x == "heal right 30" or x == "heal right 90" or x == "heal left 30" or x == "heal left 90":
            continue
        else:
            #print(tmp, list_sum_path[i][j])
            tmp = list_sum_path[i][j]

list_command

#print(list_command1, list_command2, list_command3, list_command4, list_command5, list_command6)

"""# **Almost Done**"""

list_command1

list_command1[::-1][0]

type(list_command1)

#print(list_command1, list_command2, list_command3, list_command4, list_command5, list_command6)

list_command

# fruits = ["Apple", "Banana"]

# # 1. append()
# print(f'Current Fruits List {fruits}')

# f = input("Please enter a fruit name:\n")
# fruits.append(f)

# print(f'Updated Fruits List {fruits}')

fruits = list_command1

# 1. append()

if list_command1[::-1][0] == 'FW':
    if list_command1[::-1][1] == 'LW':
        f = 'heal right 30'
        fruits.append(f)
    elif list_command1[::-1][1] == 'RW':
        f = 'heal right 30'
        fruits.append(f)
    elif list_command1[::-1][1] == 'FW':
        f = 'heal left 30'
        fruits.append(f)

#print(f'{fruits}')

list_command1

fruits2 = list_command2

f = "heal right 30"
fruits2.append(f)

#print(f'Updated Fruits List {fruits2}')

list_command3

fruits3 = list_command3

f = "heal left 30"
fruits3.append(f)

#print(f'Updated Fruits List {fruits3}')

list_command4

fruits4 = list_command4

f = "heal right 30"
fruits4.append(f)

#print(f'Updated Fruits List {fruits4}')

list_command5

fruits5 = list_command5

f = "heal left 30"
fruits5.append(f)

#print(f'Updated Fruits List {fruits5}')

fruits6 = list_command6

fruits

fruits2

fruits3

fruits4

fruits5

fruits6

#print(fruits, fruits2, fruits3, fruits4, fruits5, fruits6)

result = fruits + fruits2 + fruits3 + fruits4 + fruits5 + fruits6
result = str(result)
print(str(result))

'''#start MQTTT sub resuly
global MSG
# while True:
    #Connection success callback

def sub_string(text):
    text = text.replace('b','')
    text = text.replace("'",'')
    res = text.split(',')
    return res

def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('machima/1/#')
    client.subscribe('machima/patient/set')

# Message receiving callback
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print(sub_string(str(msg.payload)))
#     print(res[0])

#     MSG = str(msg.payload)

client = mqtt.Client("mqtt-test")

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message

# Establish a connection
client.username_pw_set("machima", "123456")
client.connect('192.168.1.99', 1883, 60)
# Publish a message
client.publish('machima/1/',payload=result,qos=0)

#     print(MSG)

client.loop_forever()'''
















#print(type(final_fruits[0]))

# list_path
# n = 2
# for i in range(len(list_path[:6])-n+1):
#     batch = list_path[i:i+n]
#     print('Window: ', batch)
#     print("Window2:", state_check(batch[0], batch[1]))
#     # for i in range(len(path)-1):

# list_path
# n = 2
# for i in range(len(list_path)-n+1):
#     batch = list_path[i:i+n]
#     print('Window: ', batch)

# len(path)

# init_goal_pairs = [((0,0),(1,2))]


# for init, goal in init_goal_pairs:
#   path = search(grid,init,goal,cost,heuristic)
#   print("this is path", path)

# lst = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# tsl = ['g', 'f', 'e', 'd', 'c', 'b', 'a']
# n = 2

# def slicewindow(list):
#      group = []
#      for i in range(len(lst)-n+1):
#          batch = lst[i:i+n]
#          group.append(batch)
#          print('Window: ', batch)
#      #for i in range(len(group)):

#      return group

# ABC = slicewindow(lst)
# ABC

# a = pd.DataFrame(ABC)
# b = a.transpose()

# a

# b

# ABC[0]

# lst[:2][0]

# abc = lst + tsl
# abc

# sumslice = ABC[0] + ABC[1]
# sumslice