import numpy

# parameters as mentioned in the assignment
orientations = moves = EAST, NORTH, WEST, SOUTH = [(1, 0), (0, -1), (-1, 0), (0, 1)]    
turns = LEFT, RIGHT = (+1, -1)
discount = numpy.float64(0.9)
error = numpy.float64(0.1)

# functions used for simulation
def turn_heading(heading, inc, headings=orientations):
    return headings[(headings.index(heading) + inc) % len(headings)]
def turn_right(heading):
    return turn_heading(heading, RIGHT)
def turn_left(heading):
    return turn_heading(heading, LEFT)

# reading input from test file
with open('input2.txt') as file:
    size = int(file.readline())
    num_of_cars = int(file.readline())
    num_of_obstacles = int(file.readline())

    obstacles = []    
    for obs in range(num_of_obstacles):
        obstacles.append([int(x) for x in file.readline().split(',')])
        
    start_positions = []
    for pos in range(num_of_cars):
        start_positions.append([int(x) for x in file.readline().split(',')])
        
    terminal_positions = []
    for pos in range(num_of_cars):
        terminal_positions.append([int(x) for x in file.readline().split(',')])

# creating a data structure to store information about each state
state = dict()
for x in range(size):
    for y in range(size):          
        state[x, y] = 1
  
with open('output.txt', 'w') as file:        
    # for each car finding optimal poicy using value iteration algorithm
    for car in range(num_of_cars):
        # initializing the reward grid with -1's
        reward_grid = [[numpy.float64(-1.0)] * size for _ in range(size)]
        # reward for obstacle = -100
        for obstacle in obstacles:
            x, y = obstacle
            reward_grid[x][y] = numpy.float64(-101.0)
        # reward for terminal position = 100
        x, y = terminal_positions[car]
        reward_grid[x][y] = numpy.float64(99.0)
        reward_grid = numpy.asarray(reward_grid)
    
        # VALUE ITERATION ALGORITHM #
    
        # initializing local variables
        policy = [[EAST] * size for _ in range(size)]
        U_0 = reward_grid.copy()
        U_1 = reward_grid.copy()
        delta = numpy.float64(1e9)
        
        # error = epsilon, discount = gamma
        while delta >= error * (1 - discount) / discount:
            U_1 = U_0.copy()
            delta = numpy.float64(0.0)
            
            # each state updating the utility function
            for s in state:
                x, y = s
                
                # initialize max_sum = - infinity
                max_sum = -1e9
                for move in moves:
                    sum = numpy.float64(0.0)
                    for orientation in orientations:
                        if move == orientation:
                            if (orientation[0] + x, orientation[1] + y) in state:
                                sum += numpy.float64(0.7) * U_1[orientation[0] + x][orientation[1] + y]
                            else:
                                sum += numpy.float64(0.7) * U_1[x][y]
                        else:
                            if (orientation[0] + x, orientation[1] + y) in state:
                                sum += numpy.float64(0.1) * U_1[orientation[0] + x][orientation[1] + y]
                            else:
                                sum += numpy.float64(0.1) * U_1[x][y]
                            
                    if sum > max_sum:
                        max_sum = sum
                        policy[x][y] = move
                
                # if the state or position is a terminal state the car stops
                # so the utility funcition is always reward at that position which is -99
                if [x, y] == terminal_positions[car]:
                    U_0[x][y] = reward_grid[x][y]    
                else:
                    # updating utility values accordinig to algorithm
                    U_0[x][y] = reward_grid[x][y] + discount * max_sum
                    if abs(U_0[x][y] - U_1[x][y]) > delta:
                        delta = abs(U_0[x][y] - U_1[x][y])
        
        # storing policy in a dictionary
        pi = {}
        for s in state:
            pi[s] = policy[s[0]][s[1]]
        pi[terminal_positions[car][0], terminal_positions[car][1]] = None
    
    
        ## simulation using policy ##
        # initialize the average reward over 10 simulations to 0
        average_reward = 0
        
        # simulate 10 times using different seeds
        for j in range(10):
            total_reward = 0
            pos = (start_positions[car][0], start_positions[car][1])
            numpy.random.seed(j)
            swerve = numpy.random.random_sample(1000000)
            k = 0
            # run till you reach terminal position
            while [pos[0], pos[1]] != terminal_positions[car]:
                move = policy[pos[0]][pos[1]]
                # 0.7 probabilty of moving according to policy, 0.1 each for other directions
                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            move = turn_right(turn_right(move))
                        else:
                            move = turn_right(move)
                    else:
                        move = turn_left(move)
                k += 1
                # update the position according to the move
                if (pos[0] + move[0], pos[1] + move[1]) in state:
                    pos = (pos[0] + move[0], pos[1] + move[1])
                
                total_reward += reward_grid[pos] 
            # average the reward over 10 simulations
            average_reward += total_reward
       
        # appending the result to ouput file along with LF character
        file.write(str(int(average_reward / 10)) + '\n')
