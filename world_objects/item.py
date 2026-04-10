from settings import * 

class InventoryItem:
    def __init__(self, item_id, count):
        self.item_id = item_id if item_id else 0
        self.count = count


        
    def __repr__(self):
        return f"Item({self.item_id},{self.count})"
    def copy(self):
        return InventoryItem(self.item_id, self.count)
    
class CherrieItem(InventoryItem):
    def __init__(self, count):
        super().__init__(CHERRIES, count)
        self.durability = 30
    def use(self, player):
        self.durability -= 1
        if self.durability == 0:
            player.health += 2 if player.health < (21 - 2 * self.count) else 0
    def copy(self):
        return CherrieItem(self.count)
        
class StoneHammer(InventoryItem):
    def __init__(self):
        super().__init__(STONE_HAMMER, 1)
        self.durability = 100
        self.durability_default = 100
       

    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return 
    def copy(self):
        return StoneHammer()



def get_itemobj(id, count):
    if id == STONE_HAMMER:
        return StoneHammer()
    elif id == CHERRIES:
        return CherrieItem(count)
    else:
        return InventoryItem(id, count)