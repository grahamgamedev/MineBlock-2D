import pygame, json, math, os, threading, data
from random import randint
from time import time

LOADERLOCK = threading.Lock()
TEXTURES = {}
with open("options.txt", "r") as f:
    exec(f.read())

class Player(pygame.sprite.Sprite):
    def __init__(self, hud):
        super().__init__()
 
        self.image = pygame.image.load(SKIN)
        self.rect = self.image.get_rect()
 
        # Set acceleration vector of player
        self.acceleration_x = 0
        self.acceleration_y = 0
 
        # List of sprites we can bump against
        self.level = None
        self.hud = hud
        self.facing = "RIGHT"
        
    def update(self):
        # Gravity
        self.calc_grav()

        # Void damage
        if self.rect.y - VS > 5000:
            self.hud.health(-10)
 
        # Move left/right
        self.rect.x += self.acceleration_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.forground_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.acceleration_x > 0:
                self.rect.right = block.rect.left
            elif self.acceleration_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.acceleration_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.forground_list, False)
        for block in block_hit_list:
            # Fall damage
            if self.acceleration_y > 1:
                if self.acceleration_y > 10:
                    self.hud.health(- round(self.acceleration_y / 4 -3))
                    
            # Reset our position based on the top/bottom of the object.
            if self.acceleration_y > 0:
                self.rect.bottom = block.rect.top
            elif self.acceleration_y < 0:
                self.rect.top = block.rect.bottom
    
            # Stop our vertical movement
            self.acceleration_y = 0
 
    def calc_grav(self):
        if self.acceleration_y == 0:
            self.acceleration_y = 1
        else:
            self.acceleration_y += 0.35
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.acceleration_y >= 0:
            self.acceleration_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            
    def jump(self):
        # move down a bit and see if there is a forground block below us.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.forground_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.acceleration_y = -9
 
    # Player movement
    def go_left(self):
        self.acceleration_x = -6
        self.facing = "LEFT"
    def go_right(self):
        self.acceleration_x = 6
        self.facing = "RIGHT"
    def stop(self):
        self.acceleration_x = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, bid, scale=100):
        super().__init__()
        global TEXTURES
        
        # Only load texture if it hasnt allredy been loaded
        if bid not in TEXTURES.keys():
            self.image = pygame.image.load(os.path.join("Texture Packs", PACK, str(bid) + ".png")).convert_alpha()
            TEXTURES.__setitem__(bid, self.image)
        else:
            self.image = TEXTURES[bid]
            
        # Scale textures only if needed
        if scale != 100:
            if bid == 105:
                self.image = pygame.transform.scale(self.image, (int(scale / 2), scale))
            else:   
                self.image = pygame.transform.scale(self.image, (scale, scale))
        self.rect = self.image.get_rect()
            
