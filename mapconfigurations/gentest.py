from oblige import *

for seed in range(10060,10100):
    print(seed)
    generator = DoomLevelGenerator(seed)
    generator.set_config({"size":"tiny","misc":1,"steepness":"heaps","doors":"heaps","keys":"heaps","liquids":"none","mons":"none","secrets":"none","teleporters":"heaps","switches":"heaps"})
    generator.generate('{}.wad'.format(seed))
