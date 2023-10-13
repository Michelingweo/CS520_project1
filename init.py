import random
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from collections import deque
from bot_strategies import Bot_1_stratgy
import numpy as np
import time


class node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'closed'  # 0:closed, 1: open
        self.if_Crew = 0  # 0: no Crew, 1: have Crew
        self.if_Alien = 0  # 0: no Alien, 1: have Alien
        self.if_Bot = 0  # 0: no Bot, 1: have Bot
        self.if_neighbor_Alien = 0  # 0: no neighbor has Alien, 1: any neighbors has Alien
        self.neighbor_Alien_num = 0 


class Agent:

    def __init__(self, N):

        self.x = None
        self.y = None
        self.N = N

    def is_valid(self, x, y, ship_matrix):

        return 0 <= x < self.N and 0 <= y < self.N and ship_matrix[x][
            y].state == 'open' and ship_matrix[x][y].if_Alien == 0

    def up(self, ship_matrix):

        if self.is_valid(self.x, self.y + 1, ship_matrix):
            self.y += 1
            return True
        else:
            return False

    def down(self, ship_matrix):

        if self.is_valid(self.x, self.y - 1, ship_matrix):
            self.y -= 1
            return True
        else:
            return False

    def left(self, ship_matrix):

        if self.is_valid(self.x - 1, self.y, ship_matrix):
            self.x -= 1
            return True
        else:
            return False

    def right(self, ship_matrix):

        if self.is_valid(self.x + 1, self.y, ship_matrix):
            self.x += 1
            return True
        else:
            return False

    def stay(self):
        return


class Alien(Agent):

    def __init__(self, N):
        super().__init__(N)

    def Alien_Random_action(self, ship_matrix):

        flag = False
        while(flag == False):

            random_action = random.randint(1, 5)

            if random_action == 1:
                flag = self.up(ship_matrix)

            elif random_action == 2:
                flag = self.down(ship_matrix)

            elif random_action == 3:
                flag = self.left(ship_matrix)

            elif random_action == 4:
                flag = self.right(ship_matrix)
            else:
                flag = True


class Bot(Agent):

    def __init__(self, N):
        super().__init__(N)