class world:
    def __init__(self, player, hud, world_name):
        self.forground_list = pygame.sprite.Group()
        self.background_list = pygame.sprite.Group()
        self.world_name = world_name
        self.player = player
        self.hud = hud
        self.world_shift = 0
        self.vworld_shift = 0
        self.grow_tick = 0

        # Load world
        with open(os.path.join("Worlds", self.world_name), "r") as f:
            d = json.loads(f.read())
        global level; level = d["Level"]
        global WS; WS = d["WS"]
        global VS; VS = d["VS"]
        player.rect.x = d["X"]
        player.rect.y = d["Y"]
        self.hud.hot = d["Hot"]
        self.hud.curent_health = d["Health"]

        x = math.floor(-(WS - player.rect.x) / 100)
        self.chright = math.floor(x / 16)
        self.chleft = math.floor(x / 16)
        
        # Correct world shift      
        self.shift_world(WS)
        self.vshift_world(VS)
        self.hud.blocks()
        self.hud.health(0)

        # Load chunks
        self.thload(self.chright)
        LOADER.join()
        self.chright += 1
        self.chleft -= 1
        self.thload(self.chright)
        LOADER.join()
        self.thload(self.chleft)
        LOADER.join()
        self.chright += 1
        self.chleft -= 1

    def load(self):
        LOADERLOCK.acquire()
        if -128 <= CHUNK * 16 < 128:
            for c in level:
                if c[0] == CHUNK:
                    for b in c[1:]:
                        block = Block(b[2])
                        block.rect.x = b[0] * 100 + WS
                        block.rect.y = b[1] * 100 + VS
                        if b[2] >= 100:
                            self.background_list.add(block)
                        else:
                            self.forground_list.add(block)
        LOADERLOCK.release()
        
    def thload(self, chunk):
        global CHUNK; CHUNK = chunk
        global LOADER
        LOADER = threading.Thread(target=self.load)
        LOADER.start()
        
    def unload(self):
        LOADERLOCK.acquire()
        if -128 <= UNCHUNK * 16 < 128:
            for c in level:
                if c[0] == UNCHUNK:
                    for i, b in enumerate(c[1:]):
                        for platform in self.forground_list:
                            if b[0] * 100 + WS == platform.rect.x:
                                if b[1] * 100 + VS == platform.rect.y:
                                    self.forground_list.remove(platform)
                        for platform in self.background_list:
                            if b[0] * 100 + WS == platform.rect.x:
                                if b[1] * 100 + VS == platform.rect.y:
                                    self.background_list.remove(platform)
        self.save()
        LOADERLOCK.release()
        
    def thunload(self, chunk):
        global UNCHUNK; UNCHUNK = chunk
        global LOADER
        LOADER = threading.Thread(target=self.unload)
        LOADER.start()
 
    def shift_world(self, shift_x):
        self.world_shift += shift_x
        global WS; WS = self.world_shift
 
        # Go through all the sprite lists and shift
        for platform in self.forground_list:
            platform.rect.x += shift_x
        for platform in self.background_list:
            platform.rect.x += shift_x

        # Load extra chunks
        x = math.floor(-(WS - player.rect.x) / 100)
        if (x + 13) / 16 == self.chright:
            self.thload(self.chright)
            self.chright += 1
            self.chleft += 1
            self.thunload(self.chleft)
        if (x - 29) / 16 == self.chleft:
            self.thload(self.chleft)
            self.chleft -= 1
            self.chright -= 1
            self.thunload(self.chright)

    def vshift_world(self, shift_y):
        self.vworld_shift += shift_y
        global VS; VS = self.vworld_shift
 
        # Go through all the sprite lists and shift
        for platform in self.forground_list:
            platform.rect.y += shift_y
        for platform in self.background_list:
            platform.rect.y += shift_y
            
    def save(self):
        with open(os.path.join("Worlds", self.world_name), "w") as f:
            f.write('{"Level":' + str(level) + ",\n")
            f.write('"WS":' + str(WS) + ', "VS":' + str(VS) + ', "X":' + str(player.rect.x) + ', "Y":' + str(player.rect.y) + ", \n")
            f.write('"Hot":' + str(self.hud.hot) + ', \n"Health":' + str(self.hud.curent_health) + '}')
            
    def draw(self, screen):
        # Draw the background
        screen.fill(SKY)
        # Draw all the sprite lists that we have
        self.background_list.draw(screen)
        self.forground_list.draw(screen)

    def update(self):
        if self.grow_tick >= 600:
            self.grow_tick = 0
            for c in level:
                if c[0] in range(self.chleft, self.chright):
                    for i, b in enumerate(c[1:]):
                        # sapling growth
                        if b[2] == 111 and b[3] <= time():
                            self.mine(b[0], b[1])
                            self.tree(b[0], b[1])
                        # Smelting
                        if b[2] == 109 and len(b) > 3:
                            ore = b[3][0]
                            out = b[3][1]
                            fuel = b[3][2]
                            
                            if ore[2] != 0 and fuel[2] != 0:
                                if data.block_types[ore[2]][3] != 0:
                                    if ore[3] > 0 and out[3] < 64:
                                        if data.block_types[fuel[2]][4] != 0:
                                            if fuel[3] >= (1 / data.block_types[fuel[2]][4]):

                                                if out[2] == 0:
                                                    out[2] = data.block_types[ore[2]][3]
                                                out[3] += 1
                                                
                                                ore[3] -= 1
                                                if ore[3] <= 0:
                                                    ore[2] = 0
                                                    
                                                fuel[3] -= (1 / data.block_types[fuel[2]][4])
                                                if fuel[3] <= 0:
                                                    fuel[2] = 0
                            else:
                                fuel[3] = math.floor(fuel[3])
                                if fuel[3] <= 0:
                                    fuel[2] = 0
                            if FURNACE:
                                self.hud.furnace()
        self.grow_tick += 1

    def tree(self, x, y):
        trand = randint(1, 2)
        if trand == 1:
            self.place_block(x,y,100)
            self.place_block(x,y-1,100)
            self.place_block(x+1,y-1,101)
            self.place_block(x-1,y-1,101)
            self.place_block(x+2,y-1,101)
            self.place_block(x-2,y-1,101)
            self.place_block(x,y-2,101)
            self.place_block(x+1,y-2,101)
            self.place_block(x-1,y-2,101)
            self.place_block(x,y-3,101)
        elif trand == 2:
            self.place_block(x,y,100)
            self.place_block(x,y-1,100)
            self.place_block(x,y-2,100)
            self.place_block(x+1,y-2,101)
            self.place_block(x-1,y-2,101)
            self.place_block(x+2,y-2,101)
            self.place_block(x-2,y-2,101)
            self.place_block(x,y-3,101)
            self.place_block(x+1,y-3,101)
            self.place_block(x-1,y-3,101)
            self.place_block(x,y-4,101)
        
    def mine(self, x = None, y = None):
        get = False
        if x == None:
            pos = pygame.mouse.get_pos()
            x = math.floor((pos[0] - WS) / 100)
            y = math.floor((pos[1] - VS) / 100)
            get = True
        for c in level:
            if c[0] in range(self.chleft, self.chright):
                for i, b in enumerate(c[1:]):
                    if [x, y] == b[0:2]:
                        prop = data.block_types[b[2]]
                        if (b[2] == 108 or b[2] == 109) and len(b) == 4:
                            for g, h in enumerate(b[3]):
                                if h[2] != 0:
                                    prop[1] = False
                        if prop[1]:
                            LOADERLOCK.acquire()
                            if prop[2] != 0 and get:
                                self.hud.add_block(prop[2])
                            level.remove(c)
                            c.remove(b)
                            level.append(c)
                            for platform in self.forground_list:
                                if x * 100 + WS == platform.rect.x:
                                    if y * 100 + VS == platform.rect.y:
                                        self.forground_list.remove(platform)
                            for platform in self.background_list:
                                if x * 100 + WS == platform.rect.x:
                                    if y * 100 + VS == platform.rect.y:
                                        self.background_list.remove(platform)
                            LOADERLOCK.release()
        
    def place(self):
        pos = pygame.mouse.get_pos()
        x = math.floor((pos[0] - WS) / 100)
        y = math.floor((pos[1] - VS) / 100)
        bid = self.hud.held[2]
        get = True
        exist = False
        chest = False
        furnace = False
        anvil = False
        plant = False

        # Prevent block placement inside the player
        if bid < 100:
            if x == round(-(WS - player.rect.x) / 100):
                player_y = round(-(VS - player.rect.y) / 100)
                if y == player_y or y == player_y +1:
                    exist = True
        # prevent item placement
        if bid >= 200:
            exist = True
        # prevent plant placement
        elif bid != 0 and data.block_types[bid][0]:
            exist = True
            plant = True
            
        for c in level:
            for i, b in enumerate(c[3:]):          
                if plant and [x, y +1] == b[0:2]:
                    if b[2] == 1 or b[2] == 2:
                            exist = False
                        
                if [x, y] == b[0:2]:
                    if b[2] == 107:
                        self.mine(b[0], b[1])
                        bid = 11
                        get = False
                    elif b[2] == 11:
                        self.mine(b[0], b[1])
                        bid = 107
                        get = False
                    elif b[2] == 105:
                        self.mine(b[0], b[1])
                        bid = 12
                        get = False
                    elif b[2] == 12:
                        self.mine(b[0], b[1])
                        bid = 105
                        get = False
                    elif b[2] == 106:
                        self.mine(b[0], b[1])
                        bid = 13
                        get = False
                    elif b[2] == 13:
                        self.mine(b[0], b[1])
                        bid = 106
                        get = False

                    elif b[2] == 108:
                        exist = True
                        chest = True
                        self.hud.content = b
                    elif b[2] == 109:
                        exist = True
                        furnace = True
                        self.hud.content = b
                    elif b[2] == 114:
                        exist = True
                        self.hud.crafting(data.anvil_recipies)
                        global CRAFTING; CRAFTING = True
                        
                    else:
                        exist = True
                                   
        LOADERLOCK.acquire()               
        if chest:
            self.hud.chest()
        elif furnace:
            self.hud.furnace()
   
        if not exist and bid != 0: 
            if get:
                self.hud.rm_block(1)
                if player.facing == "RIGHT" and bid == 105:
                    bid = 106
            for c in level:
                if c[0] == math.floor(x / 16):
                    level.remove(c)
                    if bid == 111:
                        c.append([x, y, bid, time() + randint(60, 600)])
                    else:
                        c.append([x, y, bid])
                    level.append(c)
            
            block = Block(bid)
            block.rect.x = x * 100 + WS
            block.rect.y = y * 100 + VS
            if bid >= 100:
                self.background_list.add(block)
            else:
                self.forground_list.add(block)
        LOADERLOCK.release()
        
    def place_block(self, x, y, bid):
        exist = False
        for c in level:
            for i, b in enumerate(c[3:]):          
                if [x, y] == b[0:2]:
                    exist = True
                    
        if not exist:
            LOADERLOCK.acquire()
            for c in level:
                if c[0] == math.floor(x / 16):
                    level.remove(c)
                    c.append([x, y, bid])
                    level.append(c)
            
            block = Block(bid)
            block.rect.x = x * 100 + WS
            block.rect.y = y * 100 + VS
            if bid >= 100:
                self.background_list.add(block)
            else:
                self.forground_list.add(block)
            LOADERLOCK.release()

        
