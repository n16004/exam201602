from tkinter import *
import random
import time


def point_collision(a, b):
    cx = (b[2] - b[0]) / 2
    cy = (b[3] - b[1]) / 2
    r = cx
    # left-top
    dx = cx - a[0]
    dy = cy - a[1]
    p1 = dx ** 2 + dy ** 2 < r ** 2
    # right-top
    dx = cx - a[2]
    dy = cy - a[1]
    p2 = dx ** 2 + dy ** 2 < r ** 2
    # right-bottom
    dx = cx - a[2]
    dy = cy - a[3]
    p3 = dx ** 2 + dy ** 2 < r ** 2
    # left-bottom
    dx = cx - a[0]
    dy = cy - a[3]
    p4 = dx ** 2 + dy ** 2 < r ** 2

    return p1 or p2 or p3 or p4


class Ball:
    def __init__(self, canvas, paddle, blocks, speed, color):
        self.canvas = canvas
        self.paddle = paddle
        self.speed = speed
        self.blocks = blocks
        self.id = canvas.create_oval(5, 5, 25, 25, fill=color)
        self.canvas.move(self.id, 470, 300)
        self.x = 0
        self.y = 0
        self.count = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.canvas.bind_all('<KeyPress-Return>', self.start)

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
            return False

    def hit_block(self, pos):
        collision_type = 0
        for block in self.blocks:
            block_pos = self.canvas.coords(block.id)
            c = [(pos[2] - pos[0]) / 2 + pos[0], (pos[3] - pos[1]) / 2 + pos[1]]

            if block_pos[0] <= c[0] <= block_pos[2]:
                if block_pos[1] <= pos[3] < block_pos[3] or block_pos[1] \
                        < pos[1] <= block_pos[3]:
                    collision_type |= 1

            if block_pos[1] <= c[1] <= block_pos[3]:
                if block_pos[0] <= pos[2] < block_pos[2] or block_pos[0] \
                        < pos[0] <= block_pos[2]:
                    collision_type |= 2

            if collision_type != 0:
                return (block, collision_type)

        return (None, None)

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y *= -1
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = self.y * -1
            if self.paddle.x == PADDLE_SPEED:
                self.x += 1 / 2
            if self.paddle.x == -PADDLE_SPEED:
                self.x -= 1 / 2
        if pos[0] <= 0:
            self.x *= -1
        if pos[2] >= self.canvas_width:
            self.x *= -1
        (target, collision_type) = self.hit_block(pos)
        if target != None:
            self.count += 100
            target.delete()
            del self.blocks[self.blocks.index(target)]
            if collision_type == 1:
                self.y *= -1.04
            if collision_type == 2:
                self.x *= -1.04

    def start(self, evt):
        self.x = -self.speed
        self.y = self.speed


class Paddle:
    def __init__(self, canvas, speed, color):
        self.canvas = canvas
        self.speed = speed
        self.id = canvas.create_rectangle(0, 0, PADDLE_WIDTH * 10, 15, fill=color)
        self.canvas.move(self.id, 200, 600)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
            if pos[0] < 0:
                self.x = 2
        if pos[2] >= self.canvas_width:
            self.x = 0
            if pos[2] > self.canvas_width:
                self.x = -2

    def turn_left(self, evt):
        self.x = -self.speed

    def turn_right(self, evt):
        self.x = self.speed


class Block:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.pos_x = x + random.randrange(0, 16, 4)
        self.pos_y = y
        self.id = canvas.create_rectangle(26, 35, 250 / BLOCK_WIDTH, 15, fill=color)
        self.canvas.move(self.id, 50 + self.pos_x * (100 / BLOCK_WIDTH), 25 + self.pos_y * 20)

    def delete(self):
        self.canvas.delete(self.id)


