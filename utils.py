import json,os,sys,time,requests,random
from data_structures import Graph

adv_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv'
graph = Graph()
visited = set()

def get_auth():
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv('API_KEY')
    return {'Authorization': f'Token {token}'}

auth = get_auth()

def get_current_room():
    res = requests.get(f"{adv_url}/init", headers=auth)
    if res:
        print('successful response',res.status_code,res.reason)
        current_room = res.json()
        # print(current_room)
    else:
        print('error', res.status_code,res.reason,res.text)
        sys.exit(1)
    time.sleep(current_room['cooldown'])
    return current_room

def record_room(room):
    room_id,exits = room['room_id'],room['exits']
    if room_id in graph.vertices:
        print('room ', room_id, 'already exists in map_graph')
        return graph.vertices[room_id]
    print('recording room', room_id)
    graph.data.add(json.dumps(room))
    graph.traversal_path.append(room_id)
    visited.add(room_id)
    room_entry = {}
    for way in exits:
        room_entry[way] = '?'
    graph.vertices[room_id] = room_entry
    return graph.vertices[room_id]

def flip_way(way):
    directions = {'n': 's', 's':'n', 'e':'w', 'w':'e'}
    return directions[way]

def update_rooms(prev_id,way,next_id):
    print('in update rooms')
    graph.vertices[prev_id][way] = next_id
    flip = flip_way(way)
    graph.vertices[next_id][flip] = prev_id

def random_exit(room):
    g = graph.vertices
    room_id = room['room_id']
    
    if '?' not in g[room_id].values():
        known_exit = random.choice([*g[room_id].items()])
        print('no unknown exits to explore here, randomly choosing explored exit: ', known_exit)
        return known_exit
    
    print('all exits for ', room_id, ':', g[room_id])
    unexplored = {way:g[room_id][way] for way in g[room_id] if g[room_id][way] == '?'}
    print("room id", room_id,' unexplored exits', unexplored)
    rand_exit = random.choice([*unexplored.items()])
    return rand_exit

def move(way):
    if not len(way):
        return get_current_room()
    print('moving ', way)
    res = requests.post(f"{adv_url}/move",headers=auth,json={'direction':way})
    if res:
        print('successful response', res.status_code)
        new_room = res.json()
    else:
        print('error', res.status_code)
        sys.exit(1)
    print('moved to room: ', new_room['room_id'])
    print('cooling down. please wait...',new_room['cooldown'])
    time.sleep(new_room['cooldown'])
    return new_room