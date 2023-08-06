from collections import OrderedDict
import copy
from itertools import zip_longest
import json
import logging
import pickle
import random
import re
import time

from BaseClasses import World, CollectionState, Item, Region, Location, Shop
from Regions import create_regions, mark_light_world_regions
from EntranceShuffle import link_entrances
from Rom import patch_rom, Sprite, LocalRom, JsonRom
from Rules import set_rules
from Dungeons import create_dungeons, fill_dungeons, fill_dungeons_restrictive
from Fill import distribute_items_cutoff, distribute_items_staleness, distribute_items_restrictive, flood_items
from ItemList import generate_itempool, difficulties, fill_prizes
from Utils import output_path

__version__ = '0.6.2'

logic_hash = [134, 166, 181, 191, 228, 89, 188, 200, 5, 157, 217, 139, 180, 198, 106, 104,
              88, 223, 138, 28, 54, 18, 216, 129, 248, 19, 109, 220, 159, 75, 238, 57,
              231, 183, 143, 167, 114, 176, 82, 169, 179, 94, 115, 193, 252, 222, 52, 245,
              33, 208, 39, 122, 177, 136, 29, 161, 210, 165, 6, 125, 146, 212, 101, 185,
              65, 247, 253, 85, 171, 147, 71, 148, 203, 202, 230, 1, 13, 64, 254, 141,
              32, 93, 152, 4, 92, 16, 195, 204, 246, 201, 11, 7, 189, 97, 9, 91,
              237, 215, 163, 131, 142, 34, 111, 196, 120, 127, 168, 211, 227, 61, 187, 110,
              190, 162, 59, 80, 225, 186, 37, 154, 76, 72, 27, 17, 79, 206, 207, 243,
              184, 197, 153, 48, 119, 99, 2, 151, 51, 67, 121, 175, 38, 224, 87, 242,
              45, 22, 155, 244, 209, 117, 214, 213, 194, 126, 236, 73, 133, 70, 49, 140,
              229, 108, 156, 124, 105, 226, 44, 23, 112, 102, 173, 219, 14, 116, 58, 103,
              55, 10, 95, 251, 84, 118, 160, 78, 63, 250, 31, 41, 35, 255, 170, 25,
              66, 172, 98, 249, 68, 8, 113, 21, 46, 24, 137, 149, 81, 130, 42, 164,
              50, 12, 158, 15, 47, 182, 30, 40, 36, 83, 77, 205, 20, 241, 3, 132,
              0, 60, 96, 62, 74, 178, 53, 56, 135, 174, 145, 86, 107, 233, 218, 221,
              43, 150, 100, 69, 235, 26, 234, 192, 199, 144, 232, 128, 239, 123, 240, 90]


