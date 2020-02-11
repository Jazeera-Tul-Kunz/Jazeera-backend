from utils_v2 import *
import requests,json,random,time,pickle,sys
from requests.exceptions import HTTPError

def generate_map():
    while len(visited) < 500:
        #get current room
        current = get_current_room()
        print('current room', current['room_id'])

        #record the room in the graph
        record_room(current)

        #choose a random '?' exit
        way = random_exit(current)[0]  #way is a tuple of ('n','?') or ('s',150)
        print('next way:', way)
        # print(way)

        # if len(way):
        #     way = way[0]

        next = move(way)
        record_room(next)

        cur_id,next_id = current['room_id'],next['room_id']
        print(cur_id,next_id)
        update_rooms(cur_id,way,next_id)

        # print('graph', graph)
        # print('visited', visited)
        print('traversal path: ', graph.traversal_path)
        print('rooms visited: ', len(visited))
        
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






