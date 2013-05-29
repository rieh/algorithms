from copy import deepcopy

def kruskals(adj_list):
    '''Return a minimum spanning tree of adj_list using Kruskal's algo.'''

    adj_list = deepcopy(adj_list) # Since we need to modify adj_list
    expected_mst_edges = (len(adj_list.keys()) - 1) * 2
    mst = {k:[] for k in adj_list}
    for node in adj_list:
        adj_list[node].sort(key=lambda x: x[1]) # Sort by weight edge

    while get_edge_num(mst) < expected_mst_edges:
        min_edge = get_min_weight_edge(adj_list)
        first_node = min_edge[0]
        sec_node = min_edge[1]
        weight = min_edge[2]

        if not does_create_cycle(mst, min_edge): # Then include edge in MST
            edge_first_node = (sec_node, weight)
            edge_sec_node = (first_node, weight)
            mst[first_node].append(edge_first_node)
            mst[sec_node].append(edge_sec_node)
        
        del adj_list[first_node][0]
        del adj_list[sec_node][0]        
    return mst

def get_min_weight_edge(adj_list):
    '''Return the edge with minimum weight in adj_list.'''

    min_edge = None
    for key in adj_list:
        if adj_list[key]: # If this node has edges
            cur_edge = [key] + list(adj_list[key][0])
            if min_edge is None:
                min_edge = [key] + list(cur_edge)
        min_edge = min(min_edge, cur_edge, key = lambda x: x[2])    
    return min_edge

def does_create_cycle(adj_list, edge):
    '''Return whether edge creates a cycle in adj_list.'''

    return is_connected(adj_list, edge[0]) and is_connected(adj_list, edge[1])
    
def is_connected(adj_list, node):
    ''' Return whether there is an edge in adj_list connected to node.'''

    for key in adj_list:
        if node in adj_list[key]:
            return True
    return False
        
def get_edge_num(adj_list):
    ''' Return the total number of edges in the graph (adj_list).'''

    return sum((len(v) for k,v in adj_list.iteritems()))
    
def prims(adj_list):
    '''Return a minimum spanning tree of adj_list using Prim's algo.'''

    adj_list = deepcopy(adj_list) # Since we need to modify adj_list
    expected_mst_edges = (len(adj_list.keys()) - 1) * 2
    mst = {adj_list.iterkeys().next():[]} # Choose any one node
    for node in adj_list:
        adj_list[node].sort(key=lambda x: x[1]) # Sort by weight edge    
    
    while get_edge_num(mst) < expected_mst_edges:
        copy = {}
        
        for node in mst: # Get the minimum edge among nodes in mst
            copy[node] = adj_list[node]
        min_edge = get_min_weight_edge(copy)
        
        first_node = min_edge[0]
        sec_node = min_edge[1]
        weight = min_edge[2]        
        if not does_create_cycle(mst, min_edge): # Then include edge in MST
            edge_first_node = (sec_node, weight)
            edge_sec_node = (first_node, weight)
            mst[first_node] = mst.get(first_node, []) +[(edge_first_node)]
            mst[sec_node] = mst.get(sec_node, []) + [(edge_sec_node)]
        adj_list[first_node].remove((sec_node, weight))
        adj_list[sec_node].remove((first_node, weight))
    return mst            

def a_star(start, end, coords):
    '''Return the shortest route from start coord to end coord using A*
    algorithm'''

    coords = deepcopy(coords) # Since we have to modify the coordinates
    start = deepcopy(start)
    start["g_score"], start["h_score"], start["f_score"] = 0, 0, 0
    start["prev"] = []
    visited = []
    to_discover = [start]
    
    while to_discover:
        cur_node = get_min_fscore_coord(to_discover)
        to_discover.remove(cur_node)
        is_end = cur_node["is_end"]
        x, y = cur_node['x'], cur_node['y']
        
        if is_end: # Found finishing node
            return cur_node["prev"] + [(x, y)]
    
        to_discover += get_valid_neighbors(cur_node, end, coords, visited)
        visited += [(x, y)]
    return None

def get_min_fscore_coord(to_discover):
    '''Return the coord with minimum f score in list to_discover '''

    f_score = min(coord['f_score'] for coord in to_discover)
    
    for coord in to_discover:
        if coord['f_score'] == f_score:
            return coord
    return None


def get_valid_neighbors(cur_node, end, coords, visited):
    ''' Return list of valid neighbors for cur_node.'''

    x, y = cur_node['x'], cur_node['y']
    is_wall = cur_node["is_wall"]
    valid_neighbors = []
    
    to_check = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    
    for c in to_check:
        if is_in_board_and_not_visited(c, coords, visited):
            coord = get_coord(c, coords)
            coord['prev'] = cur_node['prev'] + [(x, y)]
            update_scores(coord, cur_node, end)
            valid_neighbors += [coord]
    return valid_neighbors
        
        
def is_in_board_and_not_visited(coord, coords, visited):
    '''Return if coord is inside the board, not a wall, and was not visited.'''

    viable_coords = [(c['x'], c['y']) for c in coords if not c["is_wall"]]
    return coord in viable_coords and coord not in visited
        
def get_coord(c, coordinates):
    '''Return the dictionary coord for tuple c inside coordinates.'''

    for coord in coordinates:
        if coord['x'] == c[0] and coord['y'] == c[1]:
            return coord
    return None

def calculate_hscore(cur_node, end_node):
    '''Return the h score of cur_node.'''

    x_dist = abs(cur_node['x'] - end_node['x'])
    y_dist = abs(cur_node['y'] - end_node['y'])
    return x_dist + y_dist

def update_scores(coord, visiting_coord, end_node):
    '''Update h score for coord.'''

    coord['g_score'] = visiting_coord['g_score'] + 1
    coord['h_score'] = calculate_hscore(coord, end_node)
    coord['f_score'] = coord['g_score'] + coord['h_score']    
    

    
# cooords: [coord. coord2, ...]
# coord: {x: val, y: val, is_start: val, is_end: val, is_wall: val
            # prev:[], h_score: val, f_score:}
    

if __name__ == "__main__":
    c1 = {'x': 0, 'y': 0, 'is_start': True, 'is_wall': False, 'is_end':False}
    c2 = {'x': 1, 'y': 0, 'is_start': False, 'is_wall': True, 'is_end':False}
    c3 = {'x': 2, 'y': 0, 'is_start': False, 'is_wall': False, 'is_end':False}
    c4 = {'x': 0, 'y': 1, 'is_start': False, 'is_wall': False, 'is_end':False}
    c5 = {'x': 1, 'y': 1, 'is_start': False, 'is_wall': True, 'is_end':False}
    c6 = {'x': 2, 'y': 1, 'is_start': False, 'is_wall': False, 'is_end':False}
    c7 = {'x': 0, 'y': 2, 'is_start': False, 'is_wall': False, 'is_end':False}
    c8 = {'x': 1, 'y': 2, 'is_start': False, 'is_wall': False, 'is_end':False}
    c9 = {'x': 2, 'y': 2, 'is_start': False, 'is_wall': False, 'is_end':True}
    coords = [c1, c2, c3,c4, c5, c6, c7, c8, c9]
    start = c1
    end = c9
    print(a_star(start, end, coords))