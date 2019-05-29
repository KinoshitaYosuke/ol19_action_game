import cv2
import numpy as np

import time
from Subtraction import *
from Field_Maker import *

#ステージの大きさ
F_SIZE_X = 5000
F_SIZE_Y = 720
D_SIZE_X = 1280
D_SIZE_Y = 720

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

class Player:
    def __init__(self):
        self.player_state
        self.coordinate_x
        self.coordinate_y
        self.width
        self.height
        self.move_x
        self.move_y
        self.jump_counter
        self.hit_info
    
    def initial_coordinate():
        Player.player_state = STAND
        Player.width = 50
        Player.height = 100
        Player.move_x = 0
        Player.move_y = 0
        #Player.coordinate_x = (int)(D_SIZE_X / 2) - Player.width
        #Player.coordinate_y = 250 - Player.height
        Player.coordinate_x = (int)(D_SIZE_X / 2)
        Player.coordinate_y = D_SIZE_Y - 50
        Player.jump_counter = 20


    def set_coordinate():
        Player.coordinate_x -= Player.move_x
        Player.coordinate_y -= Player.move_y
        
    def change_state(state):
        if Player.player_state == JUMP: return
        if Player.player_state == state: return

        if state == STAND:
            if Player.player_state == BEND:
                Player.coordinate_y -= 50
            Player.player_state = STAND
            #Player.width = 50
            #Player.height = 100
        elif state == JUMP:
            if Player.hit_info != HIT_Y_DOWN and Player.hit_info !=HIT_XY_DOWN:
                return
            if Player.player_state == BEND:
                Player.coordinate_y -= 50
            Player.player_state = JUMP
            #Player.width = 50
            #Player.height = 100
        elif state == BEND:
            return
            if Player.player_state != BEND:
                Player.coordinate_y += 50
            Player.player_state = BEND
            #Player.width = 50
            #Player.height = 50


    def hit_check():
        if Player.hit_info == NO_HIT:
            Player.move_x = 0
            if Player.player_state == JUMP:
                return
            Player.move_y = -5
        elif Player.hit_info == HIT_Y_UP:
            Player.move_x = 0
            Player.move_y = -5
            Player.jump_counter = 0
        elif Player.hit_info == HIT_Y_DOWN:
            if Player.player_state == JUMP:
                return
            Player.move_x = 0
            Player.move_y = 0
            Player.jump_counter = 20
        elif Player.hit_info == HIT_X:
            Player.move_x = 5
        elif Player.hit_info == HIT_XY_UP:
            Player.move_x = 5
            Player.move_y = -5
            Player.jump_counter = 0
        elif Player.hit_info == HIT_XY_DOWN:
            Player.move_x = 5
            if Player.player_state != JUMP:
                Player.move_y = 0
                Player.jump_counter = 20
        elif Player.hit_info == HIT_XY:
            if Player.player_state != JUMP:
                Player.move_y = 0
                Player.jump_counter = 20
                Player.move_x = 5
                Player.move_y = -5
                Player.jump_counter = 0

    def jump_process():
        if Player.player_state == JUMP:
            if Player.jump_counter > 0:
                Player.move_y = 5
                Player.jump_counter -= 1
            else:
                Player.move_y = 0
                Player.jump_counter = 20
                Player.player_state = STAND

    def set_hit_info(info):
        Player.hit_info = info

    def set_width_height(w, h):
        Player.width = w
        Player.height = h

    def get_x():
        return Player.coordinate_x
    def get_y():
        return Player.coordinate_y
    def get_w():
        return Player.width
    def get_h():
        return Player.height
    def get_mx():
        return Player.move_x
    def get_my():
        return Player.move_y
    def get_state():
        return Player.player_state
    def get_hit_info():
        return Player.hit_info
    def get_jump_counter():
        return Player.jump_counter

def Load_Board():
    img = cv2.imread("./skateboard.png")
    #白領域をマスク黒化

    #マスク黒領域を背景とする
    return img
    return skate_board

def Make_Field(level):
    img = cv2.imread("./block.png")
    needle = cv2.imread("./needle.png")
    texture = img[0:50, 0:50], img[0:50, 50:100], img[0:50, 100:150], img[50:100, 0:50], img[50:100, 50:100], img[50:100, 100:150], img[100:150, 0:50], img[100:150, 50:100], img[100:150, 100:150]
    field = np.zeros((F_SIZE_Y, F_SIZE_X, 3), np.uint8)
    cv2.rectangle(field, (0, 0), (F_SIZE_X, F_SIZE_Y), (200, 200, 0), -1)
    texture_field = field.copy()
    

    if level == 0:
        cv2.rectangle(field, (0, F_SIZE_Y - 50), (F_SIZE_X, F_SIZE_Y), (0, 0, 255), -1)
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
        i = 0

    cv2.rectangle(field, (F_SIZE_X - D_SIZE_X - 30, 0), (F_SIZE_X - D_SIZE_X, F_SIZE_Y), (0, 255, 0), -1)
    cv2.rectangle(texture_field, (F_SIZE_X - D_SIZE_X - 30, 0), (F_SIZE_X - D_SIZE_X, F_SIZE_Y), (0, 255, 0), -1)

    return field, texture_field

