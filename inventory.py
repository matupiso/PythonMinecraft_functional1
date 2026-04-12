from settings import *
import pygame as pg
from world_objects.item import InventoryItem as Item 
from world_objects.item import *
from world_objects.item import get_itemobj
from utils import *

from textures import get_number_surface, item_highlight, transparent





def load_icon(name):
    icon = pg.image.load(f"C:\\Users\\stano\\vs_code\\Matusko\\Minecraft\\assets\\items\\{name}.png")
    icon = pg.transform.scale(icon, (50, 53))
    return icon
class Inventory:
    def __init__(self, app):
        self.app = app
        self.slots = [0 for i in range(40)]

        self.aaa= 0

        self.last_lbutton_state = False
        self.last_rbutton_state = False

        self.slot_idf =  [f"a{i + 1}" for i in range(8)] + [f"b{i + 1}" for i in range(8)] + [f"c{i + 1}" for i in range(8)] + [f"d{i + 1}" for i in range(8)] + [f"e{i + 1}" for i in range(4)] + [f"f{i + 1}" for i in range(4)]
        self.inventory_image = pg.image.load("assets\\inventory.png")
        self.inventory_image = pg.transform.scale(self.inventory_image, (630, 603))


        self.sx = (int(WIN_RES.x) - self.inventory_image.get_width()) // 2
        self.sy = (int(WIN_RES.y) - self.inventory_image.get_height()) // 2
        


        self.item_name_font = pg.font.Font("freesansbold.ttf", 30)
        self.item_names = {SAND:"sand", GRASS:"grass", DIRT:"dirt", STONE:"stone", 
                           SNOW:"snow", LEAVES:"leaves", WOOD:"wood", 
                           BEDROCK:"bedrock", COMMAND_BLOCK:"command_block", 
                           COAL_ORE:"coal_ore", TORCH:"torch",YELLOW_WOOL:"yellow_wool", 
                           BLUE_WOOL:"blue_wool", COAL:"coal", STICK:"stick",
                           STONE_HAMMER:"stone_hammer", CHERRIES:"cherries", PLANKS:"planks",
                           CRAFTING_TABLE:"crafting_table", DIAMOND_ORE:"diamond_ore",
                           STONE_PICAXE:"stone_picaxe", WOODEN_PICAXE:"wooden_picaxe",
                           WOODEN_LEGGINGS:"wooden_leggings", WOODEN_BOOTS:"wooden_boots", WOODEN_CHESPLATE:"wooden_chesplate",
                           WOODEN_HELMET:"wooden_helmet", STONE_SHOVEL:"stone_shovel", STONE_AXE:"stone_axe",
                           STONE_SWORD:"stone_sword", WOODEN_AXE:"wooden_axe", WOODEN_SWORD:"wooden_sword",WOODEN_SHOVEL:"wooden_shovel",
                           BREATHING_MASK:"breathing_mask"}



        self.items = {idx:load_icon(name) for idx,name in self.item_names.items()}


        self.enabled = False

        self.grabbed_item = None
        self.grabbed_item_idf = None
    def get_crafted_item(self):
        craft_group = list(map(lambda x: 0 if x == 0 else x.item_id, self.get_craft_group()))
        if craft_group == [PLANKS, 0, 0, PLANKS]:
            return (STICK, 4), Item(STICK, 4)
        elif craft_group == [COAL, 0, 0, STICK]:
            return (TORCH, 4), Item(TORCH, 4)
        elif craft_group.count(0) == 3 and craft_group.count(WOOD) == 1:
            return (PLANKS, 4), Item(PLANKS, 4)
        elif craft_group.count(PLANKS) == 4:
            return (CRAFTING_TABLE, 1), Item(CRAFTING_TABLE, 1)
        
        else:
            return None

        
    def idf_to_pos(self, idf):
        if idf == "e":
            return 552 + self.sx, 118 + self.sy
        
        if len(idf) != 2:
            return None
        
        row, column = idf[0], idf[1]
        x,y = 0,0


        if row in ["a", "b", "c", "d"]:
            if row == "a": y = 520
            elif row == "b": y = 452
            elif row == "c": y = 390
            elif row == "d": y = 330

            if column == "1": x = 23
            elif column == "2": x = 83
            elif column == "3": x = 142
            elif column == "4": x = 200
            elif column == "5": x = 258
            elif column == "6": x = 318
            elif column == "7": x = 376
            elif column == "8": x = 435
            else:
                return None
        elif row == "e":
            if column == "1": x,y = 377, 82
            elif column == "2":x,y = 434, 82
            elif column == "3":x,y = 434, 142
            elif column == "4":x,y = 377,142
            else:
                return None

        elif row == "f":
            x = 23
            if column == "1": y = 23
            elif column == "2": y = 82
            elif column == "3": y = 140
            elif column == "4": y = 199
            else:
                return None
            
            


        return (x + self.sx, y + self.sy)

    def pos_to_idf(self, mx, my):
      
        mx -= self.sx
        my -= self.sy

        if mx > 629 or mx <=0 or my > 600 or my <= 0:
            return None
        
        row = ""
        column = ""

        if mx > 23 and mx < 487 and my > 520 and my < 574:
            row = "a"
        elif mx > 23 and mx < 487 and my > 452 and my < 500:
            row = "b"
        elif mx > 23 and mx < 487 and my > 390 and my < 443:
            row = "c"
        elif mx > 23 and mx < 487 and my > 330 and my < 383:
            row = "d"
        elif mx > 376 and mx < 487 and my > 81 and my < 194:
            row = "e"
        elif mx > 552 and mx < 604 and my > 118 and my < 168:
            return "e"
        elif mx > 24 and mx < 78 and my > 24 and my < 252:
            row = "f"

        else:
            return None
        


        if row in ["a", "b", "c", "d"]:
            if mx > 23 and mx < 78:
                column = 1
            elif mx > 83 and mx < 137:
                column = 2
            elif mx > 142 and mx < 196:
                column = 3
            elif mx > 200 and mx < 253:
                column = 4
            elif mx > 258 and mx < 312:
                column = 5
            elif mx > 318 and mx < 371:
                column = 6
            elif mx >  376 and mx < 429:
                column = 7
            elif mx > 435 and mx < 489:
                column = 8
            else:
                return None
        elif row == "e":
            if mx > 377 and mx < 431 and my > 82 and my < 135:
                column = 1
            elif mx > 434 and mx < 487 and my > 82 and my < 135:
                column = 2
            elif mx > 434 and mx < 487 and my > 142 and my < 192:
                column = 3
            elif mx > 377 and mx < 431 and my > 140 and my < 194:
                column = 4
        elif row == "f":
            if my >  23 and my < 79:
                column = 1
            elif my > 82 and my < 136:
                column = 2
            elif my >  140 and my < 196:
                column = 3
            elif my > 199 and my < 253:
                column = 4
        
        
        
        
        return row + str(column)
        
    def update(self):
        for index, value in enumerate(self.slots):
            if isinstance(value, Item) and (value.count == 0 or (hasattr(value, "durability") and value.durability <= 0)):
                self.slots[index] = 0
        if self.enabled:

            pl,_,pr = pg.mouse.get_pressed()
            l,r = not self.last_lbutton_state and pl, not self.last_rbutton_state and pr, 
            self.last_lbutton_state = pl
            self.last_rbutton_state = pr
            
                
            x,y = pg.mouse.get_pos()
            idf = self.pos_to_idf(x, y)
            if not idf:
                return
            if idf and len(idf) == 2:
                item = self.slots[self._idf_to_index(idf)]
                if not isinstance(item, Item):
                    item = None
            else:
                item = None

            
            if idf == "e" and l and not self.grabbed_item and self.get_crafted_item():
                self.grabbed_item_idf = "e"
                _, self.grabbed_item = self.get_crafted_item()
                craft_group = self.get_craft_group()
                for index, value in enumerate(craft_group):
                    if value != 0:
                        craft_group[index].count -= 1
                        if value.count == 0:
                            craft_group[index] = 0
            if len(idf) == 2:
                if l and not self.grabbed_item and item:
                    self.grabbed_item = item.copy()
                    self.grabbed_item_idf = str(idf)
                    self.slots[self._idf_to_index(idf)] = 0
                elif r and self.grabbed_item:
                    if not item:
                        self.slots[self._idf_to_index(idf)] = get_itemobj(self.grabbed_item.item_id, 1)
                        self.grabbed_item.count -= 1
                        if self.grabbed_item.count <= 0:
                            self.grabbed_item = None
                            self.grabbed_item_idf = None
                    elif item and self.grabbed_item.item_id == item.item_id and item.count + 1 <= get_stackable_count(item.count):
                        self.slots[self._idf_to_index(idf)].count += 1
                        self.grabbed_item.count -= 1
                        if self.grabbed_item.count <= 0:
                            self.grabbed_item = None
                            self.grabbed_item_idf = None
                elif l and self.grabbed_item:
                    if not item:
                        self.slots[self._idf_to_index(idf)] = self.grabbed_item.copy()
                        self.grabbed_item = None
                        self.grabbed_item_idf = None
                    
                    elif isinstance(item, Item) and self.grabbed_item.item_id == item.item_id and item.count + self.grabbed_item.count <= get_stackable_count(item.item_id):
                        self.slots[self._idf_to_index(idf)].count += self.grabbed_item.count
                        self.grabbed_item = None
                        self.grabbed_item_idf = None
                    
     
        #print(self.pos_t_idf(*pg.mouse.get_pos()))
        # if pg.key.get_pressed()[pg.K_c]:

        #     with open("this.txt", "a") as f:
        #         x,y = pg.mouse.get_pos()
        #         f.write(f"{self.aaa} {x - self.sx, y - self.sy}\n")
        #     self.aaa += 1
    def render_hotbar(self):
        for i in range(1, 9):
            idf = f"a{i}"
            item_id = self[idf].item_id if isinstance(self[idf], Item) else 0
            ix,iy = (WIN_RES.x - 423) // 2 + (i-1) * 60, int(WIN_RES.y * 0.80034) + 41
            if i-1 == self.app.player.hand_index:
                    self.app.scene.render_on_screen(item_highlight, ix, iy) 
                   
        
         
            try:

               
                self.app.scene.render_on_screen(self.items[item_id], ix, iy) 
                if hasattr(self[idf], 'damage'):
                    rel_dur = (self[idf].durability / self[idf].durability_default) * 46
                    screen = pg.transform(transparent, (50, 53))
                    pg.draw.rect(screen, "black", pg.Rect(2, 48, 46, 4))
                    pg.draw.rect(screen, "green" if rel_dur > 35 else "yellow" if rel_dur > 20 else (250, 0, 0), pg.Rect( 2,  48, rel_dur, 4))
                    self.app.scene.render_on_screen(screen, ix, iy) 

                       
                
        
            except:
                pass        
        for i in range(1, 9):
            idf = f"a{i}"
            item_id = self[idf].item_id if isinstance(self[idf], Item) else 0
            item_count = self[idf].count if isinstance(self[idf], Item) else 0
            try:
                ix,iy = (WIN_RES.x - 423) // 2 + (i-1) * 60, int(WIN_RES.y * 0.80034) + 41
                ns = get_number_surface(item_count)
                if ns:
                    self.app.scene.render_on_screen(ns, ix + 30, iy + 30)


        
            except:
                pass



    def render(self):
        if not self.enabled:
            return
        screen = pg.surface.Surface(tuple(WIN_RES))
        screen.fill((0, 0, 0))

        screen.blit(self.inventory_image, (self.sx,self.sy))

        slot_idf = self.slot_idf
        for idf in slot_idf:
        
            item_id = self[idf].item_id if isinstance(self[idf], Item) else 0
            

            if item_id == 0:
                continue

            if self.idf_to_pos(idf):
                x,y = self.idf_to_pos(idf)
            else:
                x,y = 0, 0
          
            try:
                screen.blit(self.items[item_id], (x + 2, y + 2))
                if hasattr(self[idf], 'damage'):
                    rel_dur = (self[idf].durability / self[idf].durability_default) * 46
                    pg.draw.rect(screen, "black", pg.Rect(x + 2, y + 50, 46, 4))
                    pg.draw.rect(screen, "green" if rel_dur > 35 else "yellow" if rel_dur > 20 else (250, 0, 0), pg.Rect(x + 2, y + 50, rel_dur, 4))
                    

                
            except:
                pass
        for idf in slot_idf:
        
            item_count = self[idf].count if isinstance(self[idf], Item) else 0
            item_id = self[idf].item_id if isinstance(self[idf], Item) else 0
            
            

            if item_id == 0:
                continue

            if self.idf_to_pos(idf):
                x,y = self.idf_to_pos(idf)
            else:
                x,y = 0, 0
          
            try:
                ns = get_number_surface(item_count)
                if ns:
                    screen.blit(ns, (x + 30, y + 30))


            except:
                pass


        if self.grabbed_item:
            mx, my = pg.mouse.get_pos()
           
            try:
                screen.blit(self.items[self.grabbed_item.item_id], (mx - 5, my - 5))
                if hasattr(self.grabbed_item, 'damage'):
                    rel_dur = (self.grabbed_item.durability / self.grabbed_item.durability_default) * 46
                    pg.draw.rect(screen, "black", pg.Rect(mx + 2, my + 50, 46, 4))
                    pg.draw.rect(screen, "green" if rel_dur > 35 else "yellow" if rel_dur > 20 else (250, 0, 0), pg.Rect(mx + 2,my + 50, rel_dur, 4))
                    

            except:
                pass
            try:
                ns = get_number_surface(self.grabbed_item.count)
                if ns:
                    screen.blit(ns, (mx + 25, my + 25))

            except:
                pass
        if self.get_crafted_item():
            i, item_obj = self.get_crafted_item()
            item, count = i
            cx, cy = self.idf_to_pos("e")
            try:
                screen.blit(self.items[item], (cx, cy))
                if hasattr(item_obj, 'damage'):
                    rel_dur = (item_obj.durability / item_obj.durability_default) * 46
                    pg.draw.rect(screen, "black", pg.Rect(cx + 2, cy + 50, 46, 4))
                    pg.draw.rect(screen, "green" if rel_dur > 35 else "yellow" if rel_dur > 20 else (250, 0, 0), pg.Rect(cx + 2,cy + 50, rel_dur, 4))
                    

            except:
                pass
            try:
                ns = get_number_surface(count)
                if ns:
                    screen.blit(ns, (cx + 30, cy + 30))

            except:
                pass
        if self.pos_to_idf(*pg.mouse.get_pos()) and self.pos_to_idf(*pg.mouse.get_pos()) != None and len(self.pos_to_idf(*pg.mouse.get_pos())) == 2  and self[self.pos_to_idf(*pg.mouse.get_pos())]:
            img = self.item_name_font.render(self.item_names[self[self.pos_to_idf(*pg.mouse.get_pos())].item_id], True, "light blue", "dark blue")
            screen.blit(img, (pg.mouse.get_pos()[0] + 45,pg.mouse.get_pos()[1] + 60))

        self.app.scene.render_on_screen(screen, 0, 0)



        




    def __setitem__(self, key, value):
        index = self._idf_to_index(key)
        if value:
            self.slots[index] = value
    def __getitem__(self, key):
        index = self._idf_to_index(key)
        return self.slots[index]
    def __delitem__(self, key):
        index = self._idf_to_index(key)
        self.slots[index] = 0   
    def _get_group(self, group_id):
        group_start, group_end = tuple(group_id.split("-"))
        index1 = self._idf_to_index(group_start)
        index2 = self._idf_to_index(group_end) + 1

        return self.slots[index1:index2]
    
    def get_hand_group(self):
        return self._get_group("a1-a8")
    
    def get_craft_group(self):
        return self._get_group("e1-e4")
    
    def get_armor_group(self):
        return self._get_group("f1-f4")
    def get_inventory_group(self):
        return self._get_group("b1-d8")
    def get_normal_use_group(self):
        return self._get_group("a1-d8")
        
    @staticmethod
    def _idf_to_index(idf):
        if type(idf) != str:
            raise TypeError(f"argument 1(idf) must be a string got '{type(idf).__name__}'")
        if len(idf) != 2:
            raise TypeError(f"argument 1(idf) needs to have lentgh '2' got '{len(idf)}'")
        row_id, colum = tuple(idf)


        if not colum.isdigit() or not row_id.isalpha() or colum == "0":
            raise TypeError(f"argument 1(idf) has invalid format ('{idf}') should be like a1")


        rows = {"a":0, "b":8, "c":16, "d":24, "e":32, "f":36} # a = hand, b = inventory 1, c = inventory 2, d = inventory 3, e = craftingtable, f = armor
        colum = int(colum) - 1

        index = rows[row_id] + colum
        if index < 40 and index > -1: return index


        raise ValueError(f"bad index '{index}'")



