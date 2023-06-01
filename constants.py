SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600

DESIRED_TILE_SIZE = 51

DEF_COLLECTIBLE_COLOR = "purple"
COLLECTIBLE_LIFETIME = 50

def adjust_tile_size(desired_size):
    """
    Tile size is to fit evenly to the screen so an 
    attempt is made to adjust it
    """
    tile_adjusted = False
    while tile_adjusted is False:

        if desired_size > SCREEN_WIDTH / 10:
            raise ValueError("Couldn't make fit the chosen tile size to selected resolution")

        if SCREEN_HEIGHT % desired_size == 0 and SCREEN_WIDTH % desired_size == 0:
            tile_adjusted = True
        else:
            desired_size += 1
    return desired_size

# This is the actual TILE_SIZE used in the game
TILE_SIZE = adjust_tile_size(DESIRED_TILE_SIZE)


