import pyxel
import random


class App:
    def __init__(self):
        self.screen_x_dim = 160
        self.screen_y_dim = 120

        self.rect_side_size = 20
        self.ball_color = 5

        self.x = random.randint(0, self.screen_x_dim - self.rect_side_size)
        self.y = random.randint(0, self.screen_y_dim - self.rect_side_size)

        self.moving_right = True
        self.moving_down = True

        pyxel.init(self.screen_x_dim, self.screen_y_dim, caption="Bouncing Rectangle")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.x == 0:
            self.moving_right = True

        if self.x == self.screen_x_dim - self.rect_side_size:
            self.moving_right = False

        if self.y == 0:
            self.moving_down = True

        if self.y == self.screen_y_dim - self.rect_side_size:
            self.moving_down = False

        if self.moving_down:
            self.y = self.y + 1
        else:
            self.y = self.y - 1

        if self.moving_right:
            self.x = self.x + 1
        else:
            self.x = self.x - 1

    def draw(self):
        pyxel.cls(4)
        pyxel.rect(self.x, self.y, self.rect_side_size, self.rect_side_size, self.ball_color)


App()
