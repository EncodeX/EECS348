
##################################################################
# Notes:                                                         #
# You can import packages when you need, such as structures.     #
# Feel free to write helper functions, but please don't use many #
# helper functions.                                              #
##################################################################


def dfs(testmap):
    # put your codes here:
    for i in xrange(len(testmap)):
        for j in xrange(len(testmap[i])):
            if testmap[i][j] is 2:
                dfs_helper(testmap, i, j)
    return testmap


def dfs_helper(testmap, a, b):
    stack = []
    r = {}
    testmap[a][b] = 0
    stack.insert(0, (a, b))
    while len(stack) > 0:
        x, y = stack.pop(0)
        if testmap[x][y] is 3:
            rx, ry = x, y
            while (rx, ry) in r:
                testmap[rx][ry] = 5
                rx, ry = r[(rx, ry)]
            testmap[a][b] = 5
            break
        testmap[x][y] = 4
        if check_node(testmap, x - 1, y):
            r[(x - 1, y)] = (x, y)
            stack.insert(0, (x - 1, y))
        if check_node(testmap, x, y - 1):
            r[(x, y - 1)] = (x, y)
            stack.insert(0, (x, y - 1))
        if check_node(testmap, x + 1, y):
            r[(x + 1, y)] = (x, y)
            stack.insert(0, (x + 1, y))
        if check_node(testmap, x, y + 1):
            r[(x, y + 1)] = (x, y)
            stack.insert(0, (x, y + 1))


def check_node(testmap, x, y):
    if x >= 0 and y >= 0 and x < len(testmap) and y < len(testmap[x]):
        if testmap[x][y] == 0 or testmap[x][y] == 3:
            return True
    return False


def bfs(testmap):
    # put your codes here:
    for i in xrange(len(testmap)):
        for j in xrange(len(testmap[i])):
            if testmap[i][j] is 2:
                bfs_helper(testmap, i, j)
    return testmap


def bfs_helper(testmap, a, b):
    stack = []
    r = {}
    testmap[a][b] = 0
    stack.append((a, b))
    while len(stack) > 0:
        x, y = stack.pop(0)
        if testmap[x][y] is 3:
            rx, ry = x, y
            while (rx, ry) in r:
                testmap[rx][ry] = 5
                rx, ry = r[(rx, ry)]
            testmap[a][b] = 5
            break
        testmap[x][y] = 4
        if check_node(testmap, x, y + 1):
            r[(x, y + 1)] = (x, y)
            stack.append((x, y + 1))
        if check_node(testmap, x + 1, y):
            r[(x + 1, y)] = (x, y)
            stack.append((x + 1, y))
        if check_node(testmap, x, y - 1):
            r[(x, y - 1)] = (x, y)
            stack.append((x, y - 1))
        if check_node(testmap, x - 1, y):
            r[(x - 1, y)] = (x, y)
            stack.append((x - 1, y))


def a_star_search(dis_map, time_map, start, end):
    scores = {}
    # put your codes here:
    open_list = {}
    close_list = {}
    stack = []
    open_list[start] = (0, dis_map[start][end])
    stack.append((start, (0, dis_map[start][end])))
    while len(stack) > 0:
        # get a node from stack
        node = stack.pop(0)
        # delete this node in open list
        del open_list[node[0]]
        # add this node in close list
        close_list[node[0]] = node[1]
        # if we find end
        if node[0] is end:
            break
        # if we don't have this node in scores
        if node[0] not in scores:
            scores[node[0]] = {}
        # iterate all available nodes
        for k, v in time_map[node[0]].iteritems():
            # if node is reachable
            if v is not None:
                # get g and n of current node
                # node[0] means current node place
                # node[1] = (gn, hn) e.g. line99's open_list[start]
                gn, hn = close_list[node[0]]
                # if this destination is in close list
                if k in close_list:
                    # get g and h from close list
                    gc, hc = close_list[k]
                    # add to scores
                    scores[node[0]][k] = v + gn + dis_map[k][end]
                    continue
                if k in open_list:
                    # get g and h from open list
                    go, ho = open_list[k]
                    # calculate score between these 2 node
                    scores[node[0]][k] = v + gn + dis_map[k][end]
                    # if we find a better route
                    if go + ho > v + dis_map[k][end] + gn:
                        # update them in open list
                        open_list[k] = (v + gn, dis_map[k][end])
                    continue
                # if not in close neither open, add it to open
                open_list[k] = (v + gn, dis_map[k][end])
                # update score array
                scores[node[0]][k] = v + gn + dis_map[k][end]
        stack = sorted(open_list.iteritems(),
                       key=lambda n: (n[1][0] + n[1][1], n[0]))
    return scores
