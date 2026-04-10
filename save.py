from settings import *
import os
from world_objects.item import InventoryItem
import json

def save_world(world_name, world):
    if not os.path.exists(f"worlds\\{world_name}"):
        os.mkdir(f"worlds\\{world_name}")
    for chunk in world.chunks:
        if chunk:
            save_chunk(world_name, chunk)

    save_player(world_name, world.app.player)

    if os.path.exists(f"worlds\\{world_name}\\seed.www"):
        with open(f"worlds\\{world_name}\\seed.www", "w") as f:
            f.write(str(SEED))
    else:
        with open(f"worlds\\{world_name}\\seed.www", "x") as f:
            f.write(str(SEED))

    
def save_chunk(world_name,  chunk):
    x,y,z = chunk.position
    fname = f"cx{x}y{y}z{z}"
    if os.path.exists(f"worlds\\{world_name}\\{fname}.www"):
        with open(f"worlds\\{world_name}\\{fname}.www", "w") as f:
            f.write("/".join(list(map(lambda x: str(x), chunk.voxels))))
    else:
        with open(f"worlds\\{world_name}\\{fname}.www", "x") as f:
            f.write("/".join(list(map(lambda x: str(x), chunk.voxels))))

def chunk_is_generated(world_name, position):
    x,y,z = position
    if os.path.exists(f"worlds\\{world_name}\\cx{x}y{y}z{z}.www"):
        with open(f"worlds\\{world_name}\\cx{x}y{y}z{z}.www") as f:
            data = f.read()
        if "/" in data and data.replace("/", "").isdigit():
            return True
        
    return False
def world_exists(world_name):
    return os.path.exists(f"worlds\\{world_name}")

def save_player(world_name, player):
   

    player_data = repr({
        "x":player.position.x,
        "y":player.position.y,
        "z":player.position.z,
        "velocity":player.velocity,
        "yaw":player.yaw,
        "pitch":player.pitch,
        "health":player.health,
        "bubbeles":player.bubbeles,
        "gamemode":GAMEMODE,
        "inventory":player.inventory.slots,
    })
    if os.path.exists(f"worlds\\{world_name}\\player.www"):
        with open(f"worlds\\{world_name}\\player.www", "w") as f:
            f.write(player_data)
    else:
        with open(f"worlds\\{world_name}\\player.www", "x") as f:
            f.write(player_data)

def load_chunk(world_name, position):
    x,y,z = position
    with open(f"worlds\\{world_name}\\cx{x}y{y}z{z}.www", 'r') as f:
        data = list(map(lambda x: int(x), f.read().split("/")))

    if len(data) == CHUNK_VOL:
        return np.array(data, dtype="uint8")
    

    else:
        return np.append(np.array(data, dtype='uint8'), np.zeros(CHUNK_VOL - len(data), dtype='uint8'))
    

def load_player(world_name, player):
    with open(f"worlds\\{world_name}\\player.www", 'r') as f:
        data = eval(f.read(), {"Item":InventoryItem})
        player.x = data["x"]
        player.y = data["y"]
        player.z = data["z"]
        player.yaw = data["yaw"]
        player.pitch = data["pitch"]
        player.health = data["health"]
        player.bubbeles = data["bubbeles"]
        player.inventory.slots = data["inventory"]
        
        import settings as st
        st.GAMEMODE = data["gamemode"]
        del st
        



    


def get_seed(world_name):
    with open(f"worlds\\{world_name}\\seed.www", 'r') as f:
        return int(f.read())