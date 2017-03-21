from bantam import *

open_game_window('Spaaaaaace')

set_background_color('black')

pos_x = 400
pos_y = 300
ship_image = image_from_file('./ship2.gif')

while True:
  bantam_next_frame()

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