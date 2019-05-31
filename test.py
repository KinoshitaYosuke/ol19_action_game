import cv2
import numpy as np
import time

from Field_Maker import *

#ステージの大きさ
F_SIZE_X = 5000
F_SIZE_Y = 750
D_SIZE_X = 1300
D_SIZE_Y = 750

#ステージギミック
EMPTY = 0
BLOCK = 1
NEEDLE = -100
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

def Make_Field(level):
    img = cv2.imread("./block.png")
    needle = cv2.imread("./needle.png")
    texture = img[0:50, 0:50], img[0:50, 50:100], img[0:50, 100:150], img[50:100, 0:50], img[50:100, 50:100], img[50:100, 100:150], img[100:150, 0:50], img[100:150, 50:100], img[100:150, 100:150]
    field = np.zeros((F_SIZE_Y, F_SIZE_X, 3), np.uint8)
    cv2.rectangle(field, (0, 0), (F_SIZE_X, F_SIZE_Y), (200, 200, 0), -1)
    texture_field = field.copy()
    

    if level == 0:
        field = Make_Check_Field(field, 0, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, (0, 0, 255))
        texture_field = Make_Texture(texture_field, 0, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, texture[0])
        
    elif level == 1:
        #フィールドの作成
        #注意：幅200，高さ300など，描画サイズは50の倍数になるようにすること，
        #色(0, 0, 255)：壁，色(255, 0, 0)：トゲ(現時点で未実装)，色(0, 255, 0)：ゴール
        #Make_Check_Field(描画する変数, x座標始点, y座標始点, 高さ, 幅, 色)
        field = Make_Check_Field(field, 0, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, (0, 0, 255))
        field = Make_Check_Field(field, 0, 0, 1000, F_SIZE_Y - 250, (0, 0, 255))
        field = Make_Check_Field(field, 300, 0, 800, F_SIZE_Y - 200, (0, 0, 255))
        field = Make_Check_Field(field, 1300, F_SIZE_Y - 100, 2000, F_SIZE_Y, (255, 0, 0))
        field = Make_Check_Field(field, 1600, 0, 2000, 100, (0, 0, 255))
        #Make_Check_Field(描画する変数, x座標始点, y座標始点, 高さ, 幅, 貼るテクスチャ)
        texture_field = Make_Texture(texture_field, 0, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, texture[0])
        texture_field = Make_Texture(texture_field, 0, 0, 1000, F_SIZE_Y - 250, texture[0])
        texture_field = Make_Texture(texture_field, 300, 0, 800, F_SIZE_Y - 200, texture[0])
        texture_field = Make_Texture(texture_field, 1300, F_SIZE_Y - 100, 2000, F_SIZE_Y, needle)
        texture_field = Make_Texture(texture_field, 1600, 0, 2000, 100, texture[0])
    
    elif level == 2:
        #フィールドの作成
        #注意：幅200，高さ300など，描画サイズは50の倍数になるようにすること，
        #色(0, 0, 255)：壁，色(255, 0, 0)：トゲ(現時点で未実装)，色(0, 255, 0)：ゴール
        #Make_Check_Field(描画する変数, x座標始点, y座標始点, 高さ, 幅, 色)
        field = Make_Check_Field(field, 0, F_SIZE_Y - 50, 2350, F_SIZE_Y, (0, 0, 255))
        field = Make_Check_Field(field, 2350, F_SIZE_Y - 50, 2450, F_SIZE_Y, (255, 0, 0))
        field = Make_Check_Field(field, 2450, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, (0, 0, 255))
        field = Make_Check_Field(field, 1300, 550, 1500, 600, (0, 0, 255))
        field = Make_Check_Field(field, 1450, 450, 1650, 500, (0, 0, 255))
        field = Make_Check_Field(field, 1600, 350, 2650, 400, (0, 0, 255))
        field = Make_Check_Field(field, 2650, 250, 2700, 400, (0, 0, 255))
        field = Make_Check_Field(field, 1800, F_SIZE_Y - 150, 2000, F_SIZE_Y, (0, 0, 255))
        field = Make_Check_Field(field, 1900, F_SIZE_Y - 200, 2000, F_SIZE_Y, (0, 0, 255))
        field = Make_Check_Field(field, 2200, 400, 2250, 600, (0, 0, 255))
        field = Make_Check_Field(field, 2600, 0, 3000, 100, (0, 0, 255))
        #Make_Check_Field(描画する変数, x座標始点, y座標始点, 高さ, 幅, 貼るテクスチャ)
        texture_field = Make_Texture(texture_field, 0, F_SIZE_Y - 50, 2350, F_SIZE_Y, texture[0])
        texture_field = Make_Texture(texture_field, 2350, F_SIZE_Y - 50, 2450, F_SIZE_Y, needle)
        texture_field = Make_Texture(texture_field, 2450, F_SIZE_Y - 50, F_SIZE_X, F_SIZE_Y, texture[0])
        texture_field = Make_Texture(texture_field, 1300, 550, 1500, 600, texture[1])
        texture_field = Make_Texture(texture_field, 1450, 450, 1650, 500, texture[1])
        texture_field = Make_Texture(texture_field, 1600, 350, 2650, 400, texture[1])
        texture_field = Make_Texture(texture_field, 2650, 250, 2700, 400, texture[1])
        texture_field = Make_Texture(texture_field, 1800, F_SIZE_Y - 150, 2000, F_SIZE_Y, texture[0])
        texture_field = Make_Texture(texture_field, 1900, F_SIZE_Y - 200, 2000, F_SIZE_Y, texture[0])
        texture_field = Make_Texture(texture_field, 2200, 400, 2250, 600, texture[1])
        texture_field = Make_Texture(texture_field, 2600, 0, 3000, 100, texture[0])

    cv2.rectangle(field, (F_SIZE_X - D_SIZE_X - 30, 0), (F_SIZE_X - D_SIZE_X, F_SIZE_Y), (0, 255, 0), -1)
    cv2.rectangle(texture_field, (F_SIZE_X - D_SIZE_X - 30, 0), (F_SIZE_X - D_SIZE_X, F_SIZE_Y), (0, 255, 0), -1)

    return field, texture_field

