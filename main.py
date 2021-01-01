import track
import pyglet
import numpy as np
from pyglet.window import key
from pyglet.gl.gl import GL_POINTS
from pyglet.libs.win32.constants import NULL
import tensorflow as tf
import car
from car import Car
import track
import random
pyglet.resource.path = ['images']


car_img = pyglet.resource.image("car.png")

car_sprite = NULL
height = 720
width = 1280

my_car = NULL
car_sprite = NULL
reward_label = NULL

# create the batch of items
batch = pyglet.graphics.Batch()
racetrack_img = pyglet.resource.image("racetrackv2.png")
racetrack = pyglet.sprite.Sprite(img=racetrack_img, x=0, y=0)


class Game:
    def center_image(self, image):
        """Sets an image's anchor point to its center"""
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

    def reset_game(self):
        global my_car
        my_car = Car(car_sprite, loc=np.array(
            [float(width/3), float(height * 8.5/10)]))
        for gate in track.reward_gates:
            gate.active = True

    def handle_crash(self):
        if my_car.crashed == True:
            self.reset_game()

    def handle_input(self):
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


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = Game()
        for wall in track.walls:
            wall.draw_wall()
        for gate in track.reward_gates:
            gate.draw_gate()
        global car_sprite
        global my_car
        my_car = Car(car_sprite, loc=np.array(
            [float(width/3), float(height * 8.5/10)]))
        self.game.center_image(car_img)
        self.reward_label = pyglet.text.Label(text='Rewards: ' + str(
            my_car.rewards), color=(255, 255, 255, 255), font_size=10, x=width - 200, y=50, batch=batch)
        car_sprite = pyglet.sprite.Sprite(
            img=car_img, x=my_car.loc[0], y=my_car.loc[1], batch=batch)
        my_car.sprite = car_sprite
        car_sprite.rotation = my_car.rot
        # self.ai = QLearning(self.game)

    def update(self, dt):
        global my_car
        my_car.corner_graphics = []
        my_car.ray_graphics = []
        if not self.game.handle_input():
            my_car.decelerate()
        self.game.handle_crash()
        my_car.move()
        self.reward_label.text = 'Rewards: ' + str(
            my_car.rewards)
        my_car.calculate_corners()
        my_car.make_ray_corners()
        my_car.detect_collison()
        my_car.detect_rewards()
        my_car.update_sprite()

    def on_draw(self):
        game_window.clear()
        racetrack.draw()
        batch.draw()
        track.gate_batch.draw()
        track.wall_batch.draw()
        car.corner_batch.draw()
        car.ray_batch.draw()


if __name__ == '__main__':
    game_window = MyWindow(width, height, resizable=True)
    keys = key.KeyStateHandler()
    game_window.push_handlers(keys)
    pyglet.clock.schedule_interval(game_window.update, 1/60.0)
    pyglet.app.run()
