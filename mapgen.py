from utils import *
import requests,json,random,time,pickle,sys
from requests.exceptions import HTTPError

def generate_map():
    g = graph.vertices
    while len(visited) < 500:
        #get current room
        current = get_current_room()
        curr_id = current['room_id']
        print('current room', curr_id )

        #record the room in the graph. if already recorded returns the room entry in the graph.
        record_room(current)  #returns the room_exits of the current room.

        #choose a random '?' exit
        way,way_id = random_exit(current) #way is a tuple of ('n','?') or ('s',150)
        print('randomly selected: ', way, way_id)

        # if way_id != '?':
        #     unexplored = {r_id:g[r_id] for r_id in g if '?' in g[r_id].values()}
        #     new_id,new_exits = random.choice([*unexplored.items()])
        #     print(new_id,new_exits, 'newid, newexits')
        #     bfs_path = graph.bfs_ids(curr_id,new_id)
        #     print('bfs_path', bfs_path)
        #     # bfs_path = bfs_path[1:] #skip the first room because already in the first room. 
        #     for i,r_id in enumerate(bfs_path):
        #         try:
        #             next_rid = bfs_path[i+1]
        #         except:
        #             next_rid = None
        #             break
        #         next_way = [way for way in g[r_id] if g[r_id][way] == next_rid]
        #         print('next_way in bfs path', next_way)
        #         if len(next_way):
        #             next_way = next_way[0]
        #         next = move(next_way)
        #         record_room(next)
        #         cur_id,next_id = current['room_id'],next['room_id']
        #         print(cur_id,next_id)
        #         update_rooms(cur_id,way,next_id)
        #     print('current room after BFS', get_current_room())
        # else:
        next = move(way)
        record_room(next)

        cur_id,next_id = current['room_id'],next['room_id']
        print(cur_id,next_id)

        update_rooms(cur_id,way,next_id)

        print('\nrooms visited: ', len(visited), '\n')
        
        with open('pyisland.json','w') as pyisland_map:
            print('dumping graph json to', 'pyisland_map')
            json.dump(graph.vertices,pyisland_map,indent=2)
    return graph.vertices

if __name__ == '__main__':
    start_time = time.time()
    pyisland = generate_map()
    print('pyisland', pyisland)
    end_time = time.time()
    print('total execution time: ', end_time - start_time)