class TextLabel:
    def __init__(self, canvas, ball, text, x, y, fontsize, color):
        self.canvas = canvas
        self.ball = ball
        self.x = x
        self.y = y
        self.id = canvas.create_text(x, y, text=text, fill=color,
                                     font=('Times', fontsize), state='hidden')

    def draw(self):
        point = self.ball.count
        self.canvas.itemconfig(self.id, text=point, state='normal')
        if self.ball.hit_bottom != False:
            self.canvas.coords(self.id, 470, 410)
            self.canvas.itemconfig(self.id, font=('Times', 35), text='total-score %s /2400' % point)

    def show(self):
        self.canvas.itemconfig(self.id, state='normal')


        # config


WIDTH = 1000
HEIGHT = 700
FPS = 100
BALL_SPEED = 5
PADDLE_WIDTH = 20
PADDLE_SPEED = 12
BLOCK_WIDTH = 2
BLOCK_HEIGHT = 12
COLORS = ('cyan', 'green', 'red', 'orange', 'magenta', 'blue', 'pink', 'yellow')
JOKE_TEXT = ('"支配なんかしねえよ　この海で一番自由な奴が海賊王だ！！！！" ルフィー',
             '"俺は海賊王になる男だ！！！！！" - ルフィー',
             '"未来の海賊王のクルーがよ・・・・・・・・情けねえ顔するんじゃねえ！！！！！" - ルフィー',
             '"俺達の命ぐらい一緒に賭けてみろよ！！　仲間だろうが！！！！" - ルフィー',
             '"悪ィが俺は「神」に祈ったことがねｴ" - ゾロ',
             '"ルフィーは海賊王になる男だ！！１" - ゾロ''',
             '"女の・・・・・涙の落ちる音がした" - サンジ',
             '"今の時代を作れるのは、今を生きている人間だけだよ・・" - 冥王・レイリー',
             '"いつかまた会えたら！！！もう一度仲間と呼んでくれますか！！！？" - ビビ',)

# initialize
tk = Tk()
tk.title("Breakout")
tk.resizable(20, 20)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

blocks = []
for y in range(BLOCK_HEIGHT):
    for x in range(BLOCK_WIDTH):
        blocks.append(Block(canvas, x, y, random.choice(COLORS)))

paddle = Paddle(canvas, PADDLE_SPEED, 'black')
ball = Ball(canvas, paddle, blocks, BALL_SPEED, 'red')
gameover = TextLabel(canvas, ball, 'GameOver!', 250, 300, 50, 'red')
joke = TextLabel(canvas, ball, random.choice(JOKE_TEXT), 470, 332, 18, 'blue')
score = TextLabel(canvas, ball, '0', 460, 680, 20, 'black')

# mainloop
"""while True:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
        score.draw()
    else:
        gameover.show()
        joke.show()
        break

    tk.update_idletasks()
    tk.update()
    tk.after(10, update)
    time.sleep(1 / FPS)

tk.after(10, update)
tk.mainloop()
"""


def update():
    if not ball.hit_bottom:
        ball.draw()
        paddle.draw()
        score.draw()
    if ball.hit_bottom == True:
        canvas.itemconfig(gameover, state='normal')
        joke.show()

    tk.update_idletasks()
    tk.update()
    tk.after(10, update)
    time.sleep(1 / FPS)


tk.after(3, update)
tk.mainloop()

"""

from tkinter import *
import random


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.x = random.choice((-3, -2, -1, 1, 2, 3))
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True

        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = abs(self.y)

        if pos[3] >= self.canvas_height:
            # self.y = abs(self.y) * -1
            self.hit_bottom = True

        if pos[0] <= 0:
            self.x = abs(self.x)

        if pos[2] >= self.canvas_width:
            self.x = abs(self.x) * -1

        if self.hit_paddle(pos):
            self.y = abs(self.x) * -1


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, event):
        self.x = -3

    def turn_right(self, event):
        self.x = 3


tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
c = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
c.pack()
tk.update()

p = Paddle(c, 'blue')
ball = Ball(c, p, 'red')


def update():
    if not ball.hit_bottom:
        ball.draw()
        p.draw()

    tk.update_idletasks()
    tk.update()
    tk.after(10, update)


tk.after(10, update)
tk.mainloop()
"""