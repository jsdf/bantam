### how to make a space shooter game in python

Download the files from https://jamesfriend.com.au/bantam/tutorial_files.zip

Download and install python 2.7 from https://www.python.org/downloads/

Download and install atom from https://atom.io

Unzip tutorial_files.zip

Now we need to run our Python file.
In the unzipped folder, right click `bantam.py` and choose 'open with' and then
select 'python' (on Windows) or 'Python Launcher (2.7.x)' (on Mac).

Alternatively, if you are comfortable running Python from the command line, you
can just run `python bantam.py`.

You should see a window with the title 'Spaaaaaace', which contains nothing but a
black background.

Open Atom, and then in Atom use the file menu to open `game.py` (not `bantam.py`).

This is what you should see:

```python
from bantam import *

open_game_window('Spaaaaaace')

set_background_color('black')

freeze_game_window()
```

Firstly, the line `from bantam import *` is needed to load some other code so
we can use it in out game. You don't really need to think about this, it just
needs to be there at the start of the file.

Next is `open_game_window('Spaaaaaace')`. Pretty self explanatory. Opens the window you saw
which had the title 'Spaaaaaace'.

`set_background_color('black')`, again this should be self explanatory, it sets
the window's contents to be filled with black.

Finally, `freeze_game_window()`: because our game doesn't continue to do stuff
after this point (because we haven't added code to do that yet), this line just
keeps the program from exiting, otherwise the window would disappear. For the
first few steps here we want it to stick around so we can see the results of our
work.


Lets add a ship to the screen. This will represent our player. After
`set_background_color('black')`, but before `freeze_game_window()`, add the
following lines:

```python
ship_image = image_from_file('./ship2.gif')

pos_x = 400
pos_y = 300
draw_image(ship_image, pos_x, pos_y)

```

So now your file should look like this:

```python
from bantam import *

open_game_window('Spaaaaaace')

set_background_color('black')

ship_image = image_from_file('./ship2.gif')

pos_x = 400
pos_y = 300
draw_image(ship_image, pos_x, pos_y)

freeze_game_window()

```

Save the file, then switch back to the game window and press Control-r (the 
'control' key and the 'r' key at the same time). You should see the game window
disappear then reappear, and now there should be a spaceship in the middle of
the screen.

If you made a mistake you should see some text like:

```
Looks like there was an error in your code.
Please fix it, then click this window and press Enter to try loading it again.
```

What does the new code we added mean? Basically, it means we load an image from
a file called `ship2.gif`, and called it `ship_image`, and then we put it
onto the screen at `pos_x` pixels from the left of the screen, and `pos_y`
pixels from the top of the screen.

Okay, so we've got our player's spaceship on the screen, but it's still not much
of a game. Nothing is even moving. Let's see our ship fly.

Remove the line which says `freeze_game_window()`, and also the line which says
`draw_image(ship_image, pos_x, pos_y)`, and replace it with the following:

```python
while True:
  bantam_next_frame()

  pos_y = pos_y - 1

  draw_image(ship_image, pos_x, pos_y)
```

Ensure that the lines after `while True:` are indented by one tab.

So all together our file should say:

```python
from bantam import *

open_game_window('Spaaaaaace')

set_background_color('black')

pos_x = 400
pos_y = 300
ship_image = image_from_file('./ship2.gif')

while True:
  bantam_next_frame()

  pos_y = pos_y - 1

  draw_image(ship_image, pos_x, pos_y)
```

Switch back to the game window and press Control-r. You should see the ship zoom
off the top of the screen. It's not coming back. Press Control-r again to see it
once more.

What happened? Well, the chunk of code which comes after `while True:` repeats
forever (or until you quit the game).

First it gets to `bantam_next_frame()`
which just tells the game to wait for one 60th of a second. Why? Well, computer
screens can usually only handle updating their picture 60 times a second, so we
wait until the computer is ready before changing anything on the screen. 60 times
a second is pretty fast, so even if the objects on the screen move 60 times a
second, it's enough for it to look like smooth motion to us.

The next line is `pos_y = pos_y - 1`. This is updating the value called `pos_y`
which we previously set to `300` in the line `pos_y = 300`. What this means is,
we're setting `pos_y` to 'the previous value of `pos_y`, minus 1'. 

Then we draw the ship image on the screen with the line
`draw_image(ship_image, pos_x, pos_y)`. 

Because we just changed the value of `pos_y`, the ship will move up one pixel.
As the code after `while True:` runs over and over, eventually the ship will
continue to move up off the top of the screen.


Now lets take control of the ship. Change the file so it looks like this:

```python
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

```

Run it again. Try pressing the arrow keys on your keyboard and see what happens.

Try changing the number value of `amount_to_move` and reload the game. What happens?

Try changing `pos_x` and `pos_y`. What happens?
