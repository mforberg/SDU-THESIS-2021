from minecraft_pb2 import *

# Box area (they are made to be inclusive)
BOX_X_MIN = -103
BOX_X_MAX = -3
BOX_Z_MIN = 315
BOX_Z_MAX = 415

# Map analysis
MIN_SIZE_OF_AREA = 50


# List of blocks that is ignored
SKIP_LIST = [DARK_OAK_DOOR, IRON_DOOR, BIRCH_DOOR, JUNGLE_DOOR, ACACIA_DOOR, SPRUCE_DOOR, WOODEN_DOOR, IRON_TRAPDOOR,
             TRAPDOOR, FENCE, BIRCH_FENCE, ACACIA_FENCE, JUNGLE_FENCE, DARK_OAK_FENCE, NETHER_BRICK_FENCE,
             SPRUCE_FENCE, FENCE_GATE, BIRCH_FENCE_GATE, ACACIA_FENCE_GATE, JUNGLE_FENCE_GATE, DARK_OAK_FENCE_GATE,
             SPRUCE_FENCE_GATE, CARPET, COBBLESTONE_WALL, NETHER_WART, STANDING_BANNER, WALL_BANNER, STANDING_SIGN,
             WALL_SIGN, WOODEN_BUTTON, STONE_BUTTON, TRIPWIRE, AIR, BEETROOTS, TALLGRASS, RED_FLOWER, YELLOW_FLOWER,
             CHORUS_FLOWER, LEAVES, LEAVES2, VINE, SAPLING, WATERLILY, RED_MUSHROOM, BROWN_MUSHROOM, REEDS, POTATOES,
             MELON_BLOCK, MELON_STEM, PUMPKIN_STEM, PUMPKIN, DEADBUSH, SNOW_LAYER, WHEAT, RAIL, CHORUS_PLANT,
             DOUBLE_PLANT, FIRE, COCOA, CARROTS, CACTUS, TORCH]

FLUID_LIST = [WATER, FLOWING_WATER, LAVA, FLOWING_LAVA]
