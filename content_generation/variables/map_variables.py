from minecraft_pb2 import *
from shared_variables import *

# Box area (they are made to be inclusive)
"""Nicolai's coordinates"""
BOX_X_MIN = 232140
BOX_X_MAX = 232190
BOX_Z_MIN = 23233050
BOX_Z_MAX = 23233100
"""Jonas' coordinates"""
# BOX_X_MIN = 385
# BOX_X_MAX = 585
# BOX_Z_MIN = 1500
# BOX_Z_MAX = 1700
#  Test coordinates
# BOX_X_MIN = 100
# BOX_X_MAX = 300
# BOX_Z_MIN = 1500
# BOX_Z_MAX = 1700
"""Mikkel's coordinates"""
# BOX_X_MIN = -153 #-245
# BOX_X_MAX = 96   #4
# BOX_Z_MIN = 1411 #1483
# BOX_Z_MAX = 1661 #1733


# Map analysis
MIN_SIZE_OF_AREA = 20


# List of blocks that is ignored
SKIP_SET = {DARK_OAK_DOOR, IRON_DOOR, BIRCH_DOOR, JUNGLE_DOOR, ACACIA_DOOR, SPRUCE_DOOR, WOODEN_DOOR, IRON_TRAPDOOR,
            TRAPDOOR, FENCE, BIRCH_FENCE, ACACIA_FENCE, JUNGLE_FENCE, DARK_OAK_FENCE, NETHER_BRICK_FENCE,
            SPRUCE_FENCE, FENCE_GATE, BIRCH_FENCE_GATE, ACACIA_FENCE_GATE, JUNGLE_FENCE_GATE, DARK_OAK_FENCE_GATE,
            SPRUCE_FENCE_GATE, CARPET, COBBLESTONE_WALL, NETHER_WART, STANDING_BANNER, WALL_BANNER, STANDING_SIGN,
            WALL_SIGN, WOODEN_BUTTON, STONE_BUTTON, TRIPWIRE, AIR, BEETROOTS, TALLGRASS, RED_FLOWER, YELLOW_FLOWER,
            CHORUS_FLOWER, LEAVES, LEAVES2, VINE, SAPLING, WATERLILY, RED_MUSHROOM, BROWN_MUSHROOM, REEDS, POTATOES,
            MELON_BLOCK, MELON_STEM, PUMPKIN_STEM, PUMPKIN, DEADBUSH, SNOW_LAYER, WHEAT, RAIL, CHORUS_PLANT,
            DOUBLE_PLANT, FIRE, COCOA, CARROTS, CACTUS, TORCH}


FLUID_SET = {WATER, FLOWING_WATER, LAVA, FLOWING_LAVA, BEDROCK}

save_file_dir = '../data/'
save_file_path = 'block_dicts.pkl'


class MapAnalData:
    def __init__(self, block_dict: dict, surface_dict: dict, areas_for_districts: SolutionGA,
                 set_of_fluid_coordinates: set):
        self.block_dict = block_dict
        self.surface_dict = surface_dict
        self.areas_for_districts = areas_for_districts
        self.set_of_fluid_coordinates = set_of_fluid_coordinates
