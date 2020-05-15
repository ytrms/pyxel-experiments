import pyxel
import random

ball_radius = 5
screen_x_dim = 160
screen_y_dim = 100


class Ball():
    def __init__(self, color):
        self.radius = ball_radius
        self.color = color
        self.moving_down = bool(random.getrandbits(1))
        self.moving_right = bool(random.getrandbits(1))
        self.x = random.randint(0+ball_radius, screen_x_dim-ball_radius)
        self.y = random.randint(0+ball_radius, screen_y_dim-ball_radius)

    def toggle_horizontal_movement(self):
        self.moving_right = not self.moving_right

    def toggle_vertical_movement(self):
        self.moving_down = not self.moving_right


ball0 = Ball(6)
ball1 = Ball(2)
ball2 = Ball(3)

ball_list = [ball0, ball1, ball2]


class App:
    def __init__(self, screen_x_dim, screen_y_dim, list_of_balls):
        self.list_of_balls = list_of_balls
        self.screen_x_dim = screen_x_dim
        self.screen_y_dim = screen_y_dim

        pyxel.init(self.screen_x_dim, self.screen_y_dim, caption="Bouncing Balls")
        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.mouse(True)

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        for ball in ball_list:
            if ball.moving_right:
                ball.x += 1
            else:
                ball.x -= 1

            if ball.moving_down:
                ball.y += 1
            else:
                ball.y -= 1

            if ball.x == 0 + ball_radius:
                ball.moving_right = True

            if ball.x == self.screen_x_dim - ball.radius:
                ball.moving_right = False

            if ball.y == 0 + ball_radius:
                ball.moving_down = True

            if ball.y == self.screen_y_dim - ball.radius:
                ball.moving_down = False

    def draw(self):
        cycled_color = ((pyxel.frame_count//20) % 15) + 1
        pyxel.cls(0)
        pyxel.tri(ball0.x, ball0.y, ball1.x, ball1.y, ball2.x, ball2.y, cycled_color)
        for ball in ball_list:
            pyxel.circ(ball.x, ball.y, ball.radius, ball.color)


App(screen_x_dim, screen_y_dim, ball_list)
