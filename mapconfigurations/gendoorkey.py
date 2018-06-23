from oblige import *

for seed in range(1000,1110):
    print(seed)
    generator = DoomLevelGenerator(seed)
    generator.set_config({"size":"tiny","misc":1,"doors":"heaps","keys":"heaps","mons":"none","secrets":"none"})
    generator.generate('{}.wad'.format(seed))
