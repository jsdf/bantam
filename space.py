from bantam import *

open_game_window()

# the stuff which happens once to set up the game
world = bantam_create_world()

world.pos_x = 400
world.pos_y = 300
world.ship2 = image_from_file('./ship2.gif')

# the stuff which is done each frame
def update(world, dt):
  world.pos_x = world.pos_x + dt / 10
  world.pos_y = world.pos_y + dt / 10
  draw_image(world.ship2, world.pos_x, world.pos_y)

bantam_run(world, update)
