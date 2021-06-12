# coding: utf-8
import random
import numpy as np
import tkinter as tk

from config import *


class Snake:
    """スネーク環境"""

    def __init__(self):
        self.map = np.zeros((MAP_SIZE, MAP_SIZE)) # 状態
        self.snake_pos = []  # 蛇座標
        self.food_pos = None  # 食料の座標
        self.score = 0  # スコア
        self.before_action = None
        self.actions = [0,1,2,3]
        self.spawn_snake()
        self.spawn_item()

    def spawn_snake(self):
        x, y = random.randint(0, MAP_SIZE-1), random.randint(0, MAP_SIZE-1)
        self.snake_pos.append((x, y))
        self.map[x][y] = 1

    def spawn_item(self):
        ls = [(x,y) for x in range(MAP_SIZE) for y in range(MAP_SIZE) if (x,y) not in self.snake_pos]
        x, y = random.choice(ls)
        self.food_pos = (x,y)
        self.map[x][y] = 2

    def is_actable(self, action):
        x, y = self.snake_pos[0]
        dx, dy = action
        _x, _y = x+dx, y+dy
        if 0<=_x<MAP_SIZE and 0<=_y<MAP_SIZE and (_x,_y) not in self.snake_pos:
            return True
        else:
            return False

    def get_map(self):
        return self.map.copy()

    def get_reward(self, action):
        x, y = self.snake_pos[0]
        dx, dy = action
        _x, _y = x+dx, y+dy
        if (_x,_y)==self.food_pos:
            return 1
        else:
            return 0

    def move(self, action):
        for x, y in self.snake_pos:
            self.map[x][y] = 0
        x, y = self.snake_pos[0]
        dx, dy = action
        _x, _y = x+dx, y+dy
        self.snake_pos = [(_x,_y)] + self.snake_pos
        if (_x,_y) == self.food_pos:
            if GROW_SNAKE==False:
                self.snake_pos.pop(-1)
            self.score += 1
            self.spawn_item()
        else:
            self.snake_pos.pop(-1)
        for x, y in self.snake_pos:
            self.map[x][y] = 1

    def is_terminal(self):
        if self.score>=100: # 100点に達したら終了
            return True
        else:
            return False

    def get_state(self):
        state = []
        # 食べ物の有無
        x1, y1 = self.snake_pos[0]
        x2, y2 = self.food_pos
        state.append(1 if x1>x2 else 0)
        state.append(1 if y1>y2 else 0)
        state.append(1 if y1<y2 else 0)
        state.append(1 if x1<x2 else 0)
        # 頭と体/壁の距離
        direction = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for dx, dy in direction:
            ox, oy = self.snake_pos[0]
            x, y = ox+dx, oy+dy
            while 0<=x<MAP_SIZE and 0<=y<MAP_SIZE:
                if (x,y) in self.snake_pos[1:]:
                    break
                x += dx
                y += dy
            dis = ((x-ox)**2 + (y-oy)**2) ** 0.5
            state.append(dis/MAP_SIZE)
        return np.reshape(state, (1, *INPUT_SHAPE))

    # メインメソッド
    def step(self, _action):
        # 上左右下
        action = [(-1,0), (0,-1), (0,1), (1,0)][_action]

        if self.is_actable(action)==False:
            state = self.get_state()
            return state, -1, True, None

        # 遷移先の状態,報酬,終端の取得
        reward = self.get_reward(action)
        self.move(action)
        terminal = self.is_terminal()
        state = self.get_state()
        return state, reward, terminal, None

    def reset(self):
        self.__init__()
        state = self.get_state()
        return state


class SnakeGame(Snake):
    """スネークゲーム"""
    
    def __init__(self, gui, agent):
        super().__init__()
        self.gui = gui
        self.agent = agent

    def loop(self):
        action = self.agent.get_action()
        _, _, terminal, _ = self.step(action)
        self.gui.canvas_update()
        if terminal:
            self.reset()
            self.gui.after(1000, self.loop)
        else:
            self.gui.after(100, self.loop)

    def play(self):
        self.gui.canvas_update()
        self.loop()

    def reset(self):  # 改
        self.__init__(self.gui, self.agent)
        state = self.get_state()
        return state


class GUI(tk.Tk):
    """GUI"""

    def __init__(self, env):
        super().__init__()
        self.env = env
        self.canvas = tk.Canvas(self,width=CANVAS_SIZE,height=CANVAS_SIZE,highlightthickness=0)
        self.coordinates = [[(BLOCK_SIZE*x, BLOCK_SIZE*y) 
                        for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
        self.colors = COLORS
        self.canvas.pack()

    # メインメソッド
    def canvas_update(self):
        # 全削除
        self.title("score: {}".format(self.env.score))
        self.canvas.delete("canvas")
        # ゲーム描画
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                _x,_y = self.coordinates[y][x]
                code = self.env.map[y][x]
                fill = self.colors[int(code)]
                self.canvas.create_rectangle(_x,_y,_x+BLOCK_SIZE,_y+BLOCK_SIZE,fill=fill,tag="canvas")
        # 観測線描画
        if DRAW_SIGHT:
            direction = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]  # 8方向
            for dx, dy in direction:
                ox, oy = self.env.snake_pos[0]
                x, y = ox+dx, oy+dy
                while 0<=x<MAP_SIZE and 0<=y<MAP_SIZE:
                    if self.env.map[x][y]!=0:
                        break
                    x += dx
                    y += dy
                x1 = BLOCK_SIZE*(oy+0.5)
                y1 = BLOCK_SIZE*(ox+0.5)
                x2 = BLOCK_SIZE*(y+0.5)
                y2 = BLOCK_SIZE*(x+0.5)
                fill = self.colors[-1]
                self.canvas.create_line(x1, y1, x2, y2, fill=fill, tag="canvas")
                #print(self.env.get_state())
