from utils import *
import requests,json,random,time,pickle,sys
from requests.exceptions import HTTPError
# from map_map import bfs


print(__name__)


def explore_neighbors():
    g = graph.vertices
    # while len(visited) < 1:
    print(len(visited),'rooms visited')

    r = get_current_room()
    room_id = r['room_id']
    visited.add(room_id)
    roomz = explore_exits(r)

    print('roomz from explore_exits()', roomz)

    for rz in roomz:
        visited.add(rz)
        print('added to visited',rz)

    g_roomz = {r_id:g[r_id] for r_id in roomz}

    print('graph of explored rooms for room id', room_id," : ", g_roomz)

    unexplored = {r_id:g[r_id] for r_id in g_roomz if '?' in g[r_id].values()}
    print('unexplored', unexplored)

    if len(unexplored):
        next_id,waze = random.choice([*unexplored.items()])
        way = [w for w in g[room_id] if g[room_id][w] == next_id]
        print(way)
        if len(way):
            way = way[0]
        next = move(way)
        next_roomz = explore_exits(next)
        for nr in next_roomz:
            visited.add(nr)
            print('added to visited', nr)
    else:
        print('all neighbors explored\n', len(g), g)
        return g
    return g

def map_generate():
    # while len(visited) < 500:
    n_graph = explore_neighbors()
    print('neighbor graph\t',n_graph)
    unexplored_neigh = {r_id: n_graph[r_id] for r_id in n_graph if '?' in n_graph[r_id].values()}
    print('unexplored neightbors \t', unexplored_neigh)
    trav_id,trav_waze = random.choice([*unexplored_neigh.items()])
    print('randomly chosen room to move to: ', trav_id)
    cur = get_current_room()
    # path = graph.bfs(cur['room_id'],trav_id)
    # bfs_neigh(n_graph,cur['room_id'],trav_id)
    path = bfs_matt(n_graph,cur['room_id'])
    print(path)
    
    return
        
    # 
    # g_unexplored = {r_id:g[r_id] for r_id in g if '?' in g[r_id].values()}
    # print('total graph unexplored', g_unexplored)
    # traverse_id,trav_waze = random.choice([*g_unexplored.items()])
    # graph.bfs(room_id,traverse_id)

with open('pyisland_map.json',"w") as pyisland:
            json.dump(graph.vertices,pyisland,indent=2)
if __name__ == '__main__':
    map_generate()


