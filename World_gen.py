import os.path, data
from random import randint

def main(WORLD):  
    level = []
    ch = None
    
    rand = 0
    crand = 0
    coal_rand = 0
    iron_rand = 0
    gold_rand = 0
    diamond_rand = 0
        
    # Hotbar coords
    hot = data.hot

    def tree(x, y, trand):
        if trand == 1:
            ch.append([x,y,100])
            ch.append([x,y-1,100])
            ch.append([x+1,y-1,101])
            ch.append([x-1,y-1,101])
            ch.append([x+2,y-1,101])
            ch.append([x-2,y-1,101])
            ch.append([x,y-2,101])
            ch.append([x+1,y-2,101])
            ch.append([x-1,y-2,101])
            ch.append([x,y-3,101])
        elif trand == 2:
            ch.append([x,y,100])
            ch.append([x,y-1,100])
            ch.append([x,y-2,100])
            ch.append([x+1,y-2,101])
            ch.append([x-1,y-2,101])
            ch.append([x+2,y-2,101])
            ch.append([x-2,y-2,101])
            ch.append([x,y-3,101])
            ch.append([x+1,y-3,101])
            ch.append([x-1,y-3,101])
            ch.append([x,y-4,101])
            

    print("Generating")
    for x in range(-128, 128 + 1):
        # Start new chunk
        if ch == None:
            ch = [round(x / 16)]  
        if x % 16 == 0:
            print(round(x / 16))
            level.append(ch)
            ch = [round(x / 16)]

        # World borders
        if x == -128 or x == 127:
            print(x)
            for y in range(48):
                ch.append([x,y,4])
            ch.append([x,49,5])
            ch.append([x,50,5])
        else:      
            # Underground
            for y in range(29, 48):
                if crand == 0:
                    crand = randint(1, 1000)
                if crand > 50:
                    if coal_rand == 0:
                        coal_rand = randint(1, 200)
                    if iron_rand == 0:
                        iorn_rand = randint(1, 100)
                    if gold_rand == 0:
                        gold_rand = randint(1, 200)
                    if diamond_rand == 0:
                        diamond_rand = randint(1, 300)
                        
                    if coal_rand < 10:
                        ch.append([x,y,6])
                    elif iorn_rand < 10:
                        ch.append([x,y,7])
                    elif gold_rand < 5 and y > 40:
                        ch.append([x,y,8])
                    elif diamond_rand < 5 and y > 44:
                        ch.append([x,y,9])
                    else:
                        ch.append([x,y,3])
                    coal_rand -= 1
                    iorn_rand -= 1
                    gold_rand -= 1
                    diamond_rand -= 1
                else:
                    ch.append([x,y,115])
                crand -= 1
            # Bedrock
            if randint(1, 2) == 1:
                ch.append([x,48,3])
            else:
                ch.append([x,48,5])
            ch.append([x,49,5])
            ch.append([x,50,5])
            
            # Ground level
            if rand == 0:
                rand = randint(1, 10)
            # High
            if rand > 4:
                ch.append([x,28,3])
                if randint(1, 2) == 1:
                        ch.append([x,27,3])
                else:
                        ch.append([x,27,2])
                ch.append([x,26,2])
                ch.append([x,25,2])
                ch.append([x,24,1])

                # Vegitation
                trand = randint(1, 50)
                if trand < 3:
                      tree(x, 23, trand)  
                elif randint(1, 5) == 1:
                        ch.append([x,23,102])
                elif randint(1, 7) == 1:
                        ch.append([x,23,103])
                elif randint(1, 7) == 1:
                        ch.append([x,23,104])
            # Low           
            else:
                if randint(1, 2) == 1:
                        ch.append([x,28,3])
                else:
                        ch.append([x,28,2])
                ch.append([x,27,2])
                ch.append([x,26,2])
                ch.append([x,25,1])

                # Vegitation
                trand = randint(1, 50)
                if trand < 3:
                      tree(x, 24, trand)  
                elif randint(1, 5) == 1:
                        ch.append([x,24,102])
                elif randint(1, 7) == 1:
                        ch.append([x,24,103])
                elif randint(1, 7) == 1:
                        ch.append([x,24,104])
            rand -= 1

    # Save
    with open(os.path.join("Worlds", WORLD), "w") as f:
            f.write('{"Level":' + str(level[1:]) + ', \n"WS":0, "VS":-2000, "X":0, "Y":200, \n"Hot":' + str(hot) + ', \n"Health":10' + '}')
    print("Finished")
