import track
import pyglet
import numpy as np
from pyglet.window import key
from pyglet.gl.gl import GL_POINTS
from pyglet.libs.win32.constants import NULL
import car
from car import Car
import track
pyglet.resource.path = ['images']


car_img = pyglet.resource.image("car.png")

car_sprite = NULL

height = 720
width = 1280
game_window = pyglet.window.Window(width, height, resizable=True)

my_car = NULL
car_sprite = NULL

# create the batch of items
batch = pyglet.graphics.Batch()

racetrack_img = pyglet.resource.image("racetrackv2.png")
racetrack = pyglet.sprite.Sprite(img=racetrack_img, x=0, y=0)

keys = key.KeyStateHandler()
game_window.push_handlers(keys)


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def handle_input():
    # returns true if there is keyboard input, false otherwise
    if keys[key.UP]:
        if keys[key.LEFT]:
            my_car.accelerate('forward')
            my_car.turn('left')
            return True
        if keys[key.RIGHT]:
            my_car.accelerate('forward')
            my_car.turn('right')
            return True
        my_car.accelerate('forward')
        return True
    if keys[key.DOWN]:
        if keys[key.LEFT]:
            my_car.accelerate('backward')
            my_car.turn('left')
            return True
        if keys[key.RIGHT]:
            my_car.accelerate('backward')
            my_car.turn('right')
            return True
        my_car.accelerate('backward')
        return True
    if keys[key.LEFT]:
        if my_car.speed != 0:
            my_car.turn('left')
    if keys[key.RIGHT]:
        if my_car.speed != 0:
            my_car.turn('right')
    return False


@game_window.event
def on_draw():
    game_window.clear()
    racetrack.draw()
    batch.draw()
    track.wall_batch.draw()


@game_window.event
def update(dt):
    global my_car
    if not handle_input():
        my_car.decelerate()

    my_car.move()
    my_car.update_sprite()


if __name__ == '__main__':
    for wall in track.walls:
        wall.draw_wall()
    my_car = Car(car_sprite, loc=np.array(
        [float(width/3), float(height * 8.5/10)]))
    center_image(car_img)
    car_sprite = pyglet.sprite.Sprite(
        img=car_img, x=my_car.loc[0], y=my_car.loc[1], batch=batch)
    my_car.sprite = car_sprite
    car_sprite.rotation = my_car.rot
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()
