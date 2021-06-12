# coding; utf-8
import random


class Random_Agent:

    def __init__(self, env):
        self.env = env

    def get_action(self):
        return random.choice(self.env.actions)


class Human_Agent:

    def __init__(self, gui):
        self.gui = gui
        self.action = 0
        self.gui.bind("<Up>", lambda _: self.set_action(0))
        self.gui.bind("<Left>", lambda _: self.set_action(1))
        self.gui.bind("<Right>", lambda _: self.set_action(2))
        self.gui.bind("<Down>", lambda _: self.set_action(3))

    def set_action(self, action):
        self.action = action

    def get_action(self):
        return self.action