class CraftingTable(Inventory):
    def __init__(self, app):
        super().__init__(app)
        self.slots = [0 for i in range(41)]
        self.inventory_image = pg.image.load("assets\\crafting_table_gui.png")
        self.slot_idf = [f"a{i + 1}" for i in range(8)] + [f"b{i + 1}" for i in range(8)] + [f"c{i + 1}" for i in range(8)] + [f"d{i + 1}" for i in range(8)] + [f"e{i + 1}" for i in range(9)]
    def get_armor_group(self):
        [0, 0, 0 ,0]
        
    def get_craft_group(self):
        return self._get_group('e1-e9')
    @staticmethod
    def _idf_to_index(idf):
        if type(idf) != str:
            raise TypeError(f"argument 1(idf) must be a string got '{type(idf).__name__}'")
        if len(idf) != 2:
            raise TypeError(f"argument 1(idf) needs to have lentgh '2' got '{len(idf)}'")
        
        row_id, colum = tuple(idf)


        if not colum.isdigit() or not row_id.isalpha() or colum == "0":
            raise TypeError(f"argument 1(idf) has invalid format ('{idf}') should be like a1")


        rows = {"a":0, "b":8, "c":16, "d":24, "e":32} # a = hand, b = inventory 1, c = inventory 2, d = inventory 3, e = craftingtable,
        colum = int(colum) - 1

        index = rows[row_id] + colum
        if index < 41 and index > -1: return index


        raise ValueError(f"bad index '{index}'")
    def idf_to_pos(self, idf):
        if idf == "e":
            return 519 + self.sx, 146 + self.sy
        
        if len(idf) != 2:
            return None
        
        row, column = idf[0], idf[1]
        x,y = 0,0


        if row in ["a", "b", "c", "d"]:
            if row == "a": y = 520
            elif row == "b": y = 452
            elif row == "c": y = 390
            elif row == "d": y = 330

            if column == "1": x = 23
            elif column == "2": x = 83
            elif column == "3": x = 142
            elif column == "4": x = 200
            elif column == "5": x = 258
            elif column == "6": x = 318
            elif column == "7": x = 376
            elif column == "8": x = 435
            else:
                return None
        elif row == "e":
            if column == "1": x,y = 171, 69
            elif column == "2":x,y = 237, 71
            elif column == "3":x,y = 301, 71
            elif column == "4":x,y = 168, 132
            elif column == "5":x,y = 236, 135
            elif column == "6":x,y = 302, 134
            elif column == "7":x,y = 171, 200
            elif column == "8":x,y = 237, 201
            elif column == "9":x,y = 302, 200
            
            else:
                return None

        else:
            return None


        return (x + self.sx, y + self.sy)

    def pos_to_idf(self, mx, my):
        mx -= self.sx
        my -= self.sy

        if mx > 629 or mx <=0 or my > 600 or my <= 0:
            return None
        
        row = ""
        column = ""

        if mx > 23 and mx < 487 and my > 520 and my < 574:
            row = "a"
        elif mx > 23 and mx < 487 and my > 452 and my < 500:
            row = "b"
        elif mx > 23 and mx < 487 and my > 390 and my < 443:
            row = "c"
        elif mx > 23 and mx < 487 and my > 330 and my < 383:
            row = "d"
        elif mx > 495 and mx < 580 and my > 120 and my < 202:
            return "e"
        
        elif mx > 171 and mx < 356 and my > 67 and my < 256:
            row = "e"

        else:
            return None


        
        


        if row in ["a", "b", "c", "d"]:
            if mx > 23 and mx < 78:
                column = 1
            elif mx > 83 and mx < 137:
                column = 2
            elif mx > 142 and mx < 196:
                column = 3
            elif mx > 200 and mx < 253:
                column = 4
            elif mx > 258 and mx < 312:
                column = 5
            elif mx > 318 and mx < 371:
                column = 6
            elif mx >  376 and mx < 429:
                column = 7
            elif mx > 435 and mx < 489:
                column = 8
            else:
                return None
        elif row == "e":
            if mx > 171 and mx < 227 and my > 69 and my < 127:
                column = 1
            elif mx > 237 and mx < 293 and my > 71 and my < 126:
                column = 2
            elif mx > 301 and mx < 355 and my > 71 and my < 126:
                column = 3
            elif mx > 168 and mx < 226 and my > 132 and my < 186:
                column = 4
            elif mx > 236 and mx < 292 and my > 135 and my < 189:
                column = 5
            elif mx > 302 and mx < 355 and my > 134 and my < 190:
                column = 6
            elif mx > 171 and mx < 228 and my > 200 and my < 254:
                column = 7
            elif mx > 237 and mx < 292 and my > 201 and my < 256:
                column = 8
            elif mx > 302 and mx < 356 and my > 200 and my < 255:
                column = 9
            else:
                return None
       
        
        return row + str(column)
        
    
    def at_open(self, player):
        self.slots[0:32] = player.inventory._get_group("a1-d8")
        print("l")
    def at_close(self, player):
        player.inventory.slots[0:32] = self._get_group("a1-d8")
        self.slots = [0 for i in range(41)]

    def get_crafted_item(self):
        craft_group = list(map(lambda x: 0 if x == 0 else x.item_id, self.get_craft_group()))
        if craft_group == [PLANKS, 0, 0, PLANKS, 0, 0, 0, 0, 0]:
            return (STICK, 4), Item(STICK, 4)
        elif craft_group == [COAL, 0, 0, STICK, 0, 0, 0,0, 0]:
            return (TORCH, 4), Item(TORCH, 4)
        elif craft_group == [STONE, 0, 0, STICK, 0, 0, 0, 0, 0]:
            return (STONE_HAMMER, 1), StoneHammer()
        elif craft_group.count(0) == 8 and craft_group.count(WOOD) == 1:
            return (PLANKS, 4), Item(PLANKS, 4)
        elif craft_group == [PLANKS, PLANKS, 0, PLANKS, PLANKS, 0, 0, 0, 0]:
            return (CRAFTING_TABLE, 1), Item(CRAFTING_TABLE, 1)
        elif craft_group == [PLANKS, PLANKS, PLANKS, 0, STICK, 0, 0, STICK, 0]:
            return (WOODEN_PICAXE, 1), Picaxe(tier=WOODEN_PICAXE, durability=Picaxe().get_durability(WOODEN_PICAXE))
        elif craft_group == [STONE, STONE, STONE, 0, STICK, 0, 0, STICK, 0]:
            return (STONE_PICAXE, 1), Picaxe(tier=STONE_PICAXE, durability=Picaxe().get_durability(STONE_PICAXE))
        elif craft_group.count(WOOD) == 8 and craft_group[1] == 0:
            return (WOODEN_CHESPLATE, 1), Chesplate(WOODEN_CHESPLATE, 1)
        elif craft_group.count(WOOD) == 7 and craft_group[4] == 0 and craft_group[7] == 0:
            return (WOODEN_LEGGINGS, 1), Leggings(WOODEN_LEGGINGS, 1)
        elif craft_group[0:3] == [WOOD, WOOD, WOOD] and craft_group[3:6] == [WOOD,0, WOOD] and craft_group[6:9] == [0, 0, 0]:
            return (WOODEN_HELMET, 1), Helmet(WOODEN_HELMET)
        elif craft_group == [0, 0, 0, WOOD, 0, WOOD, WOOD, 0, WOOD]:
            return (WOODEN_BOOTS, 1), Boots(WOODEN_BOOTS, 1)
        elif craft_group == [PLANKS, PLANKS, 0, PLANKS, STICK, 0, 0, STICK, 0]:
            return (WOODEN_AXE, 1), Axe(tier=WOODEN_AXE, durability=Axe().get_durability(WOODEN_AXE))
        elif craft_group == [STONE, STONE, 0, STONE, STICK, 0, 0, STICK, 0]:
            return (STONE_AXE, 1), Axe(tier=STONE_AXE, durability=Axe().get_durability(STONE_AXE))
        elif craft_group == [0, PLANKS, 0, 0, STICK, 0, 0, STICK, 0]:
            return (WOODEN_SHOVEL, 1), Shovel(tier=WOODEN_SHOVEL, durability=Shovel().get_durability(WOODEN_SHOVEL))
        elif craft_group == [0, STONE, 0, 0, STICK, 0, 0, STICK, 0]:
            return (STONE_SHOVEL, 1), Shovel(tier=STONE_SHOVEL, durability=Shovel().get_durability(STONE_SHOVEL))
        elif craft_group == [0, PLANKS, 0, 0, PLANKS, 0, 0, STICK, 0]:
            return (WOODEN_SWORD, 1), Sword(tier=WOODEN_SWORD, durability=Sword().get_durability(WOODEN_SWORD))
        elif craft_group == [0, STONE, 0, 0, STONE, 0, 0, STICK, 0]:
            return (STONE_SWORD, 1), Sword(tier=STONE_SWORD, durability=Sword().get_durability(STONE_SWORD))
        elif craft_group == [LEAVES, LEAVES, LEAVES, LEAVES, 0, LEAVES, 0, PLANKS, PLANKS]:
            return (BREATHING_MASK, 1), BreathingMask()
        
        else:
            return None
