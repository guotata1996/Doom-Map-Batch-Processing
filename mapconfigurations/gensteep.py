from oblige import *

for seed in range(3900, 5000):
    print(seed)
    generator = DoomLevelGenerator(seed)
    generator.set_config({"size":"tiny","misc":1,"steepness":"heaps","doors":"none","keys":"none","liquids":"none","mons":"none","secrets":"none","teleporters":"none","switches":"none"})
    generator.generate('{}.wad'.format(seed))
