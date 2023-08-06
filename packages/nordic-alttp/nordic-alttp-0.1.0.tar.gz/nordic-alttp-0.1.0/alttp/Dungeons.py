import random

from BaseClasses import Dungeon
from Bosses import BossFactory
from Fill import fill_restrictive
from Items import ItemFactory


def create_dungeons(world, player):
    def make_dungeon(name, default_boss, dungeon_regions, big_key, small_keys, dungeon_items):
        dungeon = Dungeon(name, dungeon_regions, big_key, [] if world.retro else small_keys, dungeon_items, player)
        dungeon.boss = BossFactory(default_boss, player)
        for region in dungeon.regions:
            world.get_region(region, player).dungeon = dungeon
        return dungeon

    ES = make_dungeon('Hyrule Castle', None, ['Hyrule Castle', 'Sewers', 'Sewer Drop', 'Sewers (Dark)', 'Sanctuary'], None, [ItemFactory('Small Key (Escape)', player)], [ItemFactory('Map (Escape)', player)])
    EP = make_dungeon('Eastern Palace', 'Armos Knights', ['Eastern Palace'], ItemFactory('Big Key (Eastern Palace)', player), [], ItemFactory(['Map (Eastern Palace)', 'Compass (Eastern Palace)'], player))
    DP = make_dungeon('Desert Palace', 'Lanmolas', ['Desert Palace North', 'Desert Palace Main (Inner)', 'Desert Palace Main (Outer)', 'Desert Palace East'], ItemFactory('Big Key (Desert Palace)', player), [ItemFactory('Small Key (Desert Palace)', player)], ItemFactory(['Map (Desert Palace)', 'Compass (Desert Palace)'], player))
    ToH = make_dungeon('Tower of Hera', 'Moldorm', ['Tower of Hera (Bottom)', 'Tower of Hera (Basement)', 'Tower of Hera (Top)'], ItemFactory('Big Key (Tower of Hera)', player), [ItemFactory('Small Key (Tower of Hera)', player)], ItemFactory(['Map (Tower of Hera)', 'Compass (Tower of Hera)'], player))
    AT = make_dungeon('Agahnims Tower', 'Agahnim', ['Agahnims Tower', 'Agahnim 1'], None, ItemFactory(['Small Key (Agahnims Tower)'] * 2, player), [])
    PoD = make_dungeon('Palace of Darkness', 'Helmasaur King', ['Palace of Darkness (Entrance)', 'Palace of Darkness (Center)', 'Palace of Darkness (Big Key Chest)', 'Palace of Darkness (Bonk Section)', 'Palace of Darkness (North)', 'Palace of Darkness (Maze)', 'Palace of Darkness (Harmless Hellway)', 'Palace of Darkness (Final Section)'], ItemFactory('Big Key (Palace of Darkness)', player), ItemFactory(['Small Key (Palace of Darkness)'] * 6, player), ItemFactory(['Map (Palace of Darkness)', 'Compass (Palace of Darkness)'], player))
    TT = make_dungeon('Thieves Town', 'Blind', ['Thieves Town (Entrance)', 'Thieves Town (Deep)', 'Blind Fight'], ItemFactory('Big Key (Thieves Town)', player), [ItemFactory('Small Key (Thieves Town)', player)], ItemFactory(['Map (Thieves Town)', 'Compass (Thieves Town)'], player))
    SW = make_dungeon('Skull Woods', 'Mothula', ['Skull Woods Final Section (Entrance)', 'Skull Woods First Section', 'Skull Woods Second Section', 'Skull Woods Second Section (Drop)', 'Skull Woods Final Section (Mothula)', 'Skull Woods First Section (Right)', 'Skull Woods First Section (Left)', 'Skull Woods First Section (Top)'], ItemFactory('Big Key (Skull Woods)', player), ItemFactory(['Small Key (Skull Woods)'] * 2, player), ItemFactory(['Map (Skull Woods)', 'Compass (Skull Woods)'], player))
    SP = make_dungeon('Swamp Palace', 'Arrghus', ['Swamp Palace (Entrance)', 'Swamp Palace (First Room)', 'Swamp Palace (Starting Area)', 'Swamp Palace (Center)', 'Swamp Palace (North)'], ItemFactory('Big Key (Swamp Palace)', player), [ItemFactory('Small Key (Swamp Palace)', player)], ItemFactory(['Map (Swamp Palace)', 'Compass (Swamp Palace)'], player))
    IP = make_dungeon('Ice Palace', 'Kholdstare', ['Ice Palace (Entrance)', 'Ice Palace (Main)', 'Ice Palace (East)', 'Ice Palace (East Top)', 'Ice Palace (Kholdstare)'], ItemFactory('Big Key (Ice Palace)', player), ItemFactory(['Small Key (Ice Palace)'] * 2, player), ItemFactory(['Map (Ice Palace)', 'Compass (Ice Palace)'], player))
    MM = make_dungeon('Misery Mire', 'Vitreous', ['Misery Mire (Entrance)', 'Misery Mire (Main)', 'Misery Mire (West)', 'Misery Mire (Final Area)', 'Misery Mire (Vitreous)'], ItemFactory('Big Key (Misery Mire)', player), ItemFactory(['Small Key (Misery Mire)'] * 3, player), ItemFactory(['Map (Misery Mire)', 'Compass (Misery Mire)'], player))
    TR = make_dungeon('Turtle Rock', 'Trinexx', ['Turtle Rock (Entrance)', 'Turtle Rock (First Section)', 'Turtle Rock (Chain Chomp Room)', 'Turtle Rock (Second Section)', 'Turtle Rock (Big Chest)', 'Turtle Rock (Crystaroller Room)', 'Turtle Rock (Dark Room)', 'Turtle Rock (Eye Bridge)', 'Turtle Rock (Trinexx)'], ItemFactory('Big Key (Turtle Rock)', player), ItemFactory(['Small Key (Turtle Rock)'] * 4, player), ItemFactory(['Map (Turtle Rock)', 'Compass (Turtle Rock)'], player))
    GT = make_dungeon('Ganons Tower', 'Agahnim2', ['Ganons Tower (Entrance)', 'Ganons Tower (Tile Room)', 'Ganons Tower (Compass Room)', 'Ganons Tower (Hookshot Room)', 'Ganons Tower (Map Room)', 'Ganons Tower (Firesnake Room)', 'Ganons Tower (Teleport Room)', 'Ganons Tower (Bottom)', 'Ganons Tower (Top)', 'Ganons Tower (Before Moldorm)', 'Ganons Tower (Moldorm)', 'Agahnim 2'], ItemFactory('Big Key (Ganons Tower)', player), ItemFactory(['Small Key (Ganons Tower)'] * 4, player), ItemFactory(['Map (Ganons Tower)', 'Compass (Ganons Tower)'], player))

    GT.bosses['bottom'] = BossFactory('Armos Knights', player)
    GT.bosses['middle'] = BossFactory('Lanmolas', player)
    GT.bosses['top'] = BossFactory('Moldorm', player)

    world.dungeons += [ES, EP, DP, ToH, AT, PoD, TT, SW, SP, IP, MM, TR, GT]

