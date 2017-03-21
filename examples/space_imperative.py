from bantam import *

open_game_window()

set_background_color('black')

# the stuff which happens once to set up the game
pos_x = 400
pos_y = 300
ship_image = image_from_file('./ship2.gif')

draw_image(ship_image, pos_x, pos_y)

freeze_game_window()

# the stuff which is done each frame
while True:
  bantam_next_frame()

  # how many pixels to move the ship each frame
  amount_to_move = 1

  if is_key_pressed('Left'):
    pos_x = pos_x - amount_to_move

  if is_key_pressed('Right'):
    pos_x = pos_x + amount_to_move

  if is_key_pressed('Up'):
    pos_y = pos_y - amount_to_move

  if is_key_pressed('Down'):
    pos_y = pos_y + amount_to_move

  draw_image(ship_image, pos_x, pos_y)