class HUD():
    def __init__(self):
        self.hot = []
        self.h = None 
        pygame.font.init()
        self.myfont = pygame.font.Font(FONT, FONT_SIZE)
        
    def blocks(self):
        self.hot_list1 = pygame.sprite.Group()
        self.hot_list2 = pygame.sprite.Group()
        if self.h == None:
            self.change(1)
        gap = "       "
        text = " "
        # Go through hot and add blocks
        for b in self.hot:
            if b[2] != 0:
                block = Block(b[2], scale=50)
                block.rect.x = b[0] * 100
                block.rect.y = b[1] * 100
                self.hot_list1.add(block)
            if b == self.held:
                block = Block("Hotbar2", scale=50)
            else:
                block = Block("Hotbar1", scale=50)
            block.rect.x = b[0] * 100
            block.rect.y = b[1] * 100
            self.hot_list2.add(block)
            
            if len(str(b[3])) == 2:
                text += str(b[3]) + gap
            elif len(str(b[3])) == 1:
                text += str(b[3]) + gap + " "   
        self.textsurface = self.myfont.render(text, False, (0, 0, 0))
        
    def change(self, n):
        # Change hotbar slot
        self.held = self.hot[n-1]
        self.h = n -1
        self.blocks()

    def delete(self):
        # Delete item from hotbar
        self.hot[self.h][2] = 0
        self.hot[self.h][3] = 0
        self.blocks()

    def add_block(self, bid):
        cont = True
        for i, b in enumerate(self.hot):
            if b[2] == bid and cont:
                if not self.hot[i][3] >= 64:
                    self.hot[i][3] += 1
                    cont = False
        if cont:
            for i, b in enumerate(self.hot):
                if b[2] == 0 and cont:
                    self.hot[i][2] = bid
                    self.hot[i][3] += 1
                    cont = False
        self.blocks()
        return not cont
    def rm_block(self, number):
        self.hot[self.h][3] -= number
        if self.hot[self.h][3] <= 0:
            self.hot[self.h][2] = 0
        self.blocks()
        
    def health(self, health):
        self.before = time()
        self.curent_health += health
        self.health_list = pygame.sprite.Group()
        x = SCREEN_WIDTH
        for i in range(self.curent_health):
            block = Block("Health1")
            x -= 30
            block.rect.x = x
            block.rect.y = 10
            self.health_list.add(block)
        for i in range(10 - self.curent_health):
            block = Block("Health2")
            x -= 30
            block.rect.x = x
            block.rect.y = 10
            self.health_list.add(block)
        
    def crafting(self, recipies):
        self.recipies = recipies
        self.crafting_list1 = pygame.sprite.Group()
        self.crafting_list2 = pygame.sprite.Group()
        self.backer = pygame.image.load(os.path.join("Texture Packs", PACK, "Crafting1.png")).convert()
        x = 50
        gap = "         "
        text = " "
        
        # Go through recipies and add ingrediants
        for i, b in enumerate(self.recipies):
            block = Block(b[0], scale=50)
            x += 60
            block.rect.x = x
            block.rect.y = 450
            self.crafting_list1.add(block)

            if b[1] != 0:
                block = Block(b[1], scale=50)
                block.rect.x = x
                block.rect.y = 380
                self.crafting_list1.add(block)
                got = False
                for h in self.hot:
                    if b[1] == h[2]:
                        got = True
                if not got:
                    block = Block("Crafting2")
                    block.rect.x = x
                    block.rect.y = 380
                    self.crafting_list2.add(block)
            if b[2] != 0:
                block = Block(b[2], scale=50)
                block.rect.x = x
                block.rect.y = 325
                self.crafting_list1.add(block)
                got = False
                for h in self.hot:
                    if b[2] == h[2]:
                        got = True
                if not got:
                    block = Block("Crafting2")
                    block.rect.x = x
                    block.rect.y = 325
                    self.crafting_list2.add(block)
            if b[3] != 0:
                block = Block(b[3], scale=50)
                block.rect.x = x
                block.rect.y = 270
                self.crafting_list1.add(block)
                got = False
                for h in self.hot:
                    if b[3] == h[2]:
                        got = True 
                if not got:
                    block = Block("Crafting2")
                    block.rect.x = x
                    block.rect.y = 270
                    self.crafting_list2.add(block)
            if b[4] != 0:
                block = Block(b[4], scale=50)
                block.rect.x = x
                block.rect.y = 215
                self.crafting_list1.add(block)
                got = False
                for h in self.hot:
                    if b[4] == h[2]:
                        got = True
                if not got:
                    block = Block("Crafting2")
                    block.rect.x = x
                    block.rect.y = 215
                    self.crafting_list2.add(block)
            if b[5] != 0:
                block = Block(b[5], scale=50)
                block.rect.x = x
                block.rect.y = 160
                self.crafting_list1.add(block)
                got = False
                for h in self.hot:
                    if b[5] == h[2]:
                        got = True
                if not got:
                    block = Block("Crafting2")
                    block.rect.x = x
                    block.rect.y = 160
                    self.crafting_list2.add(block)
                
            if len(str(b[-1])) == 2:
                text += str(b[-1]) + gap
            elif len(str(b[-1])) == 1:
                text += str(b[-1]) + gap + " "
        self.craftingtext = self.myfont.render(text, False, (0, 0, 0))
                    
    def craft(self):
        pos = pygame.mouse.get_pos()
        selection = math.floor((pos[0] - 110)/60)
        if pos[1] >= 450 and pos[1] <= 500:
            if selection < len(self.recipies):
                
                # Test for all ingrediants
                hot = [[i for i in row] for row in self.hot]
                for r in self.recipies[selection][1:-1]:
                    if r != 0:
                        ingrediants = False
                        for i, b in enumerate(hot):
                            if b[2] == r and not ingrediants:
                                b[3] -= 1
                                if hot[i][3] <= 0:
                                    hot[i][2] = 0
                                ingrediants = True
                
                if ingrediants:
                    # Test for hotbar space
                    for i in range(self.recipies[selection][-1]):
                        over = self.add_block(self.recipies[selection][0])

                    # if sucsessfull take ingrediants from hotbar
                    if over:
                        self.hot = hot
                        # Put crafted item into hotbar
                        for i in range(self.recipies[selection][-1]):
                            self.add_block(self.recipies[selection][0])                    
                self.crafting(self.recipies)

    def chest(self):
        global CHEST; CHEST = True
        # Create new chest
        if len(self.content) == 3:
            self.content.append(data.chest)
    
        self.chest_list = pygame.sprite.Group()
        self.backer = pygame.image.load(os.path.join("Texture Packs", PACK, "Chest1.png")).convert()
        gap = "        "
        text = " "
        
        for i, b in enumerate(self.content[3]):
            if b[2] != 0:
                block = Block(b[2], scale=50)
                block.rect.x = b[0]
                block.rect.y = b[1]
                self.chest_list.add(block)

            if i == 9:
                self.chesttext1 = self.myfont.render(text, False, (0, 0, 0))
                text = " "
            if i == 18:
                self.chesttext2 = self.myfont.render(text, False, (0, 0, 0))
                text = " "
                
            if not b[-1] <= 1:
                if len(str(b[-1])) == 2:
                    text += str(b[-1]) + gap
                elif len(str(b[-1])) == 1:
                    text += str(b[-1]) + gap + "  "
            else:
                text += "    " + gap 
        self.chesttext3 = self.myfont.render(text, False, (0, 0, 0))

    def furnace(self):
        global FURNACE; FURNACE = True
        # Create new furnace
        if len(self.content) == 3:
            self.content.append(data.furnace)

        self.furnace_list = pygame.sprite.Group()
        self.backer = pygame.image.load(os.path.join("Texture Packs", PACK, "Furnace1.png")).convert()
        text = ""
        if self.content[3][0][3] > 1:
            text = str(self.content[3][0][3])
        self.furnacetext1 = self.myfont.render(text, False, (0, 0, 0))
        text = ""
        if self.content[3][1][3] > 1:
            text = str(self.content[3][1][3])
        self.furnacetext2 = self.myfont.render(text, False, (0, 0, 0))
        text = ""
        if self.content[3][2][3] > 1:
            text = str(self.content[3][2][3])
        self.furnacetext3 = self.myfont.render(text, False, (0, 0, 0))

        # Smelting indicator
        ore = self.content[3][0]
        out = self.content[3][1]
        fuel = self.content[3][2]
        
        if ore[2] != 0 and fuel[2] != 0:
            if data.block_types[ore[2]][3] != 0:
                if ore[3] > 0 and out[3] < 64:
                    if data.block_types[fuel[2]][4] != 0:
                        if fuel[3] >= (1 / data.block_types[fuel[2]][4]):
                            block = Block("Furnace2")
                            block.rect.x = 230
                            block.rect.y = 320
                            self.furnace_list.add(block)
        
        for i, b in enumerate(self.content[3]):
            if b[2] != 0:
                block = Block(b[2], scale=50)
                block.rect.x = b[0]
                block.rect.y = b[1]
                self.furnace_list.add(block)
        
    def put(self):
        # Put item into GUI
        pos = pygame.mouse.get_pos()
        x = math.floor((pos[0] - 110)/60) * 60 + 110
        y = math.floor((pos[1] - 200)/60) * 60 + 200
  
        for i, b in enumerate(self.content[3]):
            if b[0] == x and b[1] == y:
                if self.content[3][i][2] == 0:
                    if self.held[3] != 0:       
                        if CTRL:
                            self.content[3][i][2] = self.held[2]
                            self.content[3][i][3] = 1
                            self.rm_block(1)
                        else:
                            self.content[3][i][2:] = self.held[2:]
                            self.rm_block(self.held[3])
                        
                elif self.content[3][i][2] == self.held[2]:
                    if self.held[3] != 0:
                        if self.content[3][i][3] + self.held[3] <= 64:
                            if CTRL:
                                self.content[3][i][3] += 1
                                self.rm_block(1)
                            else:
                                self.content[3][i][3] += self.held[3]
                                self.rm_block(self.held[3])
        if CHEST:
            self.chest()
        if FURNACE:
            self.furnace()

    def get(self):
        # Take item from GUI
        pos = pygame.mouse.get_pos()
        x = math.floor((pos[0] - 110)/60) * 60 + 110
        y = math.floor((pos[1] - 200)/60) * 60 + 200
        
        for i, b in enumerate(self.content[3]):
            if b[0] == x and b[1] == y:
                if type(self.content[3][i][3]) == float:
                    self.content[3][i][3] = math.floor(self.content[3][i][3])
                if self.content[3][i][2] != 0:
                    if CTRL:
                       self.add_block(self.content[3][i][2])
                       self.content[3][i][3] -= 1
                       if self.content[3][i][3] <= 0:
                           self.content[3][i][2] = 0
                    else:
                        for item in range(self.content[3][i][3]):
                            self.add_block(self.content[3][i][2])
                        self.content[3][i][2:] = [0,0]
        if CHEST:
            self.chest()
        if FURNACE:
            self.furnace()
                                    
    def draw(self, screen):
        # Draw HUD
        if SHOW_HUD:
            self.hot_list1.draw(screen)
            self.hot_list2.draw(screen)
            screen.blit(self.textsurface,(0,55))
            self.health_list.draw(screen)
        if DEBUG:
            screen.blit(self.debug,(0,100))

        # Draw any open GUIs
        if CRAFTING:
            screen.blit(self.backer, (100,150))
            self.crafting_list1.draw(screen)
            self.crafting_list2.draw(screen)
            
            screen.blit(self.craftingtext,(110,480))
        if CHEST:
            screen.blit(self.backer, (100,250))
            self.chest_list.draw(screen)
            
            screen.blit(self.chesttext1,(110,290))
            screen.blit(self.chesttext2,(110,350))
            screen.blit(self.chesttext3,(110,410))
        if FURNACE:
            screen.blit(self.backer, (100,250))
            self.furnace_list.draw(screen)
            
            screen.blit(self.furnacetext1,(230,290))
            screen.blit(self.furnacetext2,(350,350))
            screen.blit(self.furnacetext3,(230,410))
        
    def update(self):
        # Health regeneration
        if time() - self.before > 30 and self.curent_health < 10:
            self.health(1) 
        if DEBUG:
            y = math.floor(-(VS - player.rect.y) / 100)
            x = math.floor(-(WS - player.rect.x) / 100)
            text = " Player: X " + str(x) + "  Y " + str(y)
            pos = pygame.mouse.get_pos()
            x = math.floor((pos[0] - WS) / 100)
            y = math.floor((pos[1] - VS) / 100)
            text += "  Mouse: X " + str(x) + "  Y " + str(y)
            self.debug = self.myfont.render(text, False, (0, 0, 0))
    

