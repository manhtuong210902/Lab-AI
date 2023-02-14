from Space import *
from Constants import *


def DFS(g:Graph, sc:pygame.Surface):
    print('Implement DFS algorithm')

    open_set = [g.start]
    closed_set = []
    father = [-1]*g.get_len()

    #TODO: Implement DFS algorithm using open_set, closed_set, and father
    while(open_set):
        #lấy node đầu của đỉnh stack (danh sách mở)
        curr = open_set.pop()

        #khi node đang xét là node đích
        if g.is_goal(curr):
            g.start.set_color(orange)
            while True:
                father_node = father[curr.value]

                father_node.set_color(grey)
                g.start.set_color(orange)
                g.draw(sc)

                pygame.draw.line(sc, green, curr.get_xy(), father_node.get_xy())

                if(g.is_start(father_node)):
                    break

                curr = father_node
            return

        #nếu node đang xét đang năm trong danh sách mở thì bỏ qua
        if curr in closed_set:
            continue

        curr.set_color(yellow)
        g.draw(sc)
        #thêm node curr vào danh sách mở
        closed_set.append(curr)

        #get các neighbor code curr
        for neighbor in g.get_neighbors(curr):
            if neighbor not in closed_set:
                neighbor.set_color(red)
                father[neighbor.value] = curr
            #thmee các neighbor vào stack
            open_set.append(neighbor)

        g.goal.set_color(purple)
        curr.set_color(blue)
        g.draw(sc)
        
    raise NotImplementedError('Not implemented')

def BFS(g:Graph, sc:pygame.Surface):
    print('Implement BFS algorithm')

    open_set = [g.start] #queue
    closed_set = []  
    father = [-1]*g.get_len()

    #TODO: Implement BFS algorithm using open_set, closed_set, and father
    closed_set.append(g.start)

    while open_set:
        curr = open_set.pop(0)
        if g.is_goal(curr):
            g.start.set_color(orange)
            while True:
                father_node = father[curr.value]

                father_node.set_color(grey)
                g.start.set_color(orange)
                g.draw(sc)

                pygame.draw.line(sc, green, curr.get_xy(), father_node.get_xy())

                if(g.is_start(father_node)):
                    break

                curr = father_node
            return

       
        curr.set_color(yellow)
        g.draw(sc)

        for neighbor in g.get_neighbors(curr):
            if neighbor not in closed_set:
                closed_set.append(neighbor)
                open_set.append(neighbor)
                father[neighbor.value] = curr
                neighbor.set_color(red)

        curr.set_color(blue) 
        g.goal.set_color(purple)  
        g.draw(sc)
    raise NotImplementedError('Not implemented')


def UCS(g:Graph, sc:pygame.Surface):
    print('Implement UCS algorithm')

    open_set = {} #queue
    open_set[g.start] = 0
    closed_set:list[Node] = []
    father = [-1]*g.get_len()
    cost = [100_000]*g.get_len()
    cost[g.start.value] = 0

    #TODO: Implement UCS algorithm using open_set, closed_set, and father
    while open_set:
        #sắp xếp tăng dần tập mở theo chi phi từng node
        open_set = {k: v for k, v in sorted(open_set.items(), key=lambda item: item[1])}

        #lấy node có chi phí thấp nhất ra khỏi tập mở
        curr = next(iter(open_set))

        if g.is_goal(curr):
            g.start.set_color(orange)
            while True:
                father_node = father[curr.value]

                father_node.set_color(grey)
                g.start.set_color(orange)
                g.draw(sc)

                pygame.draw.line(sc, green, curr.get_xy(), father_node.get_xy())
                if(g.is_start(father_node)):
                    break

                curr = father_node
            return
        
        #xét màu cho node hiện tại
        curr.set_color(yellow)
        g.draw(sc)

        #xét chi phí cho node hiện tại
        cost[curr.value] = open_set[curr]
        for neighbor in g.get_neighbors(curr):
            #xét chi phí cho các node neighbor của curr
            cost[neighbor.value] = cost[curr.value] + 1
            if neighbor not in closed_set:
                closed_set.append(neighbor)
                open_set[neighbor] = cost[neighbor.value]
                father[neighbor.value] = curr
                neighbor.set_color(red)

      
        open_set.pop(curr)

        curr.set_color(blue) 
        g.goal.set_color(purple)  
        g.draw(sc)
        
    raise NotImplementedError('Not implemented')