def main(args, seed=None):
    start = time.clock()

    # initialize the world
    world = World(args.multi, args.shuffle, args.logic, args.mode, args.difficulty, args.timer, args.progressive, args.goal, args.algorithm, not args.nodungeonitems, args.beatableonly, args.shuffleganon, args.quickswap, args.fastmenu, args.disablemusic, args.keysanity, args.retro, args.custom, args.customitemarray, args.shufflebosses, args.hints)
    logger = logging.getLogger('')
    if seed is None:
        random.seed(None)
        world.seed = random.randint(0, 999999999)
    else:
        world.seed = int(seed)
    random.seed(world.seed)

    world.rom_seeds = {player: random.randint(0, 999999999) for player in range(1, world.players + 1)}

    logger.info('ALttP Entrance Randomizer Version %s  -  Seed: %s\n\n', __version__, world.seed)

    world.difficulty_requirements = difficulties[world.difficulty]

    for player in range(1, world.players + 1):
        create_regions(world, player)
        create_dungeons(world, player)

    logger.info('Shuffling the World about.')

    for player in range(1, world.players + 1):
        link_entrances(world, player)

    mark_light_world_regions(world)

    logger.info('Generating Item Pool.')

    for player in range(1, world.players + 1):
        generate_itempool(world, player)

    logger.info('Calculating Access Rules.')

    for player in range(1, world.players + 1):
        set_rules(world, player)

    logger.info('Placing Dungeon Prizes.')

    fill_prizes(world)

    logger.info('Placing Dungeon Items.')

    shuffled_locations = None
    if args.algorithm in ['balanced', 'vt26'] or args.keysanity:
        shuffled_locations = world.get_unfilled_locations()
        random.shuffle(shuffled_locations)
        fill_dungeons_restrictive(world, shuffled_locations)
    else:
        fill_dungeons(world)

    logger.info('Fill the world.')

    if args.algorithm == 'flood':
        flood_items(world)  # different algo, biased towards early game progress items
    elif args.algorithm == 'vt21':
        distribute_items_cutoff(world, 1)
    elif args.algorithm == 'vt22':
        distribute_items_cutoff(world, 0.66)
    elif args.algorithm == 'freshness':
        distribute_items_staleness(world)
    elif args.algorithm == 'vt25':
        distribute_items_restrictive(world, 0)
    elif args.algorithm == 'vt26':

        distribute_items_restrictive(world, gt_filler(world), shuffled_locations)
    elif args.algorithm == 'balanced':
        distribute_items_restrictive(world, gt_filler(world))

    logger.info('Patching ROM.')

    if args.sprite is not None:
        if isinstance(args.sprite, Sprite):
            sprite = args.sprite
        else:
            sprite = Sprite(args.sprite)
    else:
        sprite = None

    player_names = {player: name for player, name in enumerate([n for n in re.split(r'[, ]', args.names) if n], 1)}
    outfilebase = 'ER_%s_%s-%s-%s%s_%s-%s%s%s%s%s_%s' % (world.logic, world.difficulty, world.mode, world.goal, "" if world.timer in ['none', 'display'] else "-" + world.timer, world.shuffle, world.algorithm, "-keysanity" if world.keysanity else "", "-retro" if world.retro else "", "-prog_" + world.progressive if world.progressive in ['off', 'random'] else "", "-nohints" if not world.hints else "", world.seed)

    jsonout = {}
    if not args.suppress_rom:
        from MultiServer import MultiWorld
        multidata = MultiWorld()
        multidata.players = world.players

        for player in range(1, world.players + 1):
            if args.jsonout:
                rom = JsonRom()
            else:
                rom = LocalRom(args.rom)
            patch_rom(world, player, rom, bytearray(logic_hash), args.heartbeep, args.heartcolor, sprite, player_names)

            multidata.rom_names[player] = list(rom.name)
            for location in world.get_filled_locations(player):
                if type(location.address) is int:
                    multidata.locations[(location.address, player)] = (location.item.code, location.item.player)

            if args.jsonout:
                jsonout['patch%d' % player] = rom.patches
            else:
                rom.write_to_file(output_path('%s_P%d%s.sfc' % (outfilebase, player, ('_' + player_names[player]) if player in player_names else '')))

        with open(output_path('%s_multidata' % outfilebase), 'wb') as f:
            pickle.dump(multidata, f, pickle.HIGHEST_PROTOCOL)

    if args.create_spoiler and not args.jsonout:
        world.spoiler.to_file(output_path('%s_Spoiler.txt' % outfilebase))

    if not args.skip_playthrough:
        logger.info('Calculating playthrough.')
        create_playthrough(world)

    if args.jsonout:
        print(json.dumps({**jsonout, 'spoiler': world.spoiler.to_json()}))
    elif args.create_spoiler and not args.skip_playthrough:
        world.spoiler.to_file(output_path('%s_Spoiler.txt' % outfilebase))

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.clock() - start)

    return world

def gt_filler(world):
    if world.goal == 'triforcehunt':
        return random.randint(15, 50)
    return random.randint(0, 15)

