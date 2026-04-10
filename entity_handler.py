from settings import *
from typing import Literal
from world_objects.entity import Chicken, player_entity
from terrian_gen import get_height
from utils import get_distance

_gch_type = Literal['a', 'e', 'b']
class EntityHandler:
    def __init__(self, app):
        self.app = app
        self.entities = []
        self.block_entities = []
        self.entity_id = 0
        
        self.add_e(self.app.player.as_entity())

   
    def entity_at(self, position):
        position = glm.ivec3(position)
        entities_at_pos = list(map(lambda entity: entity if glm.ivec3(entity.x, entity.y, entity.z) == position else None, self.entities))
        if entities_at_pos.count(None) != len(entities_at_pos):
            entities_at_pos = list(filter(lambda e: e, entities_at_pos))
            return True, entities_at_pos[0]
        return False, None

    def delte_entity(self, entity_index):
        try:
            del self.entities[entity_index]
        except:
            pass
    def update(self):
        dc = 0
        for index, entity in enumerate(self.entities): 
            if ((hasattr(entity, "_is_garbage") and entity._is_garbage == True) or entity.y < -25) and dc < 8:
                if not isinstance(entity, player_entity):
                    self.delte_entity(index)
                else:
                    entity.kill()
                    self.delte_entity(index)
                    
                dc += 1
            if entity.y < -2:
                entity.damage(4, is_void_damage=True)

            entity.update()
            

        if random.random() < 0.5:
            x,z = random.randint(0, WORLD_W * CHUNK_SIZE), random.randint(0, WORLD_D * CHUNK_SIZE)
            y  = get_height(x, z)
            if get_distance((x, y, z), self.app.player.position) < 90 :
                self.add_e(Chicken(self.app, x, y + 1, z, random.choice(["Chicky", "Chicken", "Chickoletta"])))
    def render(self):
        for i in self.entities: i.render()
    def add_be(self, e):
        self.block_entities.append(e)
    def add_e(self, e):

        e.id = self.entity_id
        self.entities.append(e)
        self.entity_id += 1
  