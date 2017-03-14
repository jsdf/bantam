from bantam import *

posx = 400
posy = 300

ship2 = image_from_file('./ship2.gif')

while True:
	dt = bantam_update()
	posx = posx + dt*100
	draw_image(ship2, posx, posy)
