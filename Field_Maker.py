import cv2
import numpy as np

import time
from Subtraction import *

#ステージの大きさ
F_SIZE_X = 5000
F_SIZE_Y = 750
D_SIZE_X = 1300
D_SIZE_Y = 750

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

def Make_Texture(stage, y, x, h, w, texture):
    print(y, x, h, w)
    for i in range(y, h, 50):
        for j in range(x, w, 50):
            print(i, j)
            stage[j:j+50, i:i+50] = texture
    return stage

def Make_Check_Field(stage, y, x, h, w, color):
    cv2.rectangle(stage, (y, x), (h, w), color, -1)
    return stage

def Make_Field():
    img = cv2.imread("./block.png")
    needle = cv2.imread("./needle.png")
    texture = img[0:50, 0:50], img[0:50, 50:100], img[0:50, 100:150], img[50:100, 0:50], img[50:100, 50:100], img[50:100, 100:150], img[100:150, 0:50], img[100:150, 50:100], img[100:150, 100:150]
    field = np.zeros((F_SIZE_Y, F_SIZE_X, 3), np.uint8)
    cv2.rectangle(field, (0, 0), (F_SIZE_X, F_SIZE_Y), (200, 200, 0), -1)
    texture_field = field.copy()
    """
    #フィールドの作成
    #注意：幅200，高さ300など，描画サイズは50の倍数になるようにすること，
    #色texture[2]：壁，色(255, 0, 0)：トゲ(現時点で未実装)，色(0, 255, 0)：ゴール
    #Make_Check_Field(描画する変数, x座標始点, y座標始点, 高さ, 幅, 色)
    field = Make_Check_Field(field, 0, F_SIZE_Y - 50, 2000, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1000, F_SIZE_Y - 100, 1150, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1050, F_SIZE_Y - 150, 1100, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1100, F_SIZE_Y - 200, 1250, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1350, F_SIZE_Y - 100, 1600, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1350, F_SIZE_Y - 150, 1550, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1350, F_SIZE_Y - 200, 1500, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 2200, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1850, F_SIZE_Y - 100, 2000, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1900, F_SIZE_Y - 150, 2000, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1950, F_SIZE_Y - 200, 2100, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 2200, F_SIZE_Y - 100, 2450, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 2200, F_SIZE_Y - 150, 2400, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 2200, F_SIZE_Y - 200, 2350, F_SIZE_Y, (0, 0, 255))

    field = Make_Check_Field(field, 2600, F_SIZE_Y - 200, 2650, F_SIZE_Y - 150, (0, 0, 255))
    field = Make_Check_Field(field, 2650, F_SIZE_Y - 200, 2700, F_SIZE_Y - 150, (0, 0, 255))
    field = Make_Check_Field(field, 2700, F_SIZE_Y - 200, 2750, F_SIZE_Y - 150, (0, 0, 255))
    field = Make_Check_Field(field, 2750, F_SIZE_Y - 200, 2800, F_SIZE_Y - 150, (0, 0, 255))
    
    field = Make_Check_Field(field, 3000, F_SIZE_Y - 100, 3400, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 3050, F_SIZE_Y - 150, 3400, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 3100, F_SIZE_Y - 200, 3400, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 3150, F_SIZE_Y - 250, 3400, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 3200, F_SIZE_Y - 300, 3400, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 3250, F_SIZE_Y - 350, 3400, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 3300, F_SIZE_Y - 400, 3400, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 3350, F_SIZE_Y - 450, 3400, F_SIZE_Y, (0, 0, 255))

    #Make_Check_Field(描画する変数, x座標始点, y座標始点, 高さ, 幅, 貼るテクスチャ)
    texture_field = Make_Texture(texture_field, 0, F_SIZE_Y - 50, 2000, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 1000, F_SIZE_Y - 100, 1150, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 1050, F_SIZE_Y - 150, 1100, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 1100, F_SIZE_Y - 200, 1250, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 1350, F_SIZE_Y - 100, 1600, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 1350, F_SIZE_Y - 150, 1550, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 1350, F_SIZE_Y - 200, 1500, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 2200, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 1850, F_SIZE_Y - 100, 2000, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 1900, F_SIZE_Y - 150, 2000, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 1950, F_SIZE_Y - 200, 2100, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 2200, F_SIZE_Y - 100, 2450, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 2200, F_SIZE_Y - 150, 2400, F_SIZE_Y, texture[1])
    texture_field = Make_Texture(texture_field, 2200, F_SIZE_Y - 200, 2350, F_SIZE_Y, texture[1])

    texture_field = Make_Texture(texture_field, 2600, F_SIZE_Y - 350, 2650, F_SIZE_Y - 300, texture[6])
    texture_field = Make_Texture(texture_field, 2650, F_SIZE_Y - 350, 2700, F_SIZE_Y - 300, texture[6])
    texture_field = Make_Texture(texture_field, 2700, F_SIZE_Y - 350, 2750, F_SIZE_Y - 300, texture[3])
    texture_field = Make_Texture(texture_field, 2750, F_SIZE_Y - 350, 2800, F_SIZE_Y - 300, texture[6])
    
    texture_field = Make_Texture(texture_field, 3000, F_SIZE_Y - 100, 3400, F_SIZE_Y - 50, texture[7])
    texture_field = Make_Texture(texture_field, 3050, F_SIZE_Y - 150, 3400, F_SIZE_Y - 50, texture[7])
    texture_field = Make_Texture(texture_field, 3100, F_SIZE_Y - 200, 3400, F_SIZE_Y - 50, texture[7])
    texture_field = Make_Texture(texture_field, 3150, F_SIZE_Y - 250, 3400, F_SIZE_Y - 50, texture[7])
    texture_field = Make_Texture(texture_field, 3200, F_SIZE_Y - 300, 3400, F_SIZE_Y - 50, texture[7])
    texture_field = Make_Texture(texture_field, 3250, F_SIZE_Y - 350, 3400, F_SIZE_Y - 50, texture[7])
    texture_field = Make_Texture(texture_field, 3300, F_SIZE_Y - 400, 3400, F_SIZE_Y - 50, texture[7])
    texture_field = Make_Texture(texture_field, 3350, F_SIZE_Y - 450, 3450, F_SIZE_Y - 50, texture[7])
    """
    field = Make_Check_Field(field, 0, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, (0, 0, 255))
    field = Make_Check_Field(field, 1000, 550, 1000 + 500, 550 + 150, (0, 0, 255))
    field = Make_Check_Field(field, 1575, 550, 1575 + 200, 550 + 150, (0, 0, 255))
    field = Make_Check_Field(field, 2300, 550, 2300 + 300, 550 + 150, (0, 0, 255))
    field = Make_Check_Field(field, 2600, 400, 2600 + 300, 400 + 300, (0, 0, 255))
    field = Make_Check_Field(field, 2900, 250, 2900 + 300, 250 + 450, (0, 0, 255))

    #トゲ
    field = Make_Check_Field(field, 1512, 0, 1512 + 50, 250, (255, 0, 0))
    field = Make_Check_Field(field, 1575, 0, 1575+ 500, 400, (255, 0, 0))
    field = Make_Check_Field(field, 1500, 650, 1500 + 100, 650 + 50, (255, 0, 0))
    field = Make_Check_Field(field, 3200, 650, 3200 + 500, 650 + 50, (255, 0, 0))

    #Make_Check_Field(描画する変数, x座標始点, y座標始点, 高さ, 幅, 貼るテクスチャ)

    #ブロック
    texture_field = Make_Texture(texture_field, 0, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, texture[0])
    texture_field = Make_Texture(texture_field, 1000, 550, 1000 + 500, 550 + 150, texture[0])
    texture_field = Make_Texture(texture_field, 1575, 550, 1575 + 200, 550 + 150, texture[0])
    texture_field = Make_Texture(texture_field, 2300, 550, 2300 + 300, 550 + 150, texture[0])
    texture_field = Make_Texture(texture_field, 2600, 400, 2600 + 300, 400 + 300, texture[0])
    texture_field = Make_Texture(texture_field, 2900, 250, 2900 + 300, 250 + 450, texture[0])

    #トゲ
    texture_field = Make_Texture(texture_field, 1512, 0, 1512 + 50, 250, needle)
    texture_field = Make_Texture(texture_field, 1575, 0, 1575+ 500, 400, needle)
    texture_field = Make_Texture(texture_field, 1500, 650, 1500 + 100, 650 + 50, needle)
    texture_field = Make_Texture(texture_field, 3200, 650, 3200 + 500, 650 + 50, needle)

    cv2.rectangle(field, (F_SIZE_X - D_SIZE_X - 30, 0), (F_SIZE_X - D_SIZE_X, F_SIZE_Y), (0, 255, 0), -1)
    cv2.rectangle(texture_field, (F_SIZE_X - D_SIZE_X - 30, 0), (F_SIZE_X - D_SIZE_X, F_SIZE_Y), (0, 255, 0), -1)

    return field, texture_field

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
    while stride_count < F_SIZE_X - D_SIZE_X:
        current = time.time()

        if time_manage(start, current):
            test = stage[0:D_SIZE_Y, stride_count:D_SIZE_X + stride_count]
            display = test.copy()
            cv2.imshow("drawing", display)
            cv2.waitKey(10)
            start = current
            stride_count += 10

    return 0

def main():
    stage,texture = Make_Field()
    #Check_Field(stage)
    Move_Field(texture)

if __name__ == '__main__':
    main()