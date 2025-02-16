 
# Published initially to gz_topic_name: "model/mecanum_robot/cmd_vel"  ros_type_name: "geometry_msgs/msg/Twist"
# Subscribed to 

import Slam_subscribe

pose_calculator_class = Slam_subscribe.PoseListener()

# store state in a 2-dim array, initilize according to initial motor pos
state = [3, 0]

# init eps, alpha, gamma
eps = 0.1
alpha = 1.0
gamma = 0.5

# init Q matrix, 16 rows (states), 4 columns (actions)
# set all values 0
Q = [[0 for n in range(4)] for m in range(16)]

def printQ():
    for m in range(16):
        print(Q[m])



# define method for executing actions
def do_action(action_index):
    global state
    if action_index == 0:
        # if motor A is already fully up, do nothing, else move A up
        if state[0] < 3:
            # move up and update state
            motorA.run_target(1000, motorA_pos[state[0] + 1])
            state[0] = state[0] + 1
    elif action_index == 1:
        # if motor A is already fully down, do nothing, else move A down
        if state[0] > 0:
            # move up and update state
            motorA.run_target(1000, motorA_pos[state[0] - 1])
            state[0] = state[0] - 1
    elif action_index == 2:
        # if motor B is already fully up, do nothing, else move B up
        if state[1] < 3:
            # move up and update state
            motorB.run_target(1000, motorB_pos[state[1] + 1])
            state[1] = state[1] + 1
    else:
        # if motor B is already fully down, do nothing, else move B down
        if state[1] > 0:
            # move up and update state
            motorB.run_target(1000, motorB_pos[state[1] - 1])
            state[1] = state[1] - 1

def get_reward():
    global distance_previous
    if distance_sensor.distance() < 2000:
        # valid reading
        reward = distance_sensor.distance() - distance_previous
        if (reward == 0) or (reward == 1) or (reward == -1):
            reward = 0
        distance_previous = distance_sensor.distance()
    else:
        # invalid reading, ignore
        reward = 0
    return reward

'''
for i in range(100):
    action = urandom.randint(0, 3)
    do_action(action)
    print(state, motorA_pos[state[0]], motorB_pos[state[1]], get_reward())
'''

def select_random_action():
    return urandom.randint(0, 3)

def select_max_action():
    global state
    global Q
    Q_row_index = 4 * state[0] + state[1]
    # select action with highest value in row Q_row_index
    actions = Q[Q_row_index]
    max_action_value = actions[0]
    max_action_index = 0
    for i in range(4):
        if actions[i] > max_action_value:
            # select
            max_action_value = actions[i]
            max_action_index = i        
    return max_action_index

'''
# test
Q[2] = [0.5, 0.2, -0.1, 0.5]
printQ()
state = [0,2]
print("max action:", select_max_action())
'''

# Q-Learning alg.
count_explore = 0
i = 0
while True:
    # choose action according to Q matrix
    action = select_max_action()

    # eps-greedy action selection
    if (urandom.random() < eps) and (i < 3000):
        count_explore += 1
        action = select_random_action()

    # perform action
    old_state = state
    do_action(action)

    # get reward
    reward = get_reward()

    # get Q matriy rows for old and new state
    # state changed when executing do_action()
    old_state_row = old_state[0] * 4 + old_state[1]
    new_state_row = state[0] * 4 + state[1]

    # get action value for the next maximizing action
    max_action_new= Q[new_state_row][select_max_action()]

    # update Q 
    Q[old_state_row][action] += alpha * (reward + gamma * max_action_new - Q[old_state_row][action])

    # print
    if ((i+1)%20 == 0):
        print("---")
        print("step", i, "exploration action", count_explore)
        printQ()

    print(distance_sensor.distance(), reward)

    i += 1