def copy_world(world):
    # ToDo: Not good yet
    ret = World(world.players, world.shuffle, world.logic, world.mode, world.difficulty, world.timer, world.progressive, world.goal, world.algorithm, world.place_dungeon_items, world.check_beatable_only, world.shuffle_ganon, world.quickswap, world.fastmenu, world.disable_music, world.keysanity, world.retro, world.custom, world.customitemarray, world.boss_shuffle, world.hints)
    ret.required_medallions = world.required_medallions.copy()
    ret.swamp_patch_required = world.swamp_patch_required.copy()
    ret.ganon_at_pyramid = world.ganon_at_pyramid.copy()
    ret.powder_patch_required = world.powder_patch_required.copy()
    ret.ganonstower_vanilla = world.ganonstower_vanilla.copy()
    ret.treasure_hunt_count = world.treasure_hunt_count
    ret.treasure_hunt_icon = world.treasure_hunt_icon
    ret.sewer_light_cone = world.sewer_light_cone
    ret.light_world_light_cone = world.light_world_light_cone
    ret.dark_world_light_cone = world.dark_world_light_cone
    ret.seed = world.seed
    ret.can_access_trock_eyebridge = world.can_access_trock_eyebridge
    ret.can_access_trock_front = world.can_access_trock_front
    ret.can_access_trock_big_chest = world.can_access_trock_big_chest
    ret.can_access_trock_middle = world.can_access_trock_middle
    ret.can_take_damage = world.can_take_damage
    ret.difficulty_requirements = world.difficulty_requirements
    ret.fix_fake_world = world.fix_fake_world
    ret.lamps_needed_for_dark_rooms = world.lamps_needed_for_dark_rooms

    for player in range(1, world.players + 1):
        create_regions(ret, player)
        create_dungeons(ret, player)

    copy_dynamic_regions_and_locations(world, ret)

    # copy bosses
    for dungeon in world.dungeons:
        for level, boss in dungeon.bosses.items():
            ret.get_dungeon(dungeon.name, dungeon.player).bosses[level] = boss

    for shop in world.shops:
        copied_shop = ret.get_region(shop.region.name, shop.region.player).shop
        copied_shop.active = shop.active
        copied_shop.inventory = copy.copy(shop.inventory)

    # connect copied world
    for region in world.regions:
        copied_region = ret.get_region(region.name, region.player)
        copied_region.is_light_world = region.is_light_world
        copied_region.is_dark_world = region.is_dark_world
        for entrance in region.entrances:
            ret.get_entrance(entrance.name, entrance.player).connect(copied_region)

    # fill locations
    for location in world.get_locations():
        if location.item is not None:
            item = Item(location.item.name, location.item.advancement, location.item.priority, location.item.type, player = location.item.player)
            ret.get_location(location.name, location.player).item = item
            item.location = ret.get_location(location.name, location.player)
        if location.event:
            ret.get_location(location.name, location.player).event = True

    # copy remaining itempool. No item in itempool should have an assigned location
    for item in world.itempool:
        ret.itempool.append(Item(item.name, item.advancement, item.priority, item.type, player = item.player))

    # copy progress items in state
    ret.state.prog_items = list(world.state.prog_items)

    for player in range(1, world.players + 1):
        set_rules(ret, player)

    return ret

def copy_dynamic_regions_and_locations(world, ret):
    for region in world.dynamic_regions:
        new_reg = Region(region.name, region.type, region.hint_text, region.player)
        ret.regions.append(new_reg)
        ret.dynamic_regions.append(new_reg)

        # Note: ideally exits should be copied here, but the current use case (Take anys) do not require this

        if region.shop:
            new_reg.shop = Shop(new_reg, region.shop.room_id, region.shop.type, region.shop.shopkeeper_config, region.shop.replaceable)
            ret.shops.append(new_reg.shop)

    for location in world.dynamic_locations:
        new_loc = Location(location.player, location.name, location.address, location.crystal, location.hint_text, location.parent_region, location.player_address)
        new_reg = ret.get_region(location.parent_region.name, location.parent_region.player)
        new_reg.locations.append(new_loc)


