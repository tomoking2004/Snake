# coding: utf-8
import random
import numpy as np
import tkinter as tk

from config import *


class Snake:
    """スネーク環境"""

    def __init__(self):
        self.map = np.zeros((MAP_SIZE, MAP_SIZE)) # 環境
        self.snake_pos = []  # 蛇座標
        self.food_pos = None  # 食料座標
        self.actions = [0,1,2,3]  # 行動の集合
        self.direction = (0,0)  # 進行方向
        self.score = 0  # スコア
        self.steps = 0  # ステップ数
        self.useless_steps = 0  # 無駄なステップ数
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

    def get_state(self):
        state = []
        # 食べ物があるか(4方向)
        ox, oy = self.snake_pos[0]
        fx, fy = self.food_pos
        state.append(1 if oy>fy else 0)
        state.append(1 if fx>ox else 0)
        state.append(1 if fy>oy else 0)
        state.append(1 if ox>fx else 0)
        # 障害物が目の前にあるか(4方向)
        for dx, dy in [(0,-1),(1,0),(0,1),(-1,0)]:
            x, y = ox+dx, oy+dy
            if not 0<=x<MAP_SIZE or not 0<=y<MAP_SIZE or (x,y) in self.snake_pos[1:]:
                state.append(1)
            else:
                state.append(0)
        # 進んでいる方向(4方向)
        dx, dy = self.direction
        state.append(1 if dy==-1 else 0)
        state.append(1 if dx==1 else 0)
        state.append(1 if dy==1 else 0)
        state.append(1 if dx==-1 else 0)
        return np.reshape(state, (1, *INPUT_SHAPE))

    def is_actable(self, action):
        x, y = self.snake_pos[0]
        dx, dy = action
        _x, _y = x+dx, y+dy
        if 0<=_x<MAP_SIZE and 0<=_y<MAP_SIZE and (_x,_y) not in self.snake_pos:
            return True
        else:
            return False

    def is_terminal(self, action):
        if not self.is_actable(action) or self.useless_steps>100:
            return True  #無効な動作をしたら/無駄なステップが100回以上続いたら終了
        else:
            return False

    def get_reward(self, action):
        dx, dy = action
        x, y = self.snake_pos[0]
        _x, _y = x+dx, y+dy
        fx, fy = self.food_pos
        if (_x,_y)==self.food_pos:
            self.useless_steps = 0
            return 10  #食べ物を獲得した
        elif (fx-_x)**2 + (fy-_y)**2 < (fx-x)**2 + (fy-y)**2:
            return 1  #食べ物に近づく
        else:
            return -1  #食べ物から離れる


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
        self.direction = action

    # メインメソッド
    def step(self, _action):
        # 上左右下
        action = [(-1,0), (0,-1), (0,1), (1,0)][_action]
        self.steps += 1
        self.useless_steps += 1

        # 遷移先の状態,報酬,終端の取得
        terminal = self.is_terminal(action)
        if terminal:
            reward = -100
            state = self.get_state()
            return state, reward, True, None
        else:
            reward = self.get_reward(action)
            self.move(action)
            state = self.get_state()
            return state, reward, False, None

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
            self.gui.after(1, self.loop)

    def play(self):
        self.gui.canvas_update()
        self.loop()

    def reset(self):  # 改
        if self.gui.highscore < self.score:
            self.gui.highscore = self.score
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
        self.highscore = 0
        self.canvas.pack()

    # メインメソッド
    def canvas_update(self):
        # 全削除
        self.title("score: {}, highscore: {}".format(self.env.score, self.highscore))
        self.canvas.delete("canvas")
        # ゲーム描画
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                _x,_y = self.coordinates[y][x]
                code = self.env.map[y][x]
                fill = self.colors[int(code)]
                self.canvas.create_rectangle(_x,_y,_x+BLOCK_SIZE,_y+BLOCK_SIZE,fill=fill,tag="canvas")