def AStar(g:Graph, sc:pygame.Surface):
    print('Implement A* algorithm')

    open_set = {}
    open_set[g.start] = 0
    closed_set:list[Node] = []
    father = [-1]*g.get_len()
    cost = [100_000]*g.get_len()
    cost[g.start.value] = 0

    #TODO: Implement A* algorithm using open_set, closed_set, and father
    while open_set:
        curr = None

        for node in open_set.keys():
             # nếu g(node) + h(node) < g(curr) + h(curr) hoặc curr = Node thì:
            if curr == None or open_set.get(node) + g.get_heuristic(node) < open_set.get(curr) + g.get_heuristic(curr):
                curr = node

        if curr == None:
            return
        
        curr.set_color(yellow)
        g.goal.set_color(purple)
        g.draw(sc)

        if g.is_goal(curr):
            g.start.set_color(orange)
            while True:
                father_node = father[curr.value]

                father_node.set_color(grey)
                g.start.set_color(orange)
                g.draw(sc)

                pygame.draw.line(sc, green, curr.get_xy(), father_node.get_xy())
                if(g.is_start(father_node)):
                    break

                curr = father_node
            return

        for neighbor in g.get_neighbors(curr):
            if neighbor not in open_set.keys() and neighbor not in closed_set:
                open_set[neighbor] = open_set[curr] + 1
                cost[neighbor.value] = cost[curr.value] + 1
                father[neighbor.value] = curr 
                neighbor.set_color(red)
            else:
                if cost[neighbor.value] > cost[curr.value] + 1:
                    cost[neighbor.value] = cost[curr.value] + 1
                    father[neighbor.value] = curr
                    if neighbor in closed_set:
                        closed_set.remove(neighbor) 
                        open_set[neighbor] = cost[neighbor.value]
                        

        curr.set_color(blue) 
        g.draw(sc)

        open_set.pop(curr, None)
        closed_set.append(curr)

    raise NotImplementedError('Not implemented')


def Greedy(g:Graph, sc:pygame.Surface):
    print('Implement A* algorithm')

    open_set = {}
    open_set[g.start] = 0
    closed_set:list[Node] = []
    father = [-1]*g.get_len()
    cost = [100_000]*g.get_len()
    cost[g.start.value] = 0

    #TODO: Implement A* algorithm using open_set, closed_set, and father
    while open_set:
        curr = None

        for node in open_set.keys():
            # nếu h(node) < h(curr) hoặc curr = Node thì:
            if curr == None or g.get_heuristic(node) < g.get_heuristic(curr):
                curr = node

        if curr == None:
            return
        
        curr.set_color(yellow)
        g.goal.set_color(purple)
        g.draw(sc)

        if g.is_goal(curr):
            g.start.set_color(orange)
            while True:
                father_node = father[curr.value]

                father_node.set_color(grey)
                g.start.set_color(orange)
                g.draw(sc)

                pygame.draw.line(sc, green, curr.get_xy(), father_node.get_xy())
                if(g.is_start(father_node)):
                    break

                curr = father_node
            return

        for neighbor in g.get_neighbors(curr):
            if neighbor not in open_set.keys() and neighbor not in closed_set:
                open_set[neighbor] = open_set[curr] + 1
                cost[neighbor.value] = cost[curr.value] + 1
                father[neighbor.value] = curr 
                neighbor.set_color(red)
            else:
                if cost[neighbor.value] > cost[curr.value] + 1:
                    cost[neighbor.value] = cost[curr.value] + 1
                    father[neighbor.value] = curr
                    if neighbor in closed_set:
                        closed_set.remove(neighbor) 
                        open_set[neighbor] = cost[neighbor.value]
                        

        curr.set_color(blue) 
        g.draw(sc)

        open_set.pop(curr, None)
        closed_set.append(curr)

    raise NotImplementedError('Not implemented')