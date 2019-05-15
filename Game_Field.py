import cv2
import numpy as np

import time

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
        Player.coordinate_x = (int)(D_SIZE_X / 2) - Player.width
        Player.coordinate_y = 250 - Player.height
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
            Player.width = 50
            Player.height = 100
        elif state == JUMP:
            if Player.hit_info != HIT_Y_DOWN and Player.hit_info !=HIT_XY_DOWN:
                return
            if Player.player_state == BEND:
                Player.coordinate_y -= 50
            Player.player_state = JUMP
            Player.width = 50
            Player.height = 100
        elif state == BEND:
            if Player.player_state != BEND:
                Player.coordinate_y += 50
            Player.player_state = BEND
            Player.width = 50
            Player.height = 50


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
            Player.move_y -= 5
            Player.jump_counter = 0
        elif Player.hit_info == HIT_XY_DOWN:
            Player.move_x = 5
            if Player.player_state != JUMP:
                Player.move_y = 0
                Player.jump_counter = 20

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

def Make_Field(level):
    field = np.zeros((F_SIZE_Y, F_SIZE_X, 3), np.uint8)
    cv2.rectangle(field, (0, 0), (F_SIZE_X, F_SIZE_Y), (200, 200, 0), -1)
    if level == 0:
        cv2.rectangle(field, (0, F_SIZE_Y - 50), (F_SIZE_X, F_SIZE_Y), (0, 0, 255), -1)
    elif level == 1:
        cv2.rectangle(field, (0, F_SIZE_Y - 50), (F_SIZE_X, F_SIZE_Y), (0, 0, 255), -1)
        cv2.rectangle(field, (0, 0), (1000, F_SIZE_Y - 250), (0, 0, 255), -1)
        cv2.rectangle(field, (300, 0), (800, F_SIZE_Y - 200), (0, 0, 255), -1)
        cv2.rectangle(field, (1300, F_SIZE_Y - 120), (2000, F_SIZE_Y), (0, 0, 255), -1)
        cv2.rectangle(field, (1600, 0), (2000, 100), (0, 0, 255), -1)
        cv2.rectangle(field, (200, 350), (300, 450), (0, 0, 255), -1)
    elif level == 2:
        i = 0

    cv2.rectangle(field, (F_SIZE_X - D_SIZE_X, 0), (F_SIZE_X - D_SIZE_X + 30, F_SIZE_Y), (0, 255, 0), -1)

    return field

def time_manage(start, current):
    if(current-start > 50 / 1000):
        return True
    else:
        return False

def Collision_Detection(player, hit_field):
    result = NO_HIT
    for y in range((int)(player.get_y() / 5) , (int)((player.get_y() + player.get_h()) / 5)):
        print("1: ", hit_field[y][(int)((player.get_x() + player.get_w()) / 5)])
        if hit_field[y][(int)((player.get_x() + player.get_w()) / 5)] == BLOCK:
            result = HIT_X
        elif hit_field[y][(int)((player.get_x() + player.get_w()) / 5)] == CLEAR:
            return CLEAR
    for x in range((int)(player.get_x() / 5), (int)((player.get_x() + player.get_w()) / 5)):
        if hit_field[(int)(player.get_y() / 5)][x] == BLOCK:
            if result == HIT_X:
                result = HIT_XY_UP
            elif result != HIT_XY_UP:
                result = HIT_Y_UP
    for x in range((int)(player.get_x() / 5), (int)((player.get_x() + player.get_w()) / 5)):
        if hit_field[(int)((player.get_y() + player.get_h()) / 5)][x] == BLOCK:
            if result == HIT_X:
                result = HIT_XY_DOWN
            elif result != HIT_XY_DOWN:
                result = HIT_Y_DOWN
    return result

def Failuer_Detection(x, y, height):
    if x <= 0 or y + height >= F_SIZE_Y:
        return True
    else:
        return False

def Start_CountDown(Start):
    for i in range(0, 3):
        count_display = Start.copy()
        cv2.putText(count_display, "test", (250, 150), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 15, cv2.LINE_AA)
        cv2.imshow("drawing", count_display)
        cv2.waitKey(1000)