def main(world_name):
    # Random loading screen
    loadings = 0
    for i, b in enumerate(os.listdir(os.path.join("Texture Packs", PACK))):
        if b[0:-5] == "Loading":
            loadings += 1
    load = str(randint(1, loadings))
    pygame.init()

    # Set the height and width of the screen
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    ro = SCREEN_WIDTH - 150
    bo = SCREEN_HEIGHT - 150

    # Icon
    pygame.display.set_caption("MineBlock 2D")
    icon = pygame.image.load(os.path.join("Texture Packs", PACK, "5.png"))
    pygame.display.set_icon(icon)

    # Loading screen
    loading = pygame.image.load(os.path.join("Texture Packs", PACK, "Loading" + load + ".png")).convert()
    loading = pygame.transform.scale(loading, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(loading, (0,0))
    pygame.display.flip()

    # Load HUD
    hud = HUD()
    global CRAFTING; CRAFTING = False
    global CHEST; CHEST = False
    global FURNACE; FURNACE = False
    global SHOW_HUD
    global DEBUG
    global CTRL; CTRL = False
    
    # Create the player
    global player; player = Player(hud)
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)

    # Load world
    current_level = world(player, hud, world_name)
    player.level = current_level

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    dead = False
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if not CRAFTING and not CHEST and not FURNACE:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.go_left()
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.go_right()       
                    if event.key == pygame.K_SPACE:
                        player.jump()
                            
                if event.key == pygame.K_e:
                    if CRAFTING:
                        CRAFTING = False
                    elif not CHEST and not FURNACE:
                        hud.crafting(data.crafting_recipies)
                        CRAFTING = True
                        
                if event.key == pygame.K_ESCAPE:
                    if CRAFTING:
                        CRAFTING = False
                    elif CHEST:
                        CHEST = False
                    elif FURNACE:
                        FURNACE = False
                    else:
                        done = True
                        
                if event.key == pygame.K_F1:
                    if SHOW_HUD:
                        SHOW_HUD = False
                    else:
                        SHOW_HUD = True
                if event.key == pygame.K_F2:
                    n = str(len(os.listdir("Screenshots")) +1)
                    pygame.image.save(screen, os.path.join("Screenshots", "Screenshot" + n + ".png"))
                if event.key == pygame.K_F3:
                    if DEBUG:
                        DEBUG = False
                    else:
                        DEBUG = True
                if event.key == pygame.K_F4:
                    current_level.save()
                if event.key == pygame.K_DELETE:
                    hud.delete()

                if event.key == pygame.K_LCTRL:
                    CTRL = True
                    
                if event.key == pygame.K_1:
                    hud.change(1)
                if event.key == pygame.K_2:
                    hud.change(2)
                if event.key == pygame.K_3:
                    hud.change(3)
                if event.key == pygame.K_4:
                    hud.change(4)
                if event.key == pygame.K_5:
                    hud.change(5)
                if event.key == pygame.K_6:
                    hud.change(6)
                if event.key == pygame.K_7:
                    hud.change(7)
                if event.key == pygame.K_8:
                    hud.change(8)
                if event.key == pygame.K_9:
                    hud.change(9)
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a and player.acceleration_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d and player.acceleration_x > 0:
                    player.stop()
                    
                if event.key == pygame.K_LCTRL:
                    CTRL = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if CRAFTING:
                        hud.craft()
                    elif CHEST or FURNACE:
                        hud.get()
                    else:
                        current_level.mine()
                if event.button == 3:
                    if CHEST or FURNACE:
                        hud.put()
                    elif not CRAFTING:
                        current_level.place()
                        
                if event.button == 4:
                    if hud.h < 8:
                        hud.change(hud.h + 2)
                    else:
                        hud.change(1)
                if event.button == 5:
                    if hud.h > 0:
                        hud.change(hud.h)
                    else:
                        hud.change(9)

        # Update the player.
        active_sprite_list.update()
        # Update HUD
        hud.update()
        # Update world
        current_level.update()

        # Check that the player is alive
        if hud.curent_health <= 0:
            done = True
            dead = True

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= ro:
            diff = player.rect.right - ro
            player.rect.right = ro
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 150:
            diff = 150 - player.rect.left
            player.rect.left = 150
            current_level.shift_world(diff)

        # If the player gets near the bottom side, shift the world up (-y)
        if player.rect.bottom >= bo:
            diff = player.rect.bottom - bo
            player.rect.bottom = bo
            current_level.vshift_world(-diff)

        # If the player gets near the top side, shift the world down (+y)
        if player.rect.top <= 150:
            diff = 150 - player.rect.top
            player.rect.top = 150
            current_level.vshift_world(diff)

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        hud.draw(screen)

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
    # Death screen    
    restart = False
    if dead:
        death = pygame.image.load(os.path.join("Texture Packs", PACK, "Death.png")).convert_alpha()
        death = pygame.transform.scale(death, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(death, (0,0))
        pygame.display.flip()
        while dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    dead = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        dead = False
                    if event.key == pygame.K_RETURN:
                        restart = True
                        dead = False        
        hud.curent_health = 10
        hud.hot = data.hot
        player.rect.x = 0
        player.rect.y = 200
        global WS; WS = 0
        global VS; VS = -2000
    
    # save
    current_level.save()
    
    if restart:
        main(world_name)
    else:
        LOADERLOCK.acquire()
        LOADER.join()
        pygame.quit()
        LOADERLOCK.release()

# Uncomment to bypass launcher    
# main("test.json")


        
        

