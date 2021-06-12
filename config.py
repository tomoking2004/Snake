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
BLOCK_SIZE = 30
CANVAS_SIZE = MAP_SIZE * BLOCK_SIZE
GROW_SNAKE = True  # 蛇の成長

# GUI
COLORS = ["grey10", "grey90", "yellow", "orange"]
DRAW_SIGHT = False  # 観測線の描画

#----------agents----------
#----------dqn----------
# Q_Network
INPUT_SHAPE = (12, )  # 入力形状(状態の形状)
OUTPUT_SIZE = 4  # 出力サイズ(行動のサイズ)
LR = 0.001  # 学習係数
GAMMA = 0.95  # 割引係数
DQN_MODEL_PATH = 'models/ddqn_model5k.h5'  # DQNモデルのパス

# Memory
MEMORY_SIZE = 5000  # メモリサイズ
BATCH_SIZE = 32  # バッチサイズ

# Trainer
DQN_MODE = 0  # DQNモード(0:DDQN, 1:DQN)
LOAD_MODEL = True  # モデルのロード
SAVE_MODEL = True  # モデルのセーブ
SAVE_CYCLE = 50  # 定期セーブ周期
NUM_EPISODES = 50000  # エピソード数
MAX_STEPS = 500  # 最大ステップ数
GOAL_AVG_REWARD = 100  # 目標平均報酬
AVG_SIZE = 10  # 平均する集合の大きさ
