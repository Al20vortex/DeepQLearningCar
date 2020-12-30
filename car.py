import numpy as np
import pyglet
import math
from pyglet.libs.win32.constants import NULL
pyglet.resource.path = ['images']
car_img = pyglet.resource.image("car.png")
car_img.width = 20
car_img.height = 40
max_speed = 15.0
max_acc = 0.3
rot_speed = 3.9
deceleration = 0.2


class Car:
    def __init__(self, sprite, loc=np.array([0.0, 0.0]), rot=0.0):
        global car_img
        self.loc = loc
        self.speed = 0.0
        # acc represents forward and backward acceleration
        self.acc = max_acc
        self.sprite = sprite
        self.crashed = False
        self.rot = rot
        self.corners = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])

    def accelerate(self, string):
        # stub
        if (string == 'forward'):
            if self.speed + max_acc > max_speed:
                self.speed = max_speed
            else:
                self.speed += max_acc
        if (string == 'backward'):
            if self.speed - max_acc < -max_speed:
                self.speed = -max_speed
            else:
                self.speed -= max_acc

    def turn(self, direction):
        if (direction == 'left'):
            self.rot -= rot_speed * self.speed / 5.0
        if direction == 'right':
            self.rot += rot_speed * self.speed / 5.0
        self.update_sprite()

    def update_sprite(self):
        self.sprite.rotation = self.rot
        self.sprite.x = self.loc[0]
        self.sprite.y = self.loc[1]

    def decelerate(self):
        self.speed
        if self.speed > 0:
            if self.speed - deceleration > 0:
                self.speed -= deceleration
            else:
                self.speed = 0

        if self.speed < 0:
            if self.speed + deceleration < 0:
                self.speed += deceleration
            else:
                self.speed = 0

    def move(self):
        if self.crashed == True:
            return
        # self.loc[0] += self.speed * \
        #     -math.cos(self.rot * 2 * math.pi / 360)
        # self.loc[1] += self.speed * \
        #     math.sin(self.rot * 2 * math.pi / 360)
        self.loc[0] += self.speed * \
            math.sin(self.rot * 2 * math.pi / 360)
        self.loc[1] += self.speed * \
            math.cos(self.rot * 2 * math.pi / 360)
        self.update_sprite()

    def calculate_corners(self):
        pass

    def hitbox(self):
        pass