def create_playthrough(world):
    # create a copy as we will modify it
    old_world = world
    world = copy_world(world)

    # in treasure hunt and pedestal goals, ganon is invincible
    if world.goal in ['pedestal', 'triforcehunt']:
        for player in range(1, world.players + 1):
            world.get_location('Ganon', player).item = None

    # if we only check for beatable, we can do this sanity check first before writing down spheres
    if world.check_beatable_only and not world.can_beat_game():
        raise RuntimeError('Cannot beat game. Something went terribly wrong here!')

    # get locations containing progress items
    prog_locations = [location for location in world.get_filled_locations() if location.item.advancement]
    state_cache = [None]
    collection_spheres = []
    state = CollectionState(world)
    sphere_candidates = list(prog_locations)
    logging.getLogger('').debug('Building up collection spheres.')
    while sphere_candidates:
        if not world.keysanity:
            state.sweep_for_events(key_only=True)

        sphere = []
        # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres
        for location in sphere_candidates:
            if state.can_reach(location):
                sphere.append(location)

        for location in sphere:
            sphere_candidates.remove(location)
            state.collect(location.item, True, location)

        collection_spheres.append(sphere)

        state_cache.append(state.copy())

        logging.getLogger('').debug('Calculated sphere %i, containing %i of %i progress items.', len(collection_spheres), len(sphere), len(prog_locations))
        if not sphere:
            logging.getLogger('').debug('The following items could not be reached: %s', ['%s (Player %d) at %s (Player %d)' % (location.item.name, location.item.player, location.name, location.player) for location in sphere_candidates])
            if not world.check_beatable_only:
                raise RuntimeError('Not all progression items reachable. Something went terribly wrong here.')
            else:
                break

    # in the second phase, we cull each sphere such that the game is still beatable, reducing each range of influence to the bare minimum required inside it
    for num, sphere in reversed(list(enumerate(collection_spheres))):
        to_delete = []
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            logging.getLogger('').debug('Checking if %s (Player %d) is required to beat the game.', location.item.name, location.item.player)
            old_item = location.item
            location.item = None
            state.remove(old_item)
            ##if world.can_beat_game(state_cache[num]):
            if world.can_beat_game():
                to_delete.append(location)
            else:
                # still required, got to keep it around
                location.item = old_item

        # cull entries in spheres for spoiler walkthrough at end
        for location in to_delete:
            sphere.remove(location)

    # we are now down to just the required progress items in collection_spheres. Unfortunately
    # the previous pruning stage could potentially have made certain items dependant on others
    # in the same or later sphere (because the location had 2 ways to access but the item originally
    # used to access it was deemed not required.) So we need to do one final sphere collection pass
    # to build up the correct spheres

    required_locations = [item for sphere in collection_spheres for item in sphere]
    state = CollectionState(world)
    collection_spheres = []
    while required_locations:
        if not world.keysanity:
            state.sweep_for_events(key_only=True)

        sphere = list(filter(state.can_reach, required_locations))

        for location in sphere:
            required_locations.remove(location)
            state.collect(location.item, True, location)

        collection_spheres.append(sphere)

        logging.getLogger('').debug('Calculated final sphere %i, containing %i of %i progress items.', len(collection_spheres), len(sphere), len(required_locations))
        if not sphere:
            raise RuntimeError('Not all required items reachable. Something went terribly wrong here.')

    # store the required locations for statistical analysis
    old_world.required_locations = [(location.name, location.player) for sphere in collection_spheres for location in sphere]

    def flist_to_iter(node):
        while node:
            value, node = node
            yield value

    def get_path(state, region):
        reversed_path_as_flist = state.path.get(region, (region, None))
        string_path_flat = reversed(list(map(str, flist_to_iter(reversed_path_as_flist))))
        # Now we combine the flat string list into (region, exit) pairs
        pathsiter = iter(string_path_flat)
        pathpairs = zip_longest(pathsiter, pathsiter)
        return list(pathpairs)

    old_world.spoiler.paths = {(location.name, location.player) : get_path(state, location.parent_region) for sphere in collection_spheres for location in sphere}
    for (_, player), path in dict(old_world.spoiler.paths).items():
        if any(exit == 'Pyramid Fairy' for (_, exit) in path):
            old_world.spoiler.paths[('Big Bomb Shop', player)] = get_path(state, world.get_region('Big Bomb Shop', player))

    # we can finally output our playthrough
    old_world.spoiler.playthrough = OrderedDict([(str(i + 1), {str(location): str(location.item) for location in sphere}) for i, sphere in enumerate(collection_spheres)])