def time_manage(start, current):
    if(current-start > 50 / 1000):
        return True
    else:
        return False

def Collision_Detection(player, display):
    hit_field = [[0 for col in range((int)(D_SIZE_X / 5))] for row in range((int)(D_SIZE_Y / 5))]
    for y in range(0, (int)(D_SIZE_Y / 5)):
        for x in range(0, (int)(D_SIZE_X / 5)):
            blue, green, red = display[y * 5, x * 5, 0], display[y * 5, x * 5, 1], display[y * 5, x * 5, 2]
            if [blue, green, red] == [0, 0, 255]:
                hit_field[y][x] = BLOCK
            elif [blue, green, red] == [0, 255, 0]:
                hit_field[y][x] = CLEAR
            elif [blue, green, red] == [255, 0, 0]:
                hit_field[y][x] = NEEDLE
            else:
                hit_field[y][x] = EMPTY

    result = NO_HIT
    print("check_region")
    print("y: ", (int)((player.get_y() - player.get_h()) / 5) + 1, "x:", (int)(player.get_y() / 5) - 1, "w:", (int)(player.get_x() / 5))
    print("x:", (int)((player.get_x() - player.get_w()) / 5) + 1, "w:", (int)(player.get_x() / 5) - 1, (int)((player.get_y() - player.get_h()) / 5))
    print((int)((player.get_x() - player.get_w()) / 5) + 1, (int)(player.get_x() / 5) - 1, (int)(player.get_y() / 5))
    print("player region")
    print("y: ", (int)((player.get_y() - player.get_h()) / 5), "x:", (int)(player.get_y() / 5), "w:", (int)(player.get_x() / 5))
    print("x:", (int)((player.get_x() - player.get_w()) / 5), "w:", (int)(player.get_x() / 5), (int)((player.get_y() - player.get_h()) / 5))
    print((int)((player.get_x() - player.get_w()) / 5), (int)(player.get_x() / 5) , (int)(player.get_y() / 5))

    for y in range((int)((player.get_y() - player.get_h()) / 5) + 1, (int)(player.get_y() / 5) - 1):
        #print("1: ", hit_field[y][(int)((player.get_x() + player.get_w()) / 5)])
        if hit_field[y][(int)(player.get_x() / 5)] == BLOCK:
            #print("hit x")
            result = HIT_X
            break
        elif hit_field[y][(int)(player.get_x() / 5)] == CLEAR:
            return CLEAR
        elif hit_field[y][(int)(player.get_x() / 5)] == NEEDLE:
            return NEEDLE
        
    for x in range((int)((player.get_x() - player.get_w()) / 5) + 1, (int)(player.get_x() / 5) - 1):
        if hit_field[(int)((player.get_y() - player.get_h()) / 5)][x] == BLOCK:
            if result == HIT_X:
                #print("hit xy up")
                result = HIT_XY_UP
                break
            elif result == NO_HIT:
                result = HIT_Y_UP
                break
    for x in range((int)((player.get_x() - player.get_w()) / 5) + 1, (int)(player.get_x() / 5) - 1):
        if hit_field[(int)(player.get_y() / 5)][x] == BLOCK:
            if result == HIT_X:
                #print("hit xy down")
                result = HIT_XY_DOWN
                break
            elif result == NO_HIT:
                result = HIT_Y_DOWN
                break
            elif result == HIT_XY_UP:
                #print("hit xy")
                result = HIT_XY
                break
    return result

def Failuer_Detection(x, y, height):
    if x <= 0 or y >= F_SIZE_Y:
        return True
    else:
        return False

def Start_CountDown(Start):
    for i in range(0, 3):
        count_display = Start.copy()
        cv2.putText(count_display, str(3 - i), (250, 150), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 255), 15, cv2.LINE_AA)
        cv2.imshow("drawing", count_display)
        cv2.waitKey(1000)