def fill_dungeons(world):
    freebes = ['Ganons Tower - Map Chest', 'Palace of Darkness - Harmless Hellway', 'Palace of Darkness - Big Key Chest', 'Turtle Rock - Big Key Chest']

    all_state_base = world.get_all_state()

    for player in range(1, world.players + 1):
        if world.retro:
            world.push_item(world.get_location('Skull Woods - Pinball Room', player), ItemFactory('Small Key (Universal)', player), False)
        else:
            world.push_item(world.get_location('Skull Woods - Pinball Room', player), ItemFactory('Small Key (Skull Woods)', player), False)
        world.get_location('Skull Woods - Pinball Room', player).event = True

    dungeons = [(list(dungeon.regions), dungeon.big_key, list(dungeon.small_keys), list(dungeon.dungeon_items)) for dungeon in world.dungeons]

    loopcnt = 0
    while dungeons:
        loopcnt += 1
        dungeon_regions, big_key, small_keys, dungeon_items = dungeons.pop(0)
        # this is what we need to fill
        dungeon_locations = [location for location in world.get_unfilled_locations() if location.parent_region.name in dungeon_regions]
        random.shuffle(dungeon_locations)

        all_state = all_state_base.copy()

        # first place big key
        if big_key is not None:
            bk_location = None
            for location in dungeon_locations:
                if location.item_rule(big_key):
                    bk_location = location
                    break

            if bk_location is None:
                raise RuntimeError('No suitable location for %s' % big_key)

            world.push_item(bk_location, big_key, False)
            bk_location.event = True
            dungeon_locations.remove(bk_location)
            all_state.clear_cached_unreachable()
            big_key = None

        # next place small keys
        while small_keys:
            small_key = small_keys.pop()
            all_state.sweep_for_events()
            sk_location = None
            for location in dungeon_locations:
                if location.name in freebes or (location.can_reach(all_state) and location.item_rule(small_key)):
                    sk_location = location
                    break

            if sk_location is None:
                # need to retry this later
                small_keys.append(small_key)
                dungeons.append((dungeon_regions, big_key, small_keys, dungeon_items))
                # infinite regression protection
                if loopcnt < (30 * world.players):
                    break
                else:
                    raise RuntimeError('No suitable location for %s' % small_key)

            world.push_item(sk_location, small_key, False)
            sk_location.event = True
            dungeon_locations.remove(sk_location)
            all_state.clear_cached_unreachable()

        if small_keys:
            # key placement not finished, loop again
            continue

        # next place dungeon items
        if world.place_dungeon_items:
            for dungeon_item in dungeon_items:
                di_location = dungeon_locations.pop()
                world.push_item(di_location, dungeon_item, False)

    world.state.clear_cached_unreachable()

