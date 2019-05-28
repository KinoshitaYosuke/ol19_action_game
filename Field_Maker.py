
import cv2
import numpy as np

import time
from Subtraction import *

#ステージの大きさ
F_SIZE_X = 2500
F_SIZE_Y = 300
D_SIZE_X = 600
D_SIZE_Y = 300

#ステージギミック
EMPTY = 0
BLOCK = 1
NEEDLE = 2
COIN = 3
CLEAR = 100

#当たり判定
NO_HIT = 0
HIT_Y_DOWN = 1
HIT_Y_UP = 2
HIT_X = 3
HIT_XY_DOWN = 4
HIT_XY_UP = 5
HIT_XY = 6

#プレイヤー状態
STAND = 0
JUMP = 1
BEND = 2

#キー入力
CV_WAITKEY_X = 120
CV_WAITKEY_W = 119
CV_WAITKEY_Z = 122
CV_WAITKEY_ENTER = 13
CV_WAITKEY_ESC = 27
CV_WAITKEY_SPACE = 32
CV_WAITKEY_TAB = 9

def Make_Field():
    field = np.zeros((F_SIZE_Y, F_SIZE_X, 3), np.uint8)
    cv2.rectangle(field, (0, 0), (F_SIZE_X, F_SIZE_Y), (200, 200, 0), -1)
    cv2.rectangle(field, (0, F_SIZE_Y - 50), (F_SIZE_X, F_SIZE_Y), (0, 0, 255), -1)
    cv2.rectangle(field, (0, 0), (1000, F_SIZE_Y - 250), (0, 0, 255), -1)
    cv2.rectangle(field, (300, 0), (800, F_SIZE_Y - 200), (0, 0, 255), -1)
    cv2.rectangle(field, (1300, F_SIZE_Y - 120), (2000, F_SIZE_Y), (0, 0, 255), -1)
    cv2.rectangle(field, (1600, 0), (2000, 100), (0, 0, 255), -1)
    cv2.rectangle(field, (200, 350), (300, 450), (0, 0, 255), -1)

    cv2.rectangle(field, (F_SIZE_X - D_SIZE_X, 0), (F_SIZE_X - D_SIZE_X + 30, F_SIZE_Y), (0, 255, 0), -1)

    return field

def Check_Field(stage):
    cv2.imshow("stage", stage)
    cv2.waitKey(0)

def time_manage(start, current):
    if(current-start > 50 / 1000):
        return True
    else:
        return False

def Move_Field(stage):
    
    stride_count = 0
    
    start = time.time()
    while stride_count < F_SIZE_X - (F_SIZE_Y * 2):
        current = time.time()

        if time_manage(start, current):
            test = stage[0:D_SIZE_Y, stride_count:D_SIZE_X + stride_count]
            display = test.copy()
            cv2.imshow("drawing", display)
            cv2.waitKey(10)
            start = current
            stride_count += 5

    return 0

def main():
    stage = Make_Field()
    Check_Field(stage)
    Move_Field(stage)

if __name__ == '__main__':
    main()