def Make_Start_Manu():
    start_menu = np.zeros((D_SIZE_Y, D_SIZE_X, 3), np.uint8)
    cv2.putText(start_menu, "Select Stage", (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(start_menu, "Level. 1", (200, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(start_menu, "Level. 2", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(start_menu, "Level. 3", (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

    return start_menu

def Select_Stage(start_menu, stage_select):
    if stage_select == 0:
        cv2.putText(start_menu, "Level. 1", (200, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)
    elif stage_select == 1:
        cv2.putText(start_menu, "Level. 2", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)
    elif stage_select == 2:
        cv2.putText(start_menu, "Level. 3", (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)

    return start_menu, stage_select

def Calculate_Player_Region(n, data):
    min_x, min_y, max_w, max_h = 1000, 1000, 0, 0
    for i in range(n):
        if min_x > data[i][0]:
            min_x = data[i][0]
        if min_y > data[i][1]:
            min_y = data[i][1]
        if max_w < data[i][0] + data[i][2]:
            max_w = data[i][0] + data[i][2]
        if max_h < data[i][1] + data[i][3]:
            max_h = data[i][1] + data[i][3]

    return min_x, min_y, max_w, max_h

def Extract_Player_Region(img, mask, min_x, min_y, max_w, max_h):
    print(min_x, min_y, max_w, max_h)
    mask_d = mask[min_y:max_h + min_y, min_x:max_w+min_x]
    img_d = img[min_y:max_h+min_y, min_x:max_w+min_x]
    mask_d[mask_d < 200] = 0
    mask_d[mask_d >= 255] = 255
    mask_d = cv2.cvtColor(mask_d, cv2.COLOR_GRAY2BGR)
    player_img = np.where(mask_d == 255, img_d, mask_d)
    player_img = cv2.resize(player_img, (50, (int)(50 * max_h / max_w)))
    mask_d = cv2.resize(mask_d, (50, (int)(50 * max_h / max_w)))
    cv2.imshow("player_img", player_img)
    return mask_d, player_img

def Player_Transparent(player, mask_d, player_img, display):
    #mask = player_img.copy()
    #mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    #mask[mask < 200] = 0
    #mask[mask >= 200] = 255
    #mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #print(player.get_x() - player.get_w(), player.get_y() - player.get_h())
    result = np.where(mask_d == 255, player_img, display[player.get_y() - player.get_h():player.get_y(), player.get_x() - player.get_w():player.get_x()])
    #cv2.imshow("result", mask)
    display[player.get_y() - player.get_h():player.get_y(), player.get_x() - player.get_w():player.get_x()] = result
    return display

def After_Process(word):
    clear = np.zeros((D_SIZE_Y, D_SIZE_X, 3), np.uint8)
    cv2.putText(clear, word, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(clear, "Push W: Start Menu", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(clear, "Push X: Finish", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("drawing", clear)
    key = cv2.waitKey(0)
    if key == CV_WAITKEY_W:
        return True
    elif key == CV_WAITKEY_X:
        return False
    
    return False

def Opening(img):
    kernel = np.ones((7,7),np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening

def Display_Start_Menu(cap, back_flag):
    if back_flag == False:
        ret, background = cap.read()

    check_field_0, texture_field_0 = Make_Field(0)
    check_field_1, texture_field_1 = Make_Field(1)
    check_field_2, texture_field_2 = Make_Field(2)
    check_field, texture_field = check_field_0, texture_field_0
    stage_select = 0

    start = time.time()
    while True:
        current = time.time()
        if time_manage(start, current):
            ret, frame = cap.read()
            cv2.imshow("cameara", frame)
            #cv2.imshow("background", background)
            start_menu = Make_Start_Manu()

            key = cv2.waitKey(10)
            if key == CV_WAITKEY_W:
                if stage_select > 0:
                    stage_select -= 1
            elif key == CV_WAITKEY_X:
                if stage_select < 2:
                    stage_select += 1
            elif key == CV_WAITKEY_Z:
                if back_flag == False:
                    th = 30
                    mask = subtraction(ret, frame, background, th)
                    standard_x, standard_y, standard_w, standard_h = rinkaku(mask)
                break
            
            start_menu, stage_select = Select_Stage(start_menu, stage_select)
            
            cv2.imshow("drawing", start_menu)
            start = current

    print("Stage Level.", stage_select)

    if stage_select == 1:
        check_field, texture_field = check_field_1, texture_field_1
    elif stage_select == 2:
        check_field, texture_field = check_field_2, texture_field_2


    if back_flag == False:
        back_flag = True
        return standard_x, standard_y, standard_w, standard_h, background, check_field, texture_field, back_flag
    else:
        return check_field, texture_field

def Display_After_Menu(clear_flag):
    if clear_flag == True:
        continue_flag = After_Process("Conguratulation!!")
    else:
        continue_flag = After_Process("Stage Failuer...")

    return continue_flag

def Game_Process(standard_x, standard_y, standard_w, standard_h, background, check_field, texture_field, cap):
    #video_file='./outtest.avi'
    skate_board = Load_Board()
    
    th = 30

    stride_count = 0
    player = Player
    player.initial_coordinate()

    start_flag = False
    clear_flag = False

    start = time.time()

    while stride_count < F_SIZE_X - (F_SIZE_Y * 2):
        player_img = np.zeros((10, 10, 3), np.uint8)
        current = time.time()

        key = cv2.waitKey(1)
        if key == CV_WAITKEY_W:
            player.change_state(JUMP)
        elif key == CV_WAITKEY_X:
            player.change_state(BEND)
        elif key == CV_WAITKEY_Z:
            player.change_state(STAND)

        if time_manage(start, current):
            #frame = cap.read()[1]
            ret, frame = cap.read()

            #前景抽出処理
            mask = subtraction(ret, frame, background, th)

            #kernel = np.ones((7,7),np.uint8)
            #opening = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

            #label = cv2.connectedComponentsWithStats(cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY))
            # オブジェクト情報を項目別に抽出
            #n = label[0] - 1
            #data = np.delete(label[2], 0, 0)
            #center = np.delete(label[3], 0, 0)

            # オブジェクト情報を利用してラベリング結果を画面に表示
            #min_x, min_y, max_w, max_h = Calculate_Player_Region(n, data)            
            
            #プレイヤーの切り取り,サイズ設定
            min_x, min_y, max_w, max_h = rinkaku(mask)
            mask_d, player_img = Extract_Player_Region(frame, mask, min_x, min_y, max_w, max_h)
            print(player_img.shape[1], player_img.shape[0])
            player.set_width_height(player_img.shape[1], player_img.shape[0])

            #state = kenshutsu(mask, min_x, min_y, max_w, max_h)
            state = kenshutsu(mask, standard_x, standard_y, standard_w, standard_h)
            if state == 1:
                player.change_state(JUMP)
                print("state:JUMP")
            else:
                player.change_state(STAND)

            #if n != 0:
                #player_img = opening[min_y:max_h, min_x:max_w]
                
                #mask = cv2.cvtColor(player_img, cv2.COLOR_BGR2GRAY)
                #result = np.where(mask==255, player_img, player_img)
                #cv2.imshow("player", player_img)
                
            stride_count += 5
            #test = stage[0:D_SIZE_Y, stride_count:D_SIZE_X + stride_count]
            display = texture_field[0:D_SIZE_Y, stride_count:D_SIZE_X + stride_count].copy()
            #display = check_field[0:D_SIZE_Y, stride_count:D_SIZE_X + stride_count].copy()
            collision_dis = check_field[0:D_SIZE_Y, stride_count:D_SIZE_X + stride_count].copy()
            player.jump_process()


            check_collision = Collision_Detection(player, collision_dis)
            #print(check_collision)
            if check_collision == NO_HIT:
                player.set_hit_info(NO_HIT)
            elif check_collision == HIT_X:
                player.set_hit_info(HIT_X)
            elif check_collision == HIT_Y_UP:
                player.set_hit_info(HIT_Y_UP)
            elif check_collision == HIT_XY_UP:
                player.set_hit_info(HIT_XY_UP)
            elif check_collision == HIT_Y_DOWN:
                player.set_hit_info(HIT_Y_DOWN)
            elif check_collision == HIT_XY_DOWN:
                player.set_hit_info(HIT_XY_DOWN)
            elif check_collision == CLEAR:
                clear_flag = True
                break
            elif check_collision == NEEDLE:
                clear_flag = False
                break

            player.hit_check()
            player.set_coordinate()

            if Failuer_Detection(player.get_x() - player.get_w(), player.get_y(), player.get_h()):
                clear_flag = False
                break

            #if n != 0:    
                #人物領域外の透過処理
                #display[player.get_y() - player.get_h():player.get_y(), player.get_x() - player.get_w():player.get_x()] = result
                #print(skate_board.shape[:2])
            #player_img[player_img.shape[0] - 10:player_img.shape[0], 0:50] = skate_board
            display = Player_Transparent(player, mask_d, player_img, display)

            cv2.imshow("drawing", display)
            #cv2.imshow("skate", skate_board)

            if start_flag == False:
                Start_CountDown(display)
                start_flag = True
            if clear_flag == True:
                break

            #print("hit check", player.get_hit_info())
            start = current

    print("Finished")

    return clear_flag

def main():
    cap = cv2.VideoCapture(0)
    back_flag = False
    standard_x, standard_y, standard_w, standard_h = 0, 0, 0, 0
    while True:
        if back_flag == False:
            standard_x, standard_y, standard_w, standard_h, background, check_field, texture_field, back_flag = Display_Start_Menu(cap, back_flag)
        else:
            check_field, texture_field = Display_Start_Menu(cap, back_flag)
        clear_flag = Game_Process(standard_x, standard_y, standard_w, standard_h, background, check_field, texture_field, cap)
        continue_flag = Display_After_Menu(clear_flag)
        back_flag = True
        if continue_flag == False:
            break

if __name__ == '__main__':
    main()