def time_manage(start, current):
    if(current-start > 50 / 1000):
        return True
    else:
        return False

def Display_Start_Menu(stage):
    stage_select = 0
    start = time.time()
    while True:
        current = time.time()
        if time_manage(start, current):
            #cv2.imshow("background", background)
            start_menu = Make_Start_Manu(stage[stage_select])

            key = cv2.waitKey(10)
            if key == CV_WAITKEY_W:
                if stage_select > 0:
                    stage_select -= 1
            elif key == CV_WAITKEY_X:
                if stage_select < 3:
                    stage_select += 1
            elif key == CV_WAITKEY_Z:
                break
            
            start_menu, stage_select = Select_Stage(start_menu, stage_select)
            
            cv2.imshow("drawing", start_menu)
            start = current


def Make_Start_Manu(start_menu):
    #start_menu = np.zeros((D_SIZE_Y, D_SIZE_X, 3), np.uint8)
    cv2.putText(start_menu, "Select Stage", (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 10, cv2.LINE_AA)
    cv2.putText(start_menu, "Level. 1", (550, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)
    cv2.putText(start_menu, "Level. 2", (550, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)
    cv2.putText(start_menu, "Level. 3", (550, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)
    #cv2.putText(start_menu, "Level. X", (550, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
    return start_menu

def Select_Stage(start_menu, stage_select):
    if stage_select == 0:
        cv2.putText(start_menu, "Level. 1", (550, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
    elif stage_select == 1:
        cv2.putText(start_menu, "Level. 2", (550, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
    elif stage_select == 2:
        cv2.putText(start_menu, "Level. 3", (550, 500), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
    elif stage_select == 3:
        cv2.putText(start_menu, "Level. X", (550, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (100, 0, 100), 5, cv2.LINE_AA)
    
    return start_menu, stage_select

def After_Process(word):
    clear = np.zeros((D_SIZE_Y, D_SIZE_X, 3), np.uint8)
    cv2.putText(clear, word, (300, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 10, cv2.LINE_AA)
    cv2.putText(clear, "Push W: Start Menu", (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)
    cv2.putText(clear, "Push X: Finish", (400, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)
    cv2.imshow("drawing", clear)
    while True:
        key = cv2.waitKey(0)
        if key == CV_WAITKEY_W:
            return True
        elif key == CV_WAITKEY_X:
            return False
    
    return False

def Display_After_Menu(clear_flag):
    if clear_flag == True:
        continue_flag = After_Process("Conguratulation!!")
    else:
        continue_flag = After_Process("Stage Failuer...")

    return continue_flag

def Load_Board():
    img = cv2.imread("./skateboard.png")
    #白領域をマスク黒化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, 0)
    img[thresh == 255] = [200, 200, 0]
    cv2.imshow("slate", img)
    return img

def Player_Transparent_2(mask_d, player_img, skate_board):
    img = player_img.copy()
    mask = mask_d.copy()
    
    back = np.zeros_like(img)
    img[mask == 0] = [200, 200, 0]
    img[img.shape[0] - 10:img.shape[0], 0:50] = skate_board

    #display[player.get_y() - player.get_h():player.get_y(), player.get_x() - player.get_w():player.get_x()] = img

    return img



def main():
    _, stage_0 = Make_Field(0)
    _, stage_1 = Make_Field(1)
    _, stage_2 = Make_Field(2)
    _, stage_3 = Make_Field(0)
    show_stage = stage_0[0:D_SIZE_Y, 1000:D_SIZE_X+1000], stage_1[0:D_SIZE_Y, 1000:D_SIZE_X+1000], stage_2[0:D_SIZE_Y, 1000:D_SIZE_X+1000], stage_3[0:D_SIZE_Y, 1000:D_SIZE_X+1000]
    #show_stage = stage[0][0:D_SIZE_Y,0:D_SIZE_X], stage[1][0:D_SIZE_Y,0:D_SIZE_X], stage[2][0:D_SIZE_Y,0:D_SIZE_X], stage[3][0:D_SIZE_Y,0:D_SIZE_X]
    while True:
        Display_Start_Menu(show_stage)
        Display_After_Menu(True)
        Display_After_Menu(False)

if __name__ == '__main__':
    main()