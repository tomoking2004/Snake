# coding: utf-8
from game import SnakeGame, GUI
from agents import Human_Agent, Random_Agent
from dqn import DQN_Agent


def app():
    # 環境生成
    env = SnakeGame(None, None)
    gui = GUI(env)

    # エージェント生成
    #agent = Random_Agent(env)
    #agent = Human_Agent(gui)
    agent = DQN_Agent(env)
    agent.load("models/3layer_dqn_100.h5")

    # 機能拡張
    env.gui = gui
    env.agent = agent

    # 起動
    env.play()
    gui.mainloop()


if __name__=="__main__":
    app()
