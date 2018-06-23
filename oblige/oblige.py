#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess
import random
import math
import shutil

oblige_version = "7.70"

oblige_frequency_vals = ["mixed", "none", "rare", "few", "less", "some", "more", "heaps"]
oblige_mon_quantity_vals = ["default", "none", "scarce", "few", "less", "some", "more", "heaps", "insane"]
oblige_wep_quantity_vals = ["default", "none", "scarce", "less", "plenty", "more", "heaps", "loveit"]

# First value is default one
oblige_options = {

    # General options
    "game": ["doom2", "doom"],
    "engine": ["zdoom", "gzdoom", "vizdoom"],
    "length": ["single", "few", "episode", "game"],
    "theme": ["original", "mostly_original", "epi", "mostly_epi", "bit_mixed", "jumble",
              "tech", "mostly_tech", "urban", "mostly_urban", "hell", "mostly_hell"],

    "size": ["micro", "tiny", "small", "regular", "large", "extreme", "epi", "prog", "mixed"],
    "outdoors": oblige_frequency_vals,
    "caves": oblige_frequency_vals,
    "liquids": oblige_frequency_vals,
    "hallways": oblige_frequency_vals,
    "teleporters": oblige_frequency_vals,
    "steepness": oblige_frequency_vals,

    "mons": ["scarce", "few", "less", "some", "more", "nuts", "mixed", "none"],
    "strength": ["weak", "easier", "normal", "harder", "tough", "crazy"],
    "ramp_up": ["slow", "medium", "fast", "episodic"],
    "bosses": ["none", "easier", "normal", "harder"],
    "traps": ["none"] + oblige_frequency_vals,
    "cages": ["none"] + oblige_frequency_vals,

    "health": ["none", "scarce", "less", "bit_less", "normal", "bit_more", "more", "heaps"],
    "ammo": ["none", "scarce", "less", "bit_less", "normal", "bit_more", "more", "heaps"],
    "weapons": ["none", "very_soon", "sooner", "normal", "later", "very_late"],
    "items": ["none", "rare", "less", "normal", "more", "heaps"],
    "secrets": oblige_frequency_vals,

    # Modules' options
    "doom_mon_control": [0, 1],
    # doom_mon_control module options
    "Spiderdemon": oblige_mon_quantity_vals,
    "caco": oblige_mon_quantity_vals,
    "gunner": oblige_mon_quantity_vals,
    "skull": oblige_mon_quantity_vals,
    "demon": oblige_mon_quantity_vals,
    "knight": oblige_mon_quantity_vals,
    "vile": oblige_mon_quantity_vals,
    "zombie": oblige_mon_quantity_vals,
    "Cyberdemon": oblige_mon_quantity_vals,
    "ss_nazi": oblige_mon_quantity_vals,
    "baron": oblige_mon_quantity_vals,
    "spectre": oblige_mon_quantity_vals,
    "arach": oblige_mon_quantity_vals,
    "mancubus": oblige_mon_quantity_vals,
    "revenant": oblige_mon_quantity_vals,
    "pain": oblige_mon_quantity_vals,
    "imp": oblige_mon_quantity_vals,
    "shooter": oblige_mon_quantity_vals,

    "doom_weapon_control": [0, 1],
    # doom_weapon_control module options
    "super": oblige_wep_quantity_vals,
    "chain": oblige_wep_quantity_vals,
    "launch": oblige_wep_quantity_vals,
    "bfg": oblige_wep_quantity_vals,
    "plasma": oblige_wep_quantity_vals,
    "shotty": oblige_wep_quantity_vals,

    "export_map": [0, 1],

    "misc": [1, 0],
    # misc module options
    "pistol_starts": ["yes", "no"],
    "alt_starts": ["no", "yes"],
    "big_rooms": oblige_frequency_vals,
    "parks": oblige_frequency_vals,
    "windows": oblige_frequency_vals,
    "symmetry": oblige_frequency_vals,
    "darkness": oblige_frequency_vals,
    "mon_variety": oblige_frequency_vals,
    "barrels": oblige_frequency_vals,
    "doors": oblige_frequency_vals,
    "keys": oblige_frequency_vals,
    "switches": oblige_frequency_vals,

    "music_swapper": [1, 0],

    "sky_generator": [1, 0],

    "small_spiderdemon": [0, 1],

    "stealth_mons": [0, 1],
    "stealth_mons_qty": ["normal", "less", "more"],

    "stealth_mon_control": [0, 1],
    # stealth_mon_control module options
    "stealth_demon": oblige_mon_quantity_vals,
    "stealth_baron": oblige_mon_quantity_vals,
    "stealth_zombie": oblige_mon_quantity_vals,
    "stealth_caco": oblige_mon_quantity_vals,
    "stealth_imp": oblige_mon_quantity_vals,
    "stealth_mancubus": oblige_mon_quantity_vals,
    "stealth_arach": oblige_mon_quantity_vals,
    "stealth_revenant": oblige_mon_quantity_vals,
    "stealth_shooter": oblige_mon_quantity_vals,
    "stealth_vile": oblige_mon_quantity_vals,
    "stealth_knight": oblige_mon_quantity_vals,
    "stealth_gunner": oblige_mon_quantity_vals,

    "zdoom_marines": [0, 1],
    "zdoom_marines_qty": ["plenty", "scarce", "heaps"],

    "zdoom_marine_control": [0, 1],
    # zdoom_marine_control module options
    "marine_bfg": oblige_mon_quantity_vals,
    "marine_chain": oblige_mon_quantity_vals,
    "marine_pistol": oblige_mon_quantity_vals,
    "marine_ssg": oblige_mon_quantity_vals,
    "marine_rail": oblige_mon_quantity_vals,
    "marine_berserk": oblige_mon_quantity_vals,
    "marine_plasma": oblige_mon_quantity_vals,
    "marine_rocket": oblige_mon_quantity_vals,
    "marine_fist": oblige_mon_quantity_vals,
    "marine_saw": oblige_mon_quantity_vals,
    "marine_shotty": oblige_mon_quantity_vals,
}

