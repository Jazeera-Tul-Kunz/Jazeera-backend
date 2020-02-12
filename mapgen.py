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



#handling rooms without unexplored '?' rooms:  using BFS.  need to reimplement.
        # if way_id == '?':
        #     # move to the '?'
        #     # record the next room
        #     # update the next and curr rooms
        #     #dump to json file
        #     next = move(way)
        #     record_room(next)

        #     cur_id,next_id = current['room_id'],next['room_id']
        #     print(cur_id,next_id)

        #     update_rooms(cur_id,way,next_id)

        #     print('\nrooms visited: ', len(visited), '\n')
            
        #     with open('pyisland.json','w') as pyisland_map:
        #         print('dumping graph json to', 'pyisland_map')
        #         json.dump(graph.vertices,pyisland_map,indent=2)

        # elif way_id != '?':
        #     print('way id has already been explored!!!', way_id)
        #     g_unexplored = {r_id:g[r_id] for r_id in g if '?' in g[r_id].values()}
        #     print('unexplored exits on the graph', g_unexplored)
        #     end_id,waze = random.choice([*g_unexplored.items()]) #ending room id , exits tuple
        #     print('randomly choosing a room with unexplored exits: ', end_id)
        #     bfs_path = bfs_island(curr_id,end_id)
        #     print('bfs_path', bfs_path)

        #     if not bfs_path:
        #         print('no bfs path returned graph: ', g)
            
        #     curr_id,*bfs_path = bfs_path

        #     for r_id in bfs_path:
        #         way = [way for way in g[curr_id] if g[curr_id][way] == r_id]
        #         print('way in bfs_path', way)
        #         if len(way):
        #             way = way[0]
        #         next = wise_move(way,r_id)
        #         # next = move(way)
        #         record_room(next)
        #         update_rooms(curr_id,way,next['room_id'])
        #         curr_id = r_id
            
        #     print('current room after BFS', get_current_room()['room_id'])



