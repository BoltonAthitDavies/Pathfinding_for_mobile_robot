import paho.mqtt.client as mqtt

pos_patience= "0,1,3|4,5,6|7,8,9|1,2,3|9,8,7"
pos = pos_patience.split('|')
print(pos)
print(pos[0])


cool = []
for i in pos:
    i = i.split(',')
    cool.append(i)
print(cool)

print(int(cool[0][0]))

position = []
for i in range(0, 4):
    for j in range(0, 3):
         abc = int(cool[i][j])
         position.append(abc)
print(position)


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
    print("ACTION MAP")
    for i in range(len(action)):
        print(action[i])

    return path


a = search(grid, init, goal, cost, heuristic)
for i in range(len(a)):
    print(a[i])

# Add more place

init_goal_pairs = [((6, 3), (0, 3)), ((0, 3), (1, 2)), ((1, 2), (1, 4)), ((1, 4), (2, 3)), ((2, 3), (2, 5)),
                   ((2, 5), (6, 3))]
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
    list_path.append("heal")
    list_sum_path.append(list_path)

del list_sum_path[-1][-1]

def state_check2(previous, next):
  data = ""
  if previous == "go up" and next == "go up" :
    data = ["FW"]
  if previous == "go up" and next == "go right" :
    data = ["RW", "FW"]
  if previous == "go up" and next == "go left":
    data = ["LW", "FW"]
  if previous == "go up" and next == "go down":
    data = ["TA", "FW"]
  if previous == "go down" and next == "go down" :
    data = ["FW"]
  if previous == "go down" and next == "go right" :
    data =  ["LW" , "FW"]
  if previous == "go down" and next == "go left" :
    data = ["RW","FW"]
  if previous == "go down" and next == "go up" :
    data = ["TA","FW"]
  if previous == "go right" and next == "go right":
    data = ["FW"]
  if previous == "go right" and next == "go up":
    data = ["LW","FW"]
  if previous == "go right" and next == "go down":
    data = ["RW","FW"]
  if previous == "go right" and next == "go left":
    data = ["TA","FW"]
  if previous == "go left" and next == "go left":
    data = ["FW"]
  if previous == "go left" and next == "go up":
    data = ["RW","FW"]
  if previous == "go left" and next == "go down":
    data = ["LW","FW"]
  if previous == "go left" and next == "go right":
    data = ["TA","FW"]
  if previous == "go up" and next == "heal":
    data = ["heal right 30"]
  if previous == "go down" and next == "heal":
    data = ["heal left 90"]
  if previous == "go right" and next == "heal":
    data = ["heal right 90"]
  if previous == "go left" and next == "heal":
    data = ["heal left 30"]
  return data


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

result = str(list_command)

# start MQTTT sub resuly
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
    client.subscribe('machima/#')
    client.subscribe('machima/patient/set')

# Message receiving callback
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print(sub_string(str(msg.payload)))
    if msg.topic ==
    small = msg.payload
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
client.publish('machima/', payload=result, qos=0)

#     print(MSG)

client.loop_forever()



# pos_patience = str([0 1,3|1', '2', '3|4', '5', '6|7', '8', '9|1', '2', '3'])

# print(str(pos_patience))
# print(len(pos_patience))
# x1 = pos_patience[0]
# y1 = pos_patience[1]
# print(x1)
# print(y1)
#
# x2 = pos_patience[2]
# y2 = pos_patience[3]
#
# x3 = pos_patience[4]
# y3 = pos_patience[5]
#
# x4 = pos_patience[6]
# y4 = pos_patience[7]


#text = pos_patience.split(',')
#print(text)
#     res = text.split(',')