oblige_config_str = """-- CONFIG FILE : OBLIGE 7.70
-- OBLIGE Level Maker (C) 2006-2017 Andrew Apted
-- http://oblige.sourceforge.net/
-- Generated by PyOblige
-- https://github.com/mwydmuch/PyOblige

seed = {seed}

---- Game Settings ----

game = {game}
engine = {engine}
length = {length}
theme = {theme}

---- Architecture ----

size = {size}
outdoors = {outdoors}
caves = {caves}
liquids = {liquids}
hallways = {hallways}
teleporters = {teleporters}
steepness = {steepness}

---- Monsters ----

mons = {mons}
strength = {strength}
ramp_up = {ramp_up}
bosses = {bosses}
traps = {traps}
cages = {cages}

---- Pickups ----

health = {health}
ammo = {ammo}
weapons = {weapons}
items = {items}
secrets = {secrets}

---- Other Modules ----

@doom_mon_control = {doom_mon_control}
  Spiderdemon = {Spiderdemon}
  caco = {caco}
  gunner = {gunner}
  skull = {skull}
  demon = {demon}
  knight = {knight}
  vile = {vile}
  zombie = {zombie}
  Cyberdemon = {Cyberdemon}
  ss_nazi = {ss_nazi}
  baron = {baron}
  spectre = {spectre}
  arach = {arach}
  mancubus = {mancubus}
  revenant = {revenant}
  pain = {pain}
  imp = {imp}
  shooter = {shooter}

@doom_weapon_control = {doom_weapon_control}
  super = {super}
  chain = {chain}
  launch = {launch}
  bfg = {bfg}
  plasma = {plasma}
  shotty = {shotty}

@export_map = {export_map}

@misc = {misc}
  pistol_starts = {pistol_starts}
  alt_starts = {alt_starts}
  big_rooms = {big_rooms}
  parks = {parks}
  windows = {windows}
  symmetry = {symmetry}
  darkness = {darkness}
  mon_variety = {mon_variety}
  barrels = {barrels}
  doors = {doors}
  keys = {keys}
  switches = {switches}

@music_swapper = {music_swapper}

@sky_generator = {sky_generator}

@small_spiderdemon = {small_spiderdemon}

@stealth_mon_control = {stealth_mon_control}
  stealth_demon = {stealth_demon}
  stealth_baron = {stealth_baron}
  stealth_zombie = {stealth_zombie}
  stealth_caco = {stealth_caco}
  stealth_imp = {stealth_imp}
  stealth_mancubus = {stealth_mancubus}
  stealth_arach = {stealth_arach}
  stealth_revenant = {stealth_revenant}
  stealth_shooter = {stealth_shooter}
  stealth_vile = {stealth_vile}
  stealth_knight = {stealth_knight}
  stealth_gunner = {stealth_gunner}

@stealth_mons = {stealth_mons}
  qty = {stealth_mons_qty}

@zdoom_marine_control = {zdoom_marine_control}
  marine_bfg = {marine_bfg}
  marine_chain = {marine_chain}
  marine_pistol = {marine_pistol}
  marine_ssg = {marine_ssg}
  marine_rail = {marine_rail}
  marine_berserk = {marine_berserk}
  marine_plasma = {marine_plasma}
  marine_rocket = {marine_rocket}
  marine_fist = {marine_fist}
  marine_saw = {marine_saw}
  marine_shotty = {marine_shotty}

@zdoom_marines = {zdoom_marines}
  qty = {zdoom_marines_qty}

-- END --
"""


