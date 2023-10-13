import random
from init import Ship
from bot_strategies import *
import matplotlib.pyplot as plt
from tqdm import tqdm
import time


def calculate_mean(lst):
    if len(lst) == 0:
        return None 

    total = sum(lst)
    mean = total / len(lst)
    return mean


def bot1_main(N):
    # init ship

    print("Evaluate Bot1 with N: {}".format(N))
    K_list = range(1, N*N//2)

    crew_rescued_num_list_with_different_K = []
    survive_timestep_num_list_with_different_K = []

    for K in tqdm(K_list):
        
        crew_rescued_num_list_with_same_K = []
        survive_timestep_num_list_with_same_K = []
        
        for episode in range(10):

            Our_Ship = Ship(N)
            Our_Ship.Create_Ship()
            Our_Ship.Put_crew_alien_bot(K)
            # Our_Ship.Show_Ship()

            time_step = 0
            crew_rescued_num = 0
            if_be_captured = 0
            
            while(time_step <= 1000 and if_be_captured == 0):

                time_1 = time.time()
                bot1_route, note = Bot_1_stratgy(Our_Ship)
                time_2 = time.time()
                # if time_2 - time_1 > 10:
                #     Our_Ship.Show_Ship()
                    # print(bot1_route)
                    # print(note)
                    # print(Our_Ship.alien_pos_after_move(move=False))

                for step, bot_pos in enumerate(bot1_route):

                    time_step+=1
                    if step == 0 and len(bot1_route) > 1:
                        continue
                    else:
                        Our_Ship.bot_move(bot_pos)
                        # Our_Ship.Show_Ship()
                        alien_pos_list = Our_Ship.alien_pos_after_move()                        
                        
                        if bot_pos in alien_pos_list:
                            if_be_captured = 1
                            break

                        elif bot_pos == (Our_Ship.crew.x, Our_Ship.crew.y):
                            crew_rescued_num += 1

                        else:
                            continue

                # generate a new crew
                while (True):
                    Our_Ship.Ship_matrix[Our_Ship.crew.x][Our_Ship.crew.y].if_Crew = 0
                    crew_x, crew_y = random.randint(0, Our_Ship.N - 1), random.randint(0, Our_Ship.N - 1)
                    if Our_Ship.Ship_matrix[crew_x][crew_y].state == 'open':
                        Our_Ship.Ship_matrix[crew_x][crew_y].if_Crew = 1
                        Our_Ship.crew.x = crew_x
                        Our_Ship.crew.y = crew_y
                        break
                    else:
                        continue
        

            survive_timestep_num_list_with_same_K.append(time_step)
            crew_rescued_num_list_with_same_K.append(crew_rescued_num)

        mean_survive_timestep_num = calculate_mean(survive_timestep_num_list_with_same_K)
        mean_crew_rescued_num = calculate_mean(crew_rescued_num_list_with_same_K)

        # print("", K, crew_rescued_num_list_with_same_K)
        survive_timestep_num_list_with_different_K.append(mean_survive_timestep_num)
        crew_rescued_num_list_with_different_K.append(mean_crew_rescued_num)
    
    # Plot average_crew_rescued_num with K
    print("crew_rescued_num_list_with_different_K: ", crew_rescued_num_list_with_different_K)
    print("survive_timestep_num_list_with_different_K: ", survive_timestep_num_list_with_different_K)
    x = list(range(1, len(crew_rescued_num_list_with_different_K)+1))

    plt.figure(figsize=(15, 6))
    plt.subplot(1, 2, 1)

    # 绘制曲线图
    plt.plot(x, crew_rescued_num_list_with_different_K, marker='o', linestyle='-', color='green')
    plt.title('Crew Rescued Number by Bot1 with Different K (N: {})'.format(N))
    plt.xlabel('Alien num(K)')
    plt.ylabel('Average Crew Rescued Number')
    plt.grid(True)

    plt.subplot(1, 2, 2)

    # 绘制曲线图
    plt.plot(x, survive_timestep_num_list_with_different_K, marker='o', linestyle='-', color='orange')
    plt.title('Survive Timestep Number by Bot1 with Different K (N: {})'.format(N))
    plt.xlabel('Alien num(K)')
    plt.ylabel('Average Survive Timestep Number')
    plt.grid(True)

    # # save
    # plt.savefig('crew_rescued_plot.png')

    plt.show()


def bot2_main(N):
    # init ship
    print("Evaluate Bot2 with N: {}".format(N))
    K_list = range(1, N * N // 2)
    crew_rescued_num_list_with_different_K = []
    survive_timestep_num_list_with_different_K = []

    for K in tqdm(K_list):
        
        crew_rescued_num_list_with_same_K = []
        survive_timestep_num_list_with_same_K = []

        for episode in range(10):
            Our_Ship = Ship(N)
            Our_Ship.Create_Ship()
            Our_Ship.Put_crew_alien_bot(K)

            time_step = 0
            crew_rescued_num = 0
            if_be_captured = 0

            while time_step <= 1000 and if_be_captured == 0:

                bot1_route, note = Bot_1_stratgy(Our_Ship)

                # print(bot1_route)
                # print(Our_Ship.alien_pos_after_move(move=False))
                # print(Our_Ship.crew.x, Our_Ship.crew.y)
                # print(Our_Ship.bot.x, Our_Ship.bot.y)

                if len(bot1_route) == 1:
                    bot_pos = bot1_route[0]  # 获取下一步移动位置
                else:
                    bot_pos = bot1_route[1]

                time_step += 1

                Our_Ship.bot_move(bot_pos)
                alien_pos_list = Our_Ship.alien_pos_after_move()

                if bot_pos in alien_pos_list:
                    if_be_captured = 1
                    break

                if bot_pos == (Our_Ship.crew.x, Our_Ship.crew.y):
                    crew_rescued_num += 1

                    while True:
                        Our_Ship.Ship_matrix[Our_Ship.crew.x][Our_Ship.crew.y].if_Crew = 0
                        crew_x, crew_y = random.randint(0, Our_Ship.N - 1), random.randint(0, Our_Ship.N - 1)
                        if Our_Ship.Ship_matrix[crew_x][crew_y].state == 'open':
                            Our_Ship.Ship_matrix[crew_x][crew_y].if_Crew = 1
                            Our_Ship.crew.x = crew_x
                            Our_Ship.crew.y = crew_y
                            break

            survive_timestep_num_list_with_same_K.append(time_step)
            crew_rescued_num_list_with_same_K.append(crew_rescued_num)

        mean_survive_timestep_num = calculate_mean(survive_timestep_num_list_with_same_K)
        mean_crew_rescued_num = calculate_mean(crew_rescued_num_list_with_same_K)

        # print("", K, crew_rescued_num_list_with_same_K)
        survive_timestep_num_list_with_different_K.append(mean_survive_timestep_num)
        crew_rescued_num_list_with_different_K.append(mean_crew_rescued_num)
    
    # Plot average_crew_rescued_num with K
    print("crew_rescued_num_list_with_different_K: ", crew_rescued_num_list_with_different_K)
    print("survive_timestep_num_list_with_different_K: ", survive_timestep_num_list_with_different_K)
    x = list(range(1, len(crew_rescued_num_list_with_different_K)+1))

    plt.figure(figsize=(15, 6))
    plt.subplot(1, 2, 1)

    # 绘制曲线图
    plt.plot(x, crew_rescued_num_list_with_different_K, marker='o', linestyle='-', color='green')
    plt.title('Crew Rescued Number by Bot2 with Different K (N: {})'.format(N))
    plt.xlabel('Alien num(K)')
    plt.ylabel('Average Crew Rescued Number')
    plt.grid(True)

    plt.subplot(1, 2, 2)

    # 绘制曲线图
    plt.plot(x, survive_timestep_num_list_with_different_K, marker='o', linestyle='-', color='orange')
    plt.title('Survive Timestep Number by Bot2 with Different K (N: {})'.format(N))
    plt.xlabel('Alien num(K)')
    plt.ylabel('Average Survive Timestep Number')
    plt.grid(True)

    # # save
    # plt.savefig('crew_rescued_plot.png')

    plt.show()
            

def bot3_main(N):
    # init ship
    print("Evaluate Bot3 with N: {}".format(N))
    K_list = range(1, N * N // 2)
    crew_rescued_num_list_with_different_K = []
    survive_timestep_num_list_with_different_K = []

    for K in tqdm(K_list):
        
        crew_rescued_num_list_with_same_K = []
        survive_timestep_num_list_with_same_K = []

        for episode in range(10):
            Our_Ship = Ship(N)
            Our_Ship.Create_Ship()
            Our_Ship.Put_crew_alien_bot(K)

            time_step = 0
            crew_rescued_num = 0
            if_be_captured = 0

            while time_step <= 1000 and if_be_captured == 0:

                bot1_route, note = Bot_3_stratgy(Our_Ship)

                # print(bot1_route)
                # print(Our_Ship.alien_pos_after_move(move=False))
                # print(Our_Ship.crew.x, Our_Ship.crew.y)
                # print(Our_Ship.bot.x, Our_Ship.bot.y)

                if len(bot1_route) == 1:
                    bot_pos = bot1_route[0]  # 获取下一步移动位置
                else:
                    bot_pos = bot1_route[1]

                time_step += 1

                # print(bot_pos)
                Our_Ship.bot_move(bot_pos)
                alien_pos_list = Our_Ship.alien_pos_after_move()
                # Our_Ship.Show_Ship()

                if bot_pos in alien_pos_list:
                    if_be_captured = 1
                    break

                if bot_pos == (Our_Ship.crew.x, Our_Ship.crew.y):
                    crew_rescued_num += 1

                    while True:
                        Our_Ship.Ship_matrix[Our_Ship.crew.x][Our_Ship.crew.y].if_Crew = 0
                        crew_x, crew_y = random.randint(0, Our_Ship.N - 1), random.randint(0, Our_Ship.N - 1)
                        if Our_Ship.Ship_matrix[crew_x][crew_y].state == 'open':
                            Our_Ship.Ship_matrix[crew_x][crew_y].if_Crew = 1
                            Our_Ship.crew.x = crew_x
                            Our_Ship.crew.y = crew_y
                            break

            survive_timestep_num_list_with_same_K.append(time_step)
            crew_rescued_num_list_with_same_K.append(crew_rescued_num)

        mean_survive_timestep_num = calculate_mean(survive_timestep_num_list_with_same_K)
        mean_crew_rescued_num = calculate_mean(crew_rescued_num_list_with_same_K)

        # print("", K, crew_rescued_num_list_with_same_K)
        survive_timestep_num_list_with_different_K.append(mean_survive_timestep_num)
        crew_rescued_num_list_with_different_K.append(mean_crew_rescued_num)
    
    # Plot average_crew_rescued_num with K
    print("crew_rescued_num_list_with_different_K: ", crew_rescued_num_list_with_different_K)
    print("survive_timestep_num_list_with_different_K: ", survive_timestep_num_list_with_different_K)
    x = list(range(1, len(crew_rescued_num_list_with_different_K)+1))

    plt.figure(figsize=(15, 6))
    plt.subplot(1, 2, 1)

    # 绘制曲线图
    plt.plot(x, crew_rescued_num_list_with_different_K, marker='o', linestyle='-', color='green')
    plt.title('Crew Rescued Number by Bot3 with Different K (N: {})'.format(N))
    plt.xlabel('Alien num(K)')
    plt.ylabel('Average Crew Rescued Number')
    plt.grid(True)

    plt.subplot(1, 2, 2)

    # 绘制曲线图
    plt.plot(x, survive_timestep_num_list_with_different_K, marker='o', linestyle='-', color='orange')
    plt.title('Survive Timestep Number by Bot3 with Different K (N: {})'.format(N))
    plt.xlabel('Alien num(K)')
    plt.ylabel('Average Survive Timestep Number')
    plt.grid(True)

    # # save
    # plt.savefig('crew_rescued_plot.png')

    plt.show()


def bot4_main(N):
    # init ship
    print("Evaluate Bot4 with N: {}".format(N))
    K_list = range(1, N * N // 2)
    crew_rescued_num_list_with_different_K = []
    survive_timestep_num_list_with_different_K = []

    for K in tqdm(K_list):
        
        crew_rescued_num_list_with_same_K = []
        survive_timestep_num_list_with_same_K = []

        for episode in range(10):
            Our_Ship = Ship(N)
            Our_Ship.Create_Ship()
            Our_Ship.Put_crew_alien_bot(K)

            time_step = 0
            crew_rescued_num = 0
            if_be_captured = 0

            while time_step <= 1000 and if_be_captured == 0:

                bot1_route, note = Bot_4_stratgy(Our_Ship)

                # print("a", bot1_route)
                # print("b", Our_Ship.alien_pos_after_move(move=False))
                # print("c", Our_Ship.crew.x, Our_Ship.crew.y)
                # print("d", Our_Ship.bot.x, Our_Ship.bot.y)

                if len(bot1_route) == 1:
                    bot_pos = bot1_route[0]  # 获取下一步移动位置
                else:
                    bot_pos = bot1_route[1]

                time_step += 1

                # print(bot_pos)
                Our_Ship.bot_move(bot_pos)
                alien_pos_list = Our_Ship.alien_pos_after_move()

                if bot_pos in alien_pos_list:
                    if_be_captured = 1
                    break

                if bot_pos == (Our_Ship.crew.x, Our_Ship.crew.y):
                    crew_rescued_num += 1

                    while True:
                        Our_Ship.Ship_matrix[Our_Ship.crew.x][Our_Ship.crew.y].if_Crew = 0
                        crew_x, crew_y = random.randint(0, Our_Ship.N - 1), random.randint(0, Our_Ship.N - 1)
                        if Our_Ship.Ship_matrix[crew_x][crew_y].state == 'open':
                            Our_Ship.Ship_matrix[crew_x][crew_y].if_Crew = 1
                            Our_Ship.crew.x = crew_x
                            Our_Ship.crew.y = crew_y
                            break

            survive_timestep_num_list_with_same_K.append(time_step)
            crew_rescued_num_list_with_same_K.append(crew_rescued_num)

        mean_survive_timestep_num = calculate_mean(survive_timestep_num_list_with_same_K)
        mean_crew_rescued_num = calculate_mean(crew_rescued_num_list_with_same_K)

        # print("", K, crew_rescued_num_list_with_same_K)
        survive_timestep_num_list_with_different_K.append(mean_survive_timestep_num)
        crew_rescued_num_list_with_different_K.append(mean_crew_rescued_num)
    
    # Plot average_crew_rescued_num with K
    print("crew_rescued_num_list_with_different_K: ", crew_rescued_num_list_with_different_K)
    print("survive_timestep_num_list_with_different_K: ", survive_timestep_num_list_with_different_K)
    x = list(range(1, len(crew_rescued_num_list_with_different_K)+1))

    plt.figure(figsize=(15, 6))
    plt.subplot(1, 2, 1)

    # 绘制曲线图
    plt.plot(x, crew_rescued_num_list_with_different_K, marker='o', linestyle='-', color='green')
    plt.title('Crew Rescued Number by Bot4 with Different K (N: {})'.format(N))
    plt.xlabel('Alien num(K)')
    plt.ylabel('Average Crew Rescued Number')
    plt.grid(True)

    plt.subplot(1, 2, 2)

    # 绘制曲线图
    plt.plot(x, survive_timestep_num_list_with_different_K, marker='o', linestyle='-', color='orange')
    plt.title('Survive Timestep Number by Bot4 with Different K (N: {})'.format(N))
    plt.xlabel('Alien num(K)')
    plt.ylabel('Average Survive Timestep Number')
    plt.grid(True)

    # # save
    # plt.savefig('crew_rescued_plot.png')

    plt.show()

if __name__ == '__main__':

    N = 8 

    bot1_main(N)

    bot2_main(N)

    bot3_main(N)

    # bot4_main(N)