class Ship:

    def __init__(self, N):

        self.N = N
        self.Ship_matrix = [[node(x, y) for x in range(self.N)]
                            for y in range(self.N)]

    def is_valid(self, x, y):

        return 0 <= x < self.N and 0 <= y < self.N

    def Count_open_neighbors(self, x, y):
        count = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            if self.is_valid(
                    x + dx, y +
                    dy) and self.Ship_matrix[x + dx][y + dy].state == 'open':
                count += 1

        return count

    def Get_Neighbor_nodes(self, x, y):

        Neighbor_nodes_list = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            if self.is_valid(
                    x + dx, y +
                    dy) and self.Ship_matrix[x + dx][y + dy].state == 'open':

                Neighbor_nodes_list.append((x + dx, y + dy))

        return Neighbor_nodes_list

    def Update_Ship_matrix_if_neighbor_Alien(self):

        # set all node.if_neighbor_Alien = 0
        for x in range(self.N):
            for y in range(self.N):
                self.Ship_matrix[x][y].if_neighbor_Alien = 0
                self.Ship_matrix[x][y].neighbor_Alien_num = 0

        for x in range(self.N):
            for y in range(self.N):

                Neighbor_nodes_list = self.Get_Neighbor_nodes(x, y)

                for neighbor_x, neighbor_y in Neighbor_nodes_list:

                    if self.Ship_matrix[neighbor_x][neighbor_y].if_Alien == 1:

                        self.Ship_matrix[x][y].neighbor_Alien_num += 1

                if self.Ship_matrix[x][y].if_Alien == 1:

                    for neighbor_x, neighbor_y in Neighbor_nodes_list:
                        self.Ship_matrix[neighbor_x][neighbor_y].if_neighbor_Alien = 1

    def Put_crew_alien_bot(self, alien_num):
        # create alien instances based on Agent
        alien_list = [Alien(self.N) for _ in range(alien_num)]
        succeed_alien_num = 0
        # randomly put alien on the ship if the node is open
        while (succeed_alien_num < alien_num):
            x, y = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if self.Ship_matrix[x][y].state == 'open' and self.Ship_matrix[x][
                    y].if_Alien == 0:
                self.Ship_matrix[x][y].if_Alien = 1
                alien_list[succeed_alien_num].x = x
                alien_list[succeed_alien_num].y = y
                succeed_alien_num += 1
            else:
                continue

        self.Update_Ship_matrix_if_neighbor_Alien()

        # randomly select an open node to put one crew
        crew = Agent(self.N)
        while (True):
            crew_x, crew_y = random.randint(0, self.N - 1), random.randint(
                0, self.N - 1)
            if self.Ship_matrix[crew_x][crew_y].state == 'open':
                self.Ship_matrix[crew_x][crew_y].if_Crew = 1
                crew.x = crew_x
                crew.y = crew_y
                break
            else:
                continue

        # randomly select an open node to put one bot
        bot = Bot(self.N)
        while (True):
            bot_x, bot_y = random.randint(0, self.N - 1), random.randint(
                0, self.N - 1)
            if self.Ship_matrix[bot_x][
                    bot_y].state == 'open' and self.Ship_matrix[bot_x][
                        bot_y].if_Alien != 1:
                self.Ship_matrix[bot_x][bot_y].if_Bot = 1
                bot.x = bot_x
                bot.y = bot_y
                break
            else:
                continue

        self.bot = bot
        self.crew = crew
        self.alien_list = alien_list

        return

    def Show_Ship(self):

        custom_cmap = ListedColormap(
            ['black', 'white', 'blue', 'red', 'green'])

        self.Ship_state_matrix = [[0 for _ in range(self.N)]
                                  for _ in range(self.N)]

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

        self.Ship_state_matrix = np.array(self.Ship_state_matrix)
        self.Ship_state_matrix = np.transpose(self.Ship_state_matrix)

        print(self.Ship_state_matrix)

        plt.figure(figsize=(self.N, self.N))
        plt.imshow(self.Ship_state_matrix, cmap=custom_cmap, origin='lower')
        plt.show()
        time.sleep(2)  # 等待2秒
        plt.close()

    def Create_Ship(self):

        # Choose a random square in the interior to open
        start_x, start_y = random.randint(1, self.N - 2), random.randint(
            1, self.N - 2)
        self.Ship_matrix[start_x][start_y].state = 'open'

        while True:

            blocked_node_with_one_open_neighbor = [
                (i, j) for i in range(0, self.N) for j in range(0, self.N)
                if self.Ship_matrix[i][j].state == 'closed'
                and self.Count_open_neighbors(i, j) == 1
            ]
            if blocked_node_with_one_open_neighbor != []:
                # randomly select a blocked node with one open neighbor
                x, y = random.choice(blocked_node_with_one_open_neighbor)
                self.Ship_matrix[x][y].state = 'open'
            else:
                break

        dead_ends = [(i, j) for i in range(0, self.N)
                     for j in range(0, self.N)
                     if self.Ship_matrix[i][j].state == 'open'
                     and self.Count_open_neighbors(i, j) == 1]

        for _ in range(len(dead_ends) // 2):
            # for (x,y) in dead_ends:
            x, y = random.choice(dead_ends)
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            neighbors = [(i, j) for i, j in neighbors if self.is_valid(i, j)
                         and self.Ship_matrix[i][j].state == 'closed']

            if neighbors:
                nx, ny = random.choice(neighbors)
                self.Ship_matrix[nx][ny].state = 'open'

        # self.Show_Ship()

    def bot_move(self, new_pos):
        self.Ship_matrix[self.bot.x][self.bot.y].if_Bot = 0

        self.bot.x = new_pos[0]
        self.bot.y = new_pos[1]
        self.Ship_matrix[new_pos[0]][new_pos[1]].if_Bot = 1

    def alien_pos_after_move(self, move=True):

        alien_pos = []
        for alien in self.alien_list:
            if move:
                # remove original indicator
                self.Ship_matrix[alien.x][alien.y].if_Alien = 0

                #random move
                alien.Alien_Random_action(self.Ship_matrix)

                #new indicator
                self.Ship_matrix[alien.x][alien.y].if_Alien = 1

            alien_pos.append((alien.x, alien.y))

        self.Update_Ship_matrix_if_neighbor_Alien()

        return alien_pos

    def Identify_whether_crew_be_surrounded(self):

        Neighbor_nodes = self.Get_Neighbor_nodes(self.crew.x, self.crew.y)

        available_nodes_num = 0
        for x, y in Neighbor_nodes:
            
            if self.Ship_matrix[x][y].if_Alien == 0:

                available_nodes_num +=1
        
        if available_nodes_num > 0:
            return False
        else:
            return True
        
    def Identify_whether_bot_be_surrounded(self):

        Neighbor_nodes = self.Get_Neighbor_nodes(self.bot.x, self.bot.y)

        available_nodes_num = 0
        for x, y in Neighbor_nodes:
            
            if self.Ship_matrix[x][y].if_Alien == 0:

                available_nodes_num +=1
        
        if available_nodes_num > 0:
            return False
        else:
            return True


if __name__ == '__main__':

    N = 10
    K = 2
    print("N = ", N)
    Our_Ship = Ship(N)
    Our_Ship.Create_Ship()
    Our_Ship.Put_crew_alien_bot(K)
    Our_Ship.Show_Ship()

    route = Bot_1_stratgy(Our_Ship)
    print(route)
