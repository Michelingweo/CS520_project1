from collections import deque
import copy


class bot_4_route:

    def __init__(self, start_coordinate):
        
        self.route_record = [start_coordinate, ]
        self.route_Neighbor_Ailen_num = 0
    
    @property
    def last_node_coordinate(self):

        return self.route_record[-1]

def Bot_1_stratgy(My_Ship, optimism=False):

    if My_Ship.Identify_whether_crew_be_surrounded() and optimism == False:

        return Bot_1_stratgy(My_Ship, optimism=True)

    # print('Start to plan route')
    route_queue = deque()

    bot_coordinate = (My_Ship.bot.x, My_Ship.bot.y)
    crew_coordinate = (My_Ship.crew.x, My_Ship.crew.y)

    directions_list = [(0, 1), (0, -1), (1, 0), (-1, 0)] # right, left, down, up

    route_queue.append([bot_coordinate])  # initial route stored in queue

    counter = 0
    
    # while route_queue and counter >= 0:
    # while route_queue and counter < 100000:
    while route_queue:
        route = route_queue.popleft()
        last_coordinate = route[-1]  # last position of current route
        counter += 1
        
        if last_coordinate == crew_coordinate:
            return route, "fined a route, optimism: {}".format(optimism)  # crew rescued

        for dx, dy in directions_list:
            current_route = copy.deepcopy(route)
            child_x = last_coordinate[0] + dx
            child_y = last_coordinate[1] + dy
            
            if (child_x, child_y) in current_route:
                continue
            
            if optimism:

                if My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].state == 'open':

                    current_route.append((child_x, child_y))
                    route_queue.append(current_route)
                    # counter -= 1
                else:
                    continue
            else:
                if My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].state == 'open' and \
                    My_Ship.Ship_matrix[child_x][child_y].if_Alien != 1:

                    current_route.append((child_x, child_y))
                    route_queue.append(current_route)
                    # counter -= 1
                else:
                    continue
    
    # if counter >= 100000:
    #     return route_queue.popleft(), "something wrong!, optimism: {}".format(optimism)


    return Bot_1_stratgy(My_Ship, optimism=True)


def Bot_3_stratgy(My_Ship, optimism = False):
    
    if My_Ship.Identify_whether_crew_be_surrounded() and optimism == False:

        return Bot_1_stratgy(My_Ship, optimism=True)

    # print('Start to plan route')
    route_queue = deque()
    alienNB_queue = deque()
    
    bot_coordinate = (My_Ship.bot.x, My_Ship.bot.y)
    crew_coordinate = (My_Ship.crew.x, My_Ship.crew.y)

    directions_list = [(0, 1), (0, -1), (1, 0), (-1, 0)] # right, left, down, up

    route_queue.append([bot_coordinate])  # initial route stored in queue

    # counter = My_Ship.N * My_Ship.N
    
    # while route_queue and counter >= 0:
    while route_queue:

        route = route_queue.popleft()
        last_coordinate = route[-1]  # last position of current route\

        if last_coordinate == crew_coordinate:
            return route, "Find a best route"  # crew rescued

        for dx, dy in directions_list:
            current_route = copy.deepcopy(route)
            child_x = last_coordinate[0] + dx
            child_y = last_coordinate[1] + dy
            
            if (child_x, child_y) in current_route:
                continue
            
            if My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].if_neighbor_Alien == 1:
                alienNB_queue.append(current_route)
                continue
            
            if My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].state == 'open' and \
                My_Ship.Ship_matrix[child_x][child_y].if_Alien != 1:

                current_route.append((child_x, child_y))
                route_queue.append(current_route)
                # counter -= 1
            else:
                continue
        
    while alienNB_queue:

        route = alienNB_queue.popleft()
        last_coordinate = route[-1]  # last position of current route

        if last_coordinate == crew_coordinate:
            return route, "Find a second best route"  # crew rescued

        for dx, dy in directions_list:
            current_route = copy.deepcopy(route)
            child_x = last_coordinate[0] + dx
            child_y = last_coordinate[1] + dy
            
            if (child_x, child_y) in current_route:
                continue
            
            if My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].state == 'open' and \
                My_Ship.Ship_matrix[child_x][child_y].if_Alien != 1:

                current_route.append((child_x, child_y))
                alienNB_queue.append(current_route)
                # counter -= 1
            else:
                continue  
        
    
    return Bot_1_stratgy(My_Ship, optimism=True)