def main():
    stage_0 = Make_Field(0)
    stage_1 = Make_Field(1)
    stage_2 = Make_Field(2)
    img = stage_0
    
    stride_count = 0
    player_x = 0
    player_y = 0

    start = time.time()

    player = Player
    player.initial_coordinate()

    start_flag = False
    clear_flag = False
    stage_select = 0

    while True:
        current = time.time()
        if time_manage(start, current):
            start_menu = np.zeros((D_SIZE_Y, D_SIZE_X, 3), np.uint8)
            cv2.putText(start_menu, "Select Stage", (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
            cv2.putText(start_menu, "Level. 1", (200, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(start_menu, "Level. 2", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(start_menu, "Level. 3", (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

            key = cv2.waitKey(10)
            if key == CV_WAITKEY_W:
                if stage_select > 0:
                    stage_select -= 1
            elif key == CV_WAITKEY_X:
                if stage_select < 2:
                    stage_select += 1
            elif key == CV_WAITKEY_Z:
                break

            if stage_select == 0:
                cv2.putText(start_menu, "Level. 1", (200, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)
            elif stage_select == 1:
                cv2.putText(start_menu, "Level. 2", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)
            elif stage_select == 2:
                cv2.putText(start_menu, "Level. 3", (200, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow("drawing", start_menu)
            start = current

    print("Stage Level.", stage_select)

    if stage_select == 1:
        img = stage_1
    elif stage_select == 2:
        img = stage_2

    while stride_count < F_SIZE_X - (F_SIZE_Y * 2):
        current = time.time()

        key = cv2.waitKey(1)
        if key == CV_WAITKEY_W:
            player.change_state(JUMP)
        elif key == CV_WAITKEY_X:
            player.change_state(BEND)
        elif key == CV_WAITKEY_Z:
            player.change_state(STAND)

        if time_manage(start, current):
            stride_count += 5
            test = img[0:D_SIZE_Y, stride_count:D_SIZE_X + stride_count]
            display = test.copy()
            player.jump_process()

            #hit_field = [(int)(D_SIZE_Y / 5)][(int)(D_SIZE_X / 5)]
            hit_field = [[0 for col in range((int)(D_SIZE_X / 5))] for row in range((int)(D_SIZE_Y / 5))]
            for y in range(0, (int)(D_SIZE_Y / 5)):
                for x in range(0, (int)(D_SIZE_X / 5)):
                    blue, green, red = display[y * 5, x * 5, 0], display[y * 5, x * 5, 1], display[y * 5, x * 5, 2]
                    if [blue, green, red] == [0, 0, 255]:
                        hit_field[y][x] = BLOCK
                    elif [blue, green, red] == [0, 255, 0]:
                        hit_field[y][x] = CLEAR
                    else:
                        hit_field[y][x] = EMPTY

            check_collision = Collision_Detection(player, hit_field)
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

            player.hit_check()
            player.set_coordinate()

            if Failuer_Detection(player.get_x(), player.get_y(), player.get_h()):
                clear_flag = False
                break

            cv2.rectangle(display, (player.get_x(), player.get_y()), 
                          (player.get_x() + player.get_w(), player.get_y() + player.get_h()), (255, 255, 255), -1)
            cv2.imshow("drawing", display)

            if start_flag == False:
                Start_CountDown(display)
                start_flag = True
            if clear_flag == True:
                break

            print("hit check", player.get_hit_info())
            start = current

    if clear_flag == True:
        clear = np.zeros((D_SIZE_Y, D_SIZE_X, 3), np.uint8)
        cv2.putText(clear, "Conguratulation!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(clear, "Push W: Start Menu", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(clear, "Push X: Finish", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("drawing", clear)

        key = cv2.waitKey(0)
        if key == CV_WAITKEY_W:
            return 0
        elif key == CV_WAITKEY_X:
            return 0
    else:
        failuer = np.zeros((D_SIZE_Y, D_SIZE_X, 3), np.uint8)
        cv2.putText(failuer, "Stage Filuer...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(failuer, "Push W: Start Menu", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(failuer, "Push X: Finish", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("drawing", failuer)

        key = cv2.waitKey(0)
        if key == CV_WAITKEY_W:
            return 0
        elif key == CV_WAITKEY_X:
            return 0
    

    print("Finished")

    return 0

if __name__ == '__main__':
    main()