# Block properties
# bid:[plant, brakeable, bid to get, gravity effected, bid to smelt, fuel]
block_types = {1:[False,True,1,False,0,0], 2:[False,True,2,False,0,0],
               3:[False,True,3,False,0,0], 4:[False,False,0,False,0,0],
               5:[False,False,0,False,0,0], 6:[False,True,6,False,0,64],
               7:[False,True,7,False,202,0], 8:[False,True,8,False,203,0],
               9:[False,True,9,False,10,0], 10:[False,True,10,False,0,8],
               11:[False,True,107,False,0,1], 12:[False,True,105,False,0,2],
               13:[False,True,105,False,0,2], 14:[False,True,14,False,202,0],
               15:[False,True,15,False,203,0], 16:[False,True,16,True,17,0],
               17:[False,True,0,False,17,0], 18:[False,True,18,False,3,0],
               19:[False,True,19,True,0,0],
                
               100:[False,True,100,False,0,8], 101:[False,True,111,False,0,0],
               102:[True,True,0,True,0,0], 103:[True,True,103,True,0,0],
               104:[True,True,104,True,0,0], 105:[False,True,105,False,0,2],
               106:[False,True,105,False,0,2], 107:[False,True,107,False,0,1],
               108:[False,True,108,False,0,8], 109:[False,True,109,False,0,0],
               110:[False,True,110,False,0,2], 111:[True,True,111,False,0,0],
               112:[False,True,112,False,0,8], 113:[False,True,113,False,202,0],
               114:[False,True,114,False,202,0], 115:[False,True,3,False,0,0],
               116:[False,True,116,False,203,0], 117:[False,True,117,False,0,1],
               118:[False,True,118,False,0,1],

               200:[False,True,0,False,0,0.25], 201:[False,True,0,False,0,8],
               202:[False,True,0,False,202,0], 203:[False,True,0,False,203,0]}

# Crafting recipies
# [bid to craft, bids,required,0,0,0, quantity to get]
crafting_recipies = [[112, 100,0,0,0,0, 1], [10, 100,0,0,0,0, 1],
                     [200, 10,0,0,0,0, 32], [107, 10,0,0,0,0, 4],
                     [105, 10,0,0,0,0, 2], [110, 10,0,0,0,0, 4],
                     [108, 10,10,0,0,0, 1], [109, 3,3,0,0,0, 1],
                     [115, 3,0,0,0,0, 1], [18, 3,0,0,0,0, 1],
                     [114, 202,202,202,202,202, 1], [117, 10,200,201,0,0, 5],
                     [118, 10,103,104,0,0, 5]]

anvil_recipies = [[201, 6,0,0,0,0, 9], [14, 202,202,202,202,202, 1],
                  [113, 202,202,202,0,0, 1], [15, 203,203,203,203,203, 1],
                  [116, 203,203,203,0,0, 1]]

# Empty chest
chest = [[110, 260, 0, 0], [170, 260, 0, 0], [230, 260, 0, 0], [290, 260, 0, 0], [350, 260, 0, 0], [410, 260, 0, 0], [470, 260, 0, 0], [530, 260, 0, 0], [590, 260, 0, 0],
         [110, 320, 0, 0], [170, 320, 0, 0], [230, 320, 0, 0], [290, 320, 0, 0], [350, 320, 0, 0], [410, 320, 0, 0], [470, 320, 0, 0], [530, 320, 0, 0], [590, 320, 0, 0],
         [110, 380, 0, 0], [170, 380, 0, 0], [230, 380, 0, 0], [290, 380, 0, 0], [350, 380, 0, 0], [410, 380, 0, 0], [470, 380, 0, 0], [530, 380, 0, 0], [590, 380, 0, 0]]

# Empty furnace
furnace = [[230,260,0,0], [350,320,0,0], [230,380,0,0]]

# Empty hotbar
hot = [[0, 0, 0, 0], [0.5, 0, 0, 0], [1, 0, 0, 0], [1.5, 0, 0, 0], [2, 0, 0, 0], [2.5, 0, 0, 0], [3, 0, 0, 0], [3.5, 0, 0, 0], [4, 0, 0, 0], [4.5, 0, 0, 0]]

# Default options
options = """# This file is used to configure MineBlock 2D

# Sky color
SKY = (135, 206, 250)
#SKY = (100, 106, 150)

# Font and size
FONT = "Arial Black.ttf"
FONT_SIZE = 16

# Window size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Skin filename
SKIN = "Default_skin.png"

# Texture pack folder
PACK = "Default"

# Debug info
DEBUG = False

# Show HUD
SHOW_HUD = True
"""