def Bot_4_hide(My_Ship):

    bot_coordinate = (My_Ship.bot.x, My_Ship.bot.y)
    crew_coordinate = (My_Ship.crew.x, My_Ship.crew.y)
    route = [bot_coordinate, ]

    if My_Ship.Identify_whether_bot_be_surrounded():

        Neighbor_nodes = My_Ship.Get_Neighbor_nodes(My_Ship.bot.x, My_Ship.bot.y)

        # print("kk1")
        return [bot_coordinate, Neighbor_nodes[0]], "find a route"

    directions_list = [(0, 1), (0, -1), (1, 0), (-1, 0)] # right, left, down, up

    if bot_coordinate == crew_coordinate:

        # print("kk2")
        return route, "fined a route" # crew rescued

    route_candidate = []
    for dx, dy in directions_list:
        current_route = copy.deepcopy(route)
        child_x = My_Ship.bot.x + dx
        child_y = My_Ship.bot.y + dy

        if My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].state == 'open' and \
            My_Ship.Ship_matrix[child_x][child_y].if_Alien != 1 and \
                My_Ship.Ship_matrix[child_x][child_y].if_neighbor_Alien != 1:

            current_route.append((child_x, child_y))

            # print("kk3")
            return current_route, "find a route"
            # counter -= 1
        elif My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].state == 'open' and \
            My_Ship.Ship_matrix[child_x][child_y].if_Alien != 1:

                current_route.append((child_x, child_y))

                route_candidate = copy.deepcopy(current_route)

        else:
            continue

    # print("kk4")
    return route_candidate, "find a route"
    

def Bot_4_stratgy(My_Ship, optimism = False):

    route_candidate_list = []
    route_candidate_list_max_num = My_Ship.N * 2
    
    if My_Ship.Identify_whether_crew_be_surrounded() and optimism == False:

        return Bot_4_hide(My_Ship)

    # print('Start to plan route')
    route_queue = deque()
    alienNB_queue = deque()
    
    bot_coordinate = (My_Ship.bot.x, My_Ship.bot.y)
    crew_coordinate = (My_Ship.crew.x, My_Ship.crew.y)

    directions_list = [(0, 1), (0, -1), (1, 0), (-1, 0)] # right, left, down, up

    route_queue.append(bot_4_route(bot_coordinate))  # initial route stored in queue

    # counter = My_Ship.N * My_Ship.N
    
    # while route_queue and counter >= 0:
    while route_queue:

        route = route_queue.popleft()
        last_coordinate = route.last_node_coordinate  # last position of current route

        if last_coordinate == crew_coordinate:

            return route.route_record, "Find a best route"  # crew rescued

        for dx, dy in directions_list:
            current_route = copy.deepcopy(route)
            child_x = last_coordinate[0] + dx
            child_y = last_coordinate[1] + dy
            
            if (child_x, child_y) in current_route.route_record:
                continue
            
            if My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].if_neighbor_Alien == 1:

                current_route.route_record.append((child_x, child_y))
                current_route.route_Neighbor_Ailen_num += My_Ship.Ship_matrix[child_x][child_y].neighbor_Alien_num
                # print(current_route.route_Neighbor_Ailen_num)
                alienNB_queue.append(current_route)
                continue
            
            if My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].state == 'open' and \
                My_Ship.Ship_matrix[child_x][child_y].if_Alien != 1:

                current_route.route_record.append((child_x, child_y))
                current_route.route_Neighbor_Ailen_num += My_Ship.Ship_matrix[child_x][child_y].neighbor_Alien_num
                # print(current_route.route_Neighbor_Ailen_num)
                route_queue.append(current_route)
                # counter -= 1
            else:
                continue
        
    # while alienNB_queue:

    #     route = alienNB_queue.popleft()
    #     # print("route_Neighbor_Ailen_num: ", route.route_Neighbor_Ailen_num)
    #     last_coordinate = route.last_node_coordinate  # last position of current route

    #     if last_coordinate == crew_coordinate:
    #         if len(route_candidate_list) > route_candidate_list_max_num:
    #             break
    #         else:
    #             route_candidate_list.append(route)
    #         continue

    #     for dx, dy in directions_list:
    #         current_route = copy.deepcopy(route)
    #         child_x = last_coordinate[0] + dx
    #         child_y = last_coordinate[1] + dy
            
    #         if (child_x, child_y) in current_route.route_record:
    #             continue
            
    #         if My_Ship.is_valid(child_x, child_y) and My_Ship.Ship_matrix[child_x][child_y].state == 'open' and \
    #             My_Ship.Ship_matrix[child_x][child_y].if_Alien != 1:

    #             current_route.route_record.append((child_x, child_y))
    #             current_route.route_Neighbor_Ailen_num += My_Ship.Ship_matrix[child_x][child_y].neighbor_Alien_num
    #             alienNB_queue.append(current_route)
    #             # counter -= 1
    #         else:
    #             continue 

    # if len(route_candidate_list) > 0:
    #     # print(len(route_candidate_list))
    #     # for route in route_candidate_list:
    #     #     print(route.route_Neighbor_Ailen_num, ",", len(route.route_record), "   ", end="")
    #     sorted_route_candidate_list = sorted(route_candidate_list, key=lambda x: x.route_Neighbor_Ailen_num)
    #     return sorted_route_candidate_list[0].route_record, "find a route with least route_Neighbor_Ailen_num"
    
    return Bot_4_hide(My_Ship)


