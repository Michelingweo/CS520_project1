import random
from matplotlib import pyplot
from matplotlib.colors import ListedColormap

class node:

    def __init__(self, x, y):

        self.x = None
        self.y = None
        self.state = 'closed'  # 0:closed, 1: open
        self.if_Crew = 0  # 0: no Crew, 1: have Crew
        self.if_Alien = 0  # 0: no Alien, 1: have Alien
        self.if_Bot = 0  # 0: no Bot, 1: have Bot
        self.if_neighbor_Alien = 0  # 0: no neighbor has Alien, 1: any neighbors has Alien


class Agent:

    def __init__(self, N):

        self.x = None
        self.y = None
        self.N = N
        self.state = 0 # 0: alien, 1: bot

    def is_valid(self, x, y):

        return 0 <= x < self.N and 0 <= y < self.N

    def up(self):

        if self.is_valid(self.x, self.y-1):
            self.y -= 1
        else:
            return

    def down(self):

        if self.is_valid(self.x, self.y+1):
            self.y += 1
        else:
            return

    def left(self):

        if self.is_valid(self.x-1, self.y):
            self.x -= 1
        else:
            return

    def right(self):

        if self.is_valid(self.x+1, self.y):
            self.x += 1
        else:
            return
    
    def stay(self):
        return
    
# create a bot class and a alien class to inherit from Agent class

    
    
    
    
    
class Ship:

    def __init__(self, N):

        self.N = N
        self.Ship_matrix = [[node(x, y) for x in range(self.N)] for y in range(self.N)]

    def is_valid(self, x, y):

        return 0 <= x < self.N and 0 <= y < self.N

    def Count_open_neighbors(self, x, y):
        count = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            if self.is_valid(x + dx, y + dy) and self.Ship_matrix[x + dx][y + dy].state == 'open':
                count += 1

        return count
    
    def put_crew_alien_bot(self, alien_num):
        # create alien instances based on Agent
        alien_list = [Agent(self.N) for _ in range(alien_num)]
        succeed_alien_num = 0
        # randomly put alien on the ship if the node is open
        while(succeed_alien_num < alien_num):
            x, y = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if self.Ship_matrix[x][y].state == 'open' and self.Ship_matrix[x][y].if_Alien == 0:
                self.Ship_matrix[x][y].if_Alien = 1
                alien_list[succeed_alien_num].x = x
                alien_list[succeed_alien_num].y = y
                succeed_alien_num += 1
            else:
                continue
            
        # randomly select an open node to put one crew
        while(True):
            crew_x, crew_y = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if self.Ship_matrix[crew_x][crew_y].state == 'open':
                self.Ship_matrix[crew_x][crew_y].if_Crew = 1
                break
            else:  
                continue
            
        # randomly select an open node to put one bot
        bot = Agent(self.N)
        while(True):
            bot_x, bot_y = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if self.Ship_matrix[bot_x][bot_y].state == 'open' and self.Ship_matrix[bot_x][bot_y].if_Alien != 1:
                self.Ship_matrix[bot_x][bot_y].if_Bot = 1
                bot.x = bot_x
                bot.y = bot_y
                break
            else:  
                continue
        
        return bot, alien_list
        
    
    def Show_Ship(self):

        # self.Ship_matrix[0][4] = 1
        # self.Ship_matrix[2][4] = 1
        # self.Ship_matrix[3][2] = 1
        # self.Ship_matrix[5][6] = 1
        custom_cmap = ListedColormap(['black', 'white', 'blue', 'red', 'green'])
        
        self.Ship_state_matrix = [[0 for _ in range(self.N)] for _ in range(self.N)]

        for x in range(self.N):

            for y in range(self.N):

                if self.Ship_matrix[x][y].state == 'open':
                    if self.Ship_matrix[x][y].if_Crew == 1:
                        self.Ship_state_matrix[x][y] = 4
                        
                    elif self.Ship_matrix[x][y].if_Alien == 1:
                        self.Ship_state_matrix[x][y] = 3
                        
                    elif self.Ship_matrix[x][y].if_Bot == 1:
                        self.Ship_state_matrix[x][y] = 2
                        
                    else:
                        self.Ship_state_matrix[x][y] = 1

                else:
                    continue

        pyplot.figure(figsize=(self.N, self.N))
        pyplot.imshow(self.Ship_state_matrix, cmap=custom_cmap)
        pyplot.show()

        # for x in range(self.N):
        #     for y in range(self.N):
        #         print(self.Ship_matrix[x][y], end="")
        #     print("")

    def Create_Ship(self):

        # Choose a random square in the interior to open
        start_x, start_y = random.randint(1, self.N - 2), random.randint(1, self.N - 2)
        self.Ship_matrix[start_x][start_y].state = 'open'

        while True:
            
            blocked_node_with_one_open_neighbor = [(i, j) for i in range(0, self.N) for j in range(0, self.N) if 
                                                    self.Ship_matrix[i][j].state == 'closed' and self.Count_open_neighbors(i, j) == 1]
            if blocked_node_with_one_open_neighbor != []:
                # randomly select a blocked node with one open neighbor
                x, y = random.choice(blocked_node_with_one_open_neighbor)
                self.Ship_matrix[x][y].state = 'open'
            else:
                break
        
        
        dead_ends = [(i, j) for i in range(0, self.N) for j in range(0, self.N) if
                     self.Ship_matrix[i][j].state == 'open' and self.Count_open_neighbors(i, j) == 1]
        
        for _ in range(len(dead_ends) // 2):
        # for (x,y) in dead_ends:
            x, y = random.choice(dead_ends)
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            neighbors = [(i, j) for i, j in neighbors if
                         self.is_valid(i, j) and self.Ship_matrix[i][j].state == 'closed']

            if neighbors:
                nx, ny = random.choice(neighbors)
                self.Ship_matrix[nx][ny].state = 'open'

        # self.Show_Ship()

        


if __name__ == '__main__':

    N = 50
    print("N = ", N)
    Our_Ship = Ship(N)
    Our_Ship.Create_Ship()
    Our_Ship.put_crew_alien_bot(10)
    Our_Ship.Show_Ship()








