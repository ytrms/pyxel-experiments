import pyxel
import random

screen_x_dim: int = 120
screen_y_dim: int = 80
paddle_height: int = 10
paddle_width: int = 3
paddle_padding_from_screen = 3
puck_speed: int = 2


class Puck:
    def __init__(self):
        self.side_length = 2
        self.x = screen_x_dim // 2
        self.y = screen_y_dim // 2
        self.color = 7
        self.move_down = bool(random.getrandbits(1))
        self.move_right = bool(random.getrandbits(1))

    def move(self):
        if self.y == 0:
            self.move_down = True

        if self.y + self.side_length == screen_y_dim:
            self.move_down = False

        if self.move_down:
            self.y += puck_speed

        if not self.move_down:
            self.y -= puck_speed

        if self.move_right:
            self.x += puck_speed

        if not self.move_right:
            self.x -= puck_speed


class Paddle:
    def __init__(self, x_position, color):
        self.color = color
        self.height = paddle_height
        self.y = (screen_y_dim // 2) - (self.height // 2)
        self.x = x_position
        self.width = paddle_width

    def move_up(self):
        if self.y > 0:
            self.y = self.y - 2

    def move_down(self):
        if (self.y + self.height) < screen_y_dim:
            self.y = self.y + 2


def paddle_and_puck_collide(paddle: Paddle, puck: Puck) -> bool:
    """
    Given the paddle and a puck, returns whether the two collide.
    """

    if paddle.x < screen_x_dim // 2:
        # We are dealing with the left paddle
        if puck.x <= paddle.x + paddle.width:
            if puck.y < paddle.y + paddle.height // 2:
                if puck.y + puck.side_length >= paddle.y:
                    return True
            else:
                if puck.y <= paddle.y + paddle.height:
                    return True

    else:
        if puck.x + puck.side_length >= paddle.x:
            if puck.y < paddle.y + paddle.height // 2:
                if puck.y + puck.side_length >= paddle.y:
                    return True
            else:
                if puck.y <= paddle.y + paddle.height:
                    return True
    return False


class App:
    def __init__(self, x_dim, y_dim):
        self.screen_x_dim = x_dim
        self.screen_y_dim = y_dim
        self.score1 = 0
        self.score2 = 0
        self.game_paused: bool = True
        self.best_of_msg: str = "BEST OF 9"
        self.p1won: bool = False
        self.p2won: bool = False

        pyxel.init(self.screen_x_dim, self.screen_y_dim, caption="PONG")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.p1won or self.p2won:
                pyxel.quit()
            else:
                self.game_paused = not self.game_paused

        if not self.game_paused:
            # Listening to input
            if pyxel.btn(pyxel.KEY_Q):
                paddle1.move_up()

            if pyxel.btn(pyxel.KEY_A):
                paddle1.move_down()

            if pyxel.btn(pyxel.KEY_O):
                paddle2.move_up()

            if pyxel.btn(pyxel.KEY_L):
                paddle2.move_down()

            # move puck
            the_puck.move()

            # check collision for both paddles
            if the_puck.x <= paddle_width + paddle_padding_from_screen:
                if paddle_and_puck_collide(paddle1, the_puck):
                    the_puck.move_right = True
            elif the_puck.x + the_puck.side_length >= screen_x_dim - paddle_padding_from_screen - \
                    paddle_width:
                if paddle_and_puck_collide(paddle2, the_puck):
                    the_puck.move_right = False

            # update points and set ball
            if the_puck.x <= 0:
                self.score2 += 1
                the_puck.x = paddle2.x - paddle2.width
                the_puck.y = paddle2.y + paddle2.height // 2
                if self.score2 >= 5:
                    self.best_of_msg = "BRAVO P2"
                    self.p2won = True
                self.game_paused = True

            if the_puck.x + the_puck.side_length >= screen_x_dim:
                self.score1 += 1
                the_puck.x = paddle1.x + paddle1.width
                the_puck.y = paddle1.y + paddle1.height // 2
                if self.score1 >= 5:
                    self.best_of_msg = "BRAVO P1"
                    self.p1won = True
                self.game_paused = True


    def draw(self):
        if not self.game_paused:
            pyxel.cls(0)
            pyxel.rect(paddle1.x, paddle1.y, paddle1.width, paddle1.height, paddle1.color)
            pyxel.rect(paddle2.x, paddle2.y, paddle2.width, paddle2.height, paddle2.color)
            pyxel.rect(the_puck.x, the_puck.y, the_puck.side_length, the_puck.side_length, the_puck.color)
            pyxel.text(screen_x_dim // 3, paddle_padding_from_screen, str(self.score1), 7)
            pyxel.text(screen_x_dim - screen_x_dim // 3, paddle_padding_from_screen, str(self.score2), 7)
        else:
            best_of_width = len(self.best_of_msg) * 3
            pyxel.text(screen_x_dim // 2 - best_of_width // 2 - 6, screen_y_dim - screen_y_dim // 3,
                       self.best_of_msg, 7)
            pyxel.text(screen_x_dim // 2 - 17, screen_y_dim - screen_y_dim // 3 + 6, "SPACEBAR", 7)


paddle1 = Paddle(paddle_padding_from_screen, 5)
paddle2 = Paddle(screen_x_dim - paddle_width - paddle_padding_from_screen, 8)
the_puck = Puck()

App(screen_x_dim, screen_y_dim)
