import random

#map
'START BLOCK'
#house
houseXs = (-200,600,1400)
doorXs = (-200+110,600+110,1400+110)

#grass
grassdata = list()

for i in range(-50,50):
    #generate grass in patches
    for j in range(random.randint(1,4)):
        grass = dict()
    
        grass['X'] = random.randint(-50,50)+i*random.randint(500,700)
        grass['type'] = random.randint(0,1)

        grassdata.append(grass)
'END BLOCK'
