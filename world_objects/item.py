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
        self.durability = 15
    def use(self, player):
        self.durability -= 1
        if self.durability == 0:
            player.health += 4 if player.health < 18 else 0
            if self.count > 1:
                self.count -= 1
                self.durability = 15
            else :self.count = 0
    def copy(self):
        return CherrieItem(self.count)
        
class StoneHammer(InventoryItem):
    def __init__(self, durability=25):
        super().__init__(STONE_HAMMER, 1)
        self.durability = durability
        self.durability_default = 25
       

    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return 
    def copy(self):
        return StoneHammer(durability=self.durability)

class Picaxe(InventoryItem):
    
    def __init__(self, tier=WOODEN_PICAXE, durability=100):
        super().__init__(tier, 1)
        if tier == WOODEN_PICAXE:

            self.durability = durability
            self.durability_default = 60
        elif tier == STONE_PICAXE:
            self.durability = durability
            self.durability_default = 200
        else:
            self.durability = durability
            self.durability_default = 10
        self.tier = tier
    def get_durability(self, tier):
        if tier == WOODEN_PICAXE:

      
            return  60
        elif tier == STONE_PICAXE:
           
            return 200
        else:
            return  10  
    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
    def copy(self):
        return Picaxe(tier=self.tier, durability=self.durability)
    
class Axe(InventoryItem):
    
    def __init__(self, tier=WOODEN_AXE, durability=100):
        super().__init__(tier, 1)
        if tier == WOODEN_AXE:

            self.durability = durability
            self.durability_default = 70
        elif tier == STONE_AXE:
            self.durability = durability
            self.durability_default = 230
        else:
            self.durability = durability
            self.durability_default = 10
        self.tier = tier
    def get_durability(self, tier):
        if tier == WOODEN_AXE:

      
            return  70
        elif tier == STONE_AXE:
           
            return 230
        else:
            return  10  
    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
    def copy(self):
        return Axe(tier=self.tier, durability=self.durability)

class BreathingMask(InventoryItem):
    
    def __init__(self, durability=80):
        super().__init__(BREATHING_MASK, 1)
        self.durability = durability
        self.durability_default = 80

    def fuse(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
    def copy(self):
        return BreathingMask(durability=self.durability)
class Sword(InventoryItem):
    
    def __init__(self, tier=WOODEN_SWORD, durability=100):
        super().__init__(tier, 1)
        if tier == WOODEN_SWORD:

            self.durability = durability
            self.durability_default = 160
        elif tier == STONE_SWORD:
            self.durability = durability
            self.durability_default = 300
        else:
            self.durability = durability
            self.durability_default = 10
        self.tier = tier
    def get_durability(self, tier):
        if tier == WOODEN_SWORD:

      
            return  160
        elif tier == STONE_SWORD:
           
            return 300
        else:
            return  10  
    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
    def copy(self):
        return Sword(tier=self.tier, durability=self.durability)
class Shovel(InventoryItem):
    
    def __init__(self, tier=WOODEN_SHOVEL, durability=100):
        super().__init__(tier, 1)
        if tier == WOODEN_SHOVEL:

            self.durability = durability
            self.durability_default = 60
        elif tier == STONE_SHOVEL:
            self.durability = durability
            self.durability_default = 200
        else:
            self.durability = durability
            self.durability_default = 10
        self.tier = tier
    def get_durability(self, tier):
        if tier == WOODEN_SHOVEL:

      
            return  60
        elif tier == STONE_SHOVEL:
           
            return 200
        else:
            return  10  
    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
    def copy(self):
        return Shovel(tier=self.tier, durability=self.durability)
class Helmet(InventoryItem):
    def __init__(self, tier, durability=None):
        super().__init__(tier, 1)
        self.durability = durability if durability else self.get_dur(tier)
        self.durability_default = self.get_dur(tier)    
        self.tier = tier

    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
    def get_dur(self, tier):
        if tier == WOODEN_HELMET:
            return 100
        else:
            return 3
    def get_protection(self):
        if self.tier == WOODEN_HELMET:
            return 0.9
        else:
            return 1
    def copy(self):
        return Helmet(self.tier, durability=self.durability)
class Chesplate(InventoryItem):
    def __init__(self, tier, durability=None):
        super().__init__(tier, 1)
        self.durability = durability if durability else self.get_dur(tier)
        self.durability_default = self.get_dur(tier)    
        self.tier = tier

    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
    def get_dur(self, tier):
        if tier == WOODEN_CHESPLATE:
            return 100
        else:
            return 3
    def get_protection(self):
        if self.tier == WOODEN_CHESPLATE:
            return 0.9
        else:
            return 1
    def copy(self):
        return Chesplate(self.tier, durability=self.durability)
class Leggings(InventoryItem):
    def __init__(self, tier, durability=None):
        super().__init__(tier, 1)
        self.durability = durability if durability else self.get_dur(tier)
        self.durability_default = self.get_dur(tier)    
        self.tier = tier

    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
    def get_dur(self, tier):
        if tier == WOODEN_LEGGINGS:
            return 100
        else:
            return 3
    def get_protection(self):
        if self.tier == WOODEN_LEGGINGS:
            return 0.98
        else:
            return 1
    def copy(self):
        return Leggings(self.tier, durability=self.durability)
class Boots(InventoryItem):
    def __init__(self, tier, durability=None):
        super().__init__(tier, 1)
        self.durability = durability if durability else self.get_dur(tier)
        self.durability_default = self.get_dur(tier)    
        self.tier = tier

    def damage(self):
        self.durability -= 1
        if self.durability <= 0:
            return True
        return False
    def get_dur(self, tier):
        if tier == WOODEN_BOOTS:
            return 100
        else:
            return 3
    def get_protection(self):
        if self.tier == WOODEN_BOOTS:
            return 0.9999
        else:
            return 1
    def copy(self):
        return Boots(self.tier, durability=self.durability)


def get_itemobj(id, count):
    if id == STONE_HAMMER:
        return StoneHammer()
    elif id == CHERRIES:
        return CherrieItem(count)
    else:
        return InventoryItem(id, count)