def get_dungeon_item_pool(world):
    return [item for dungeon in world.dungeons for item in dungeon.all_items if item.key or world.place_dungeon_items]

def fill_dungeons_restrictive(world, shuffled_locations):
    all_state_base = world.get_all_state()

    for player in range(1, world.players + 1):
        skull_woods_big_chest = world.get_location('Skull Woods - Pinball Room', player)
        if world.retro:
            world.push_item(skull_woods_big_chest, ItemFactory('Small Key (Universal)', player), False)
        else:
            world.push_item(skull_woods_big_chest, ItemFactory('Small Key (Skull Woods)', player), False)
        skull_woods_big_chest.event = True
        shuffled_locations.remove(skull_woods_big_chest)

    if world.keysanity:
        #in keysanity dungeon items are distributed as part of the normal item pool
        for item in world.get_items():
            if item.key:
                item.advancement = True
            elif item.map or item.compass:
                item.priority = True
        return

    dungeon_items = get_dungeon_item_pool(world)

    # sort in the order Big Key, Small Key, Other before placing dungeon items
    sort_order = {"BigKey": 3, "SmallKey": 2}
    dungeon_items.sort(key=lambda item: sort_order.get(item.type, 1))

    fill_restrictive(world, all_state_base, shuffled_locations, dungeon_items)

    world.state.clear_cached_unreachable()


dungeon_music_addresses = {'Eastern Palace - Prize': [0x1559A],
                           'Desert Palace - Prize': [0x1559B, 0x1559C, 0x1559D, 0x1559E],
                           'Tower of Hera - Prize': [0x155C5, 0x1107A, 0x10B8C],
                           'Palace of Darkness - Prize': [0x155B8],
                           'Swamp Palace - Prize': [0x155B7],
                           'Thieves\' Town - Prize': [0x155C6],
                           'Skull Woods - Prize': [0x155BA, 0x155BB, 0x155BC, 0x155BD, 0x15608, 0x15609, 0x1560A, 0x1560B],
                           'Ice Palace - Prize': [0x155BF],
                           'Misery Mire - Prize': [0x155B9],
                           'Turtle Rock - Prize': [0x155C7, 0x155A7, 0x155AA, 0x155AB]}
