# coding: utf-8
import os

"""環境定数"""

#----------debug----------
# When using tensorflow or keras
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
os.environ['KMP_DUPLICATE_LIB_OK']='True'

#----------game----------
# Snake
MAP_SIZE = 24
GROW_SNAKE = True  # 蛇の成長

# GUI
BLOCK_SIZE = 30
CANVAS_SIZE = MAP_SIZE * BLOCK_SIZE
COLORS = ["grey10", "grey90", "yellow", "orange"]

#----------dqn----------
# params
INPUT_SHAPE = (12, )  # 入力形状(状態の形状)
OUTPUT_SIZE = 4  # 出力サイズ(行動のサイズ)
LR = 0.001  # 学習係数
GAMMA = 0.95  # 割引係数
MEMORY_SIZE = 10000  # メモリサイズ
BATCH_SIZE = 500  # バッチサイズ
# train
DQN_MODEL_NAME = '3layer_dqn2'  # DQNモデルの名前
DQN_MODE = 0  # DQNモード(0:DDQN, 1:DQN)
SAVE_CYCLE = 100  # 定期セーブ周期
NUM_EPISODES = 1000  # エピソード数
#MAX_STEPS = 500  # 最大ステップ数
GOAL_AVG_REWARD = MAP_SIZE**2 - 1  # 目標平均報酬
AVG_SIZE = 10  # 平均する集合の大きさ