def oblige_unique_vals(vals):
    seen = set()
    return [x for x in vals if not (x in seen or seen.add(x))]


def oblige_realpath(local_path):
    return os.path.realpath(os.path.realpath(os.path.join(os.path.dirname(__file__), local_path)))


class DoomLevelGenerator(object):
    def __init__(self, seed=None):
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randint(0, 2147483647)
        self.config = {}
        for (k, v) in oblige_options.items():
            self.config[k] = v[0]

    def set_seed(self, seed):
        self.seed = seed

    def get_seed(self):
        return self.seed

    def set_config(self, new_config):
        for (k, v) in new_config.items():

            # Check if provided config is correct
            if k not in oblige_options:
                raise ValueError("Provided key {} is not valid Oblige option!".format(k))

            if v not in oblige_options[k]:
                raise ValueError("Provided value {} is not valid value of {}!\nAvailable values: "
                                 .format(v, k, oblige_unique_vals(oblige_options[k])))

            self.config[k] = v

    def generate(self, wad_path, verbose=False):
        wad_path = 'O:\\Doom\\viz_2018\\maps\\tmp\\' + wad_path
        # Config preprocessing
        if self.config["engine"] == "vizdoom":
            self.config["engine"] = "zdoom"

        if verbose:
            print("Config:")
            for (k, v) in self.config.items():
                if v != oblige_options[k][0]:
                    print("  {}: {}".format(k, v))

        # Prepare paths
        if os.path.isdir(wad_path):
            raise ValueError("{} is a directory!".format(wad_path))

        if os.path.splitext(wad_path)[1] != ".wad":
            wad_path += ".wad"

        wad_path = os.path.realpath(wad_path)
        config_path = os.path.realpath(os.path.splitext(wad_path)[0] + ".txt")
        '''
        with open(config_path, "w") as config_file:
            config_file.write(oblige_config_str.format(seed=self.seed, **self.config))

        if sys.platform in ["win32", "win64"]:
            oblige_exe = "Oblige.exe"
            oblige_path = "C:\\Users\\guotata\\Anaconda3\\envs\\py3\\Lib\\site-packages\\oblige\\Oblige-7.70\\" + oblige_exe
        else:
            oblige_exe = "./Oblige"
            oblige_path = "Oblige_src/Oblige"

        oblige_dir = "Oblige_src"

        if verbose:
            print("Config text file path: {}"
                  "\nOutput wad file path: {}"
                  "\nOblige executable path: {}".format(config_path, wad_path, oblige_path))
        
        cmd = "{} --batch {} --load {} --keep".format(oblige_path, wad_path, config_path)
        # if verbose:
        #    cmd += " --verbose"
        #print(cmd)
        # Launch Oblige
        try:
            oblige_process = subprocess.Popen(cmd)
            results = oblige_process.communicate()[0]
            exit_code = oblige_process.returncode

        except subprocess.CalledProcessError:
            raise Exception("Oblige failed to generate .wad file!\nExit code: {}\nLog:\n{}"
                            .format(exit_code, results))

        if verbose:
            print("Exit code: {}\n"
                  "Oblige output:\n{}".format(exit_code, results))

        # Parse results
        maps = 1
        map_str = "MAP{:02}".format(maps)
        while str(results).find(map_str) != -1:
            maps += 1
            map_str = "MAP{:02}".format(maps)
        '''
        wad_path_0 = os.path.splitext(wad_path)[0]
        cmd = "O:\\Doom\\mapinfo\\zwadconv.exe {} {}".format(wad_path, 'O:\\Doom\\mapinfo\\tmp\\z.wad')
        #print(cmd)
        try:
            zwadconv_process = subprocess.Popen(cmd)
            results = zwadconv_process.communicate()[0]
            exit_code = zwadconv_process.returncode
        except subprocess.CalledProcessError:
            raise Exception("zwadconv failed to convert .wad file!\nExit code: {}\nLog:\n{}"
                            .format(exit_code, results))
        
        cmd = "O:\\Doom\\mapinfo\\wad2udmf.exe -i O:\\Doom\\mapinfo\\tmp\\z.wad -o O:\\Doom\\mapinfo\\tmp\\u.wad"
        #print(cmd)
        try:
            udmfconv_process = subprocess.Popen(cmd)
            results = udmfconv_process.communicate()[0]
            exit_code = udmfconv_process.returncode
        except subprocess.CalledProcessError:
            raise Exception("wad2udmf failed to convert .wad file!\nExit code: {}\nLog:\n{}"
                            .format(exit_code, results))
        
        cmd = "O:\\Doom\\mapinfo\\WADex.exe E O:\\Doom\\mapinfo\\tmp\\u.wad O:\\Doom\\mapinfo\\tmp"
        try:
            xtract_process = subprocess.Popen(cmd)
            results = xtract_process.communicate()[0]
            exit_code = xtract_process.returncode
        except subprocess.CalledProcessError:
            raise Exception("failed to extract .wad file!\nExit code: {}\nLog:\n{}"
                            .format(exit_code, results))
        
        linedmap = open('O:\\Doom\\mapinfo\\tmp\\TEXTMAP','r+')
        addon_things = []

        interest_vertex = set()
        interest_side = set()
        interest_sector = set()

        class addon_thing:
            def __init__(self):
                self.v1 = None
                self.v2 = None
                self.sf = None #or: sidefront
                self.sb = None #or: sideback
                self.tid = None

        while True:
            aline = linedmap.readline()
            if not aline:
                break
            if aline.startswith('linedef'):
                playeruse = False
                playercross = False
                special = -1
                v1 = v2 = -1
                sf = sb = -1
                keytype = -1
                while True:
                    line = linedmap.readline()
                    if line.startswith('}'):
                        if special == 13 or special == 11 or special == 12 or special == 21 or special == 70 or special == 243:
                            assert (v1 >= 0 and v2 >= 0)
                            new_thing = addon_thing()
                            new_thing.v1 = v1
                            new_thing.v2 = v2
                            new_thing.sf = sf
                            new_thing.sb = sb
                            interest_vertex.add(v1)
                            interest_vertex.add(v2)
                            if sf > -1:
                                interest_side.add(sf)
                            if sb > -1:
                                interest_side.add(sb)

                            if special == 13:#key_door raise
                                assert (keytype != -1)
                                new_thing.tid = keytype - 129
                            elif special == 11 or special == 12 or special == 21:
                                new_thing.tid = 6 #door open/remote control
                            elif special == 70:
                                new_thing.tid = 7 #teleporter
                            elif special == 243:
                                new_thing.tid = 8 #exit

                            addon_things.append(new_thing)
                        break
                    if line.startswith('v1'):
                        line = line.replace(' ','')
                        line = line.replace(';','')
                        digit = line.split('=')[-1]
                        v1 = int(digit)
                    if line.startswith('v2'):
                        line = line.replace(' ','')
                        line = line.replace(';','')
                        digit = line.split('=')[-1]
                        v2 = int(digit)
                    if line.startswith('playercross'):
                        playercross = True
                    if line.startswith('playeruse'):
                        playeruse = True
                    if line.startswith('special'):
                        line = line.replace(' ','')
                        line = line.replace(';','')
                        digit = line.split('=')[-1]
                        special = int(digit)
                    if line.startswith('sidefront'):
                        line = line.replace(' ','')
                        line = line.replace(';','')
                        digit = line.split('=')[-1]
                        sf = int(digit)
                    if line.startswith('sideback'):
                        line = line.replace(' ','')
                        line = line.replace(';','')
                        digit = line.split('=')[-1]
                        sb = int(digit)
                    if line.startswith('arg3'):
                        line = line.replace(' ','')
                        line = line.replace(';','')
                        digit = line.split('=')[-1]
                        keytype = int(digit)

            elif aline.startswith('sidedef'):
                side_num = aline.split(' ')[-2]
                idx = int(side_num)
                if idx in interest_side:
                    sec = None
                    while True:
                        line = linedmap.readline()
                        if line.startswith('sector'):
                            line = line.replace(' ','')
                            line = line.replace(';','')
                            digit = int(line.split('=')[-1])
                            interest_sector.add(digit)
                            for thing in addon_things:
                                if thing.sf == idx:
                                    thing.sf = digit
                                if thing.sb == idx:
                                    thing.sb = digit
                            break
                            

            elif aline.startswith('vertex'):
                vertex_num = aline.split(' ')[-2]
                idx = int(vertex_num)

                if idx in interest_vertex:
                    x = y = None
                    while True:
                        line = linedmap.readline()
                        if line.startswith('x'):
                            line = line.replace(' ','')
                            line = line.replace(';','')
                            digit = line.split('=')[-1]
                            x = int(float(digit))
                        if line.startswith('y'):
                            line = line.replace(' ','')
                            line = line.replace(';','')
                            digit = line.split('=')[-1]
                            y = int(float(digit))
                        if line.startswith('}'):
                            assert (x is not None)
                            assert (y is not None)
                            for thing in addon_things:
                                if thing.v1 == idx:
                                    thing.v1 = (x, y)
                                if thing.v2 == idx:
                                    thing.v2 = (x, y)
                            break

            elif aline.startswith('sector //'):
                sector_num = aline.split(' ')[-2]
                idx = int(sector_num)

                if idx in interest_sector:
                    floor = ceiling = None
                    while True:
                        line = linedmap.readline()
                        if line.startswith('heightfloor'):
                            line = line.replace(' ', '')
                            line = line.replace(';', '')
                            digit = line.split('=')[-1]
                            floor = int(digit)
                        if line.startswith('heightceiling'):
                            line = line.replace(' ','')
                            line = line.replace(';','')
                            digit = line.split('=')[-1]
                            ceiling = int(digit)
                        if line.startswith('}'):
                            assert (floor is not None)
                            assert (ceiling is not None)
                            for thing in addon_things:
                                if thing.sf == idx:
                                    thing.sf = (floor, ceiling)
                                if thing.sb == idx:
                                    thing.sb = (floor, ceiling)
                            break
                
        #modify height
        for thing in addon_things:
            if thing.sf == -1:
                #single-sided
                assert (len(thing.sb) == 2)
                thing.sf = thing.sb
            elif thing.sb == -1:
                assert (len(thing.sf) == 2)
            elif thing.sf[1] == thing.sb[1]:
                #share the ceiling-- abandon
                tmp_lo = min(thing.sf[0], thing.sb[0])
                tmp_hi = max(thing.sf[0], thing.sb[0])
                assert (tmp_lo != tmp_hi)
                thing.sf = (tmp_lo, tmp_hi)
            else:
                tmp_hi = max(thing.sf[1], thing.sb[1])
                tmp_lo = min(thing.sf[0], thing.sb[0])
                thing.sf = (tmp_lo, tmp_hi)


        linedmap.seek(0, 2)
        mapinfo = open(wad_path_0+"_m.txt", 'w')
                
        for ind in range(len(addon_things)):
            athing = addon_things[ind]
            x1, y1 = athing.v1
            x2, y2 = athing.v2
            flr, cei = athing.sf
            tid = ind + 601
            length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            r_x = (x2 - x1) / length
            r_y = (y2 - y1) / length
            n_x = r_y
            n_y = -r_x

            dest_x = (x1 + x2) / 2 + n_x * 32
            dest_y = (y1 + y2) / 2 + n_y * 32
            dest_x = int(round(dest_x/32.0)) * 32
            dest_y = int(round(dest_y/32.0)) * 32

            thing_str = '''
thing
{{
x={}.000;
y={}.000;
type=9040;
angle=0;
skill1=true;
skill2=true;
skill3=true;
skill4=true;
skill5=true;
single=true;
coop=true;
dm=true;
id = {};
}}\n'''.format(dest_x, dest_y, tid)

            linedmap.writelines(thing_str)
            if athing.tid < 3:
                #modify door pos
                if x1 == x2:
                    if y1 < y2:
                        y1 -= 11
                        y2 += 11
                    else:
                        y1 += 11
                        y2 -= 11
                else:
                    if x1 < x2:
                        x1 -= 11
                        x2 += 11
                    else:
                        x1 += 11
                        x2 -= 11
            mapinfo.write('{} {} {} {} {} {} {} {}\n'.format(tid, athing.tid, x1, y1, x2, y2, flr, cei))

        linedmap.close()
        mapinfo.close()
        os.system("copy O:\\Doom\\mapinfo\\BEHAVIOR O:\\Doom\\mapinfo\\tmp\\BEHAVIOR")
        
        cmd = "O:\\Doom\\mapinfo\\WADex.exe A {} {}".format(wad_path_0 + '_m.wad' , 'O:\\Doom\\mapinfo\\tmp')
        try:
            assemble_process = subprocess.Popen(cmd)
            results = assemble_process.communicate()[0]
            exit_code = assemble_process.returncode
        except subprocess.CalledProcessError:
            raise Exception("failed to assemble .wad file!\nExit code: {}\nLog:\n{}"
                            .format(exit_code, results))
        
        def del_file(path):
            ls = os.listdir(path)
            for i in ls:
                c_path = os.path.join(path, i)
                if os.path.isdir(c_path):
                    shutil.rmtree(c_path)
                else:
                    os.remove(c_path)
        del_file('O:\\Doom\\mapinfo\\tmp')
        
        return 0
