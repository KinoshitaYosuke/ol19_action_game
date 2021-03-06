#include <iostream>
#include <opencv2/opencv.hpp>
#include <time.h>

#include <random>

//ステージの大きさ
#define F_SIZE_X 2500
#define F_SIZE_Y 300
#define D_SIZE_X 600
#define D_SIZE_Y 300

//ステージギミック
#define EMPTY 0
#define BLOCK 1
#define NEEDLE 2
#define COIN 3
#define CLEAR 100

//当たり判定
#define NO_HIT 0
#define HIT_Y_DOWN 1
#define HIT_Y_UP 2
#define HIT_X 3
#define HIT_XY_DOWN 4
#define HIT_XY_UP 5

//プレイヤー状態
#define STAND 0
#define JUMP 1
#define BEND 2

//キー入力
#define CV_WAITKEY_X 120
#define CV_WAITKEY_W 119
#define CV_WAITKEY_Z 122
#define CV_WAITKEY_ENTER 13
#define CV_WAITKEY_ESC 27
#define CV_WAITKEY_SPACE 32
#define CV_WAITKEY_TAB 9

//プレイヤー情報
class Player {
private:
	int player_state;
	int coordinate_x;
	int coordinate_y;
	int width;
	int height;
	int move_x;
	int move_y;
	int jump_counter;
	int hit_info;

public:
	void initial_coordinate();
	void set_coordinate();
	void change_state(int state);
	void hit_check();
	void jump_process();
	void set_hit_info(int info);

	int get_x();
	int get_y();
	int get_w();
	int get_h();
	int get_mx();
	int get_my();
	int get_state();
	int get_hit_info();
	int get_jump_counter();

};

void Player::initial_coordinate() {
	player_state = STAND;
	width = 50;
	height = 100;
	move_x = 0;
	move_y = 0;
	coordinate_x = int(D_SIZE_X / 2) - width;
	coordinate_y = 250 - height;
	jump_counter = 20;

	return;
}

void Player::set_coordinate() {
	coordinate_x -= move_x;
	coordinate_y -= move_y;

	return;
}

void Player::change_state(int state) {
	if(player_state == JUMP)
		return;
	if (player_state == state)
		return;

	switch (state) {
	case STAND:
		if (player_state == BEND)
			coordinate_y -= 50;
		player_state = STAND;
		width = 50;
		height = 100;
		break;
	case JUMP:
		if (player_state == BEND)
			coordinate_y -= 50;
		player_state = JUMP;
		width = 50;
		height = 100;
		break;
	case BEND:
		if (player_state != BEND)
			coordinate_y += 50;
		player_state = BEND;
		width = 50;
		height = 50;
		break;
	}

	return;
}

void Player::set_hit_info(int info) {
	hit_info = info;
	return;
}

void Player::hit_check() {
	switch (hit_info) {
	case NO_HIT:
		move_x = 0;
		if (player_state == JUMP)
			return;
		move_y = -5;
		break;
	case HIT_Y_UP:
		move_x = 0;
		move_y = -5;
		jump_counter = 0;
		break;
	case HIT_Y_DOWN:
		if (player_state == JUMP)
			return;
		move_x = 0;
		move_y = 0;
		jump_counter = 20;
		break;
	case HIT_X:
		move_x = 5;
		break;
	case HIT_XY_UP:
		move_x = 5;
		move_y = -5;
		jump_counter = 0;
		break;
	case HIT_XY_DOWN:
		move_x = 5;

		if (player_state != JUMP) {
			move_y = 0;
			jump_counter = 20;
		}
		//player_state = STAND;
		break;
	}
	return;
}

void Player::jump_process() {
	if (player_state == JUMP) {
		if (jump_counter > 0) {
			move_y = 5;
			jump_counter -= 1;
		}
		//else if (jump_counter > -20) {
		//	move_y = -5;
		//	jump_counter -= 1;
		//}
		else {
			move_y = 0;
			jump_counter = 20;
			player_state = STAND;
		}
	}
	return;
}

int Player::get_x() {
	return coordinate_x;
}
int Player::get_y() {
	return coordinate_y;
}
int Player::get_w() {
	return width;
}
int Player::get_h() {
	return height;
}
int Player::get_mx() {
	return move_x;
}
int Player::get_my() {
	return move_y;
}
int Player::get_state() {
	return player_state;
}
int Player::get_hit_info() {
	return hit_info;
}
int Player::get_jump_counter() {
	return jump_counter;
}

//ステージ生成
cv::Mat Make_Field(int level) {
	cv::Mat field = cv::Mat::zeros(F_SIZE_Y, F_SIZE_X, CV_8UC3);
	/*
	for (int x = 0; x <= F_SIZE_X - 60; x += 60) {
		std::random_device rand;
		std::mt19937 mt(rand());
		std::uniform_int_distribution<> rand255(0, 255);
		std::cout << x << std::endl;
		cv::rectangle(field, cv::Point(x, 0), cv::Point(x + 60, F_SIZE_Y), cv::Scalar(rand255(mt), rand255(mt), rand255(mt)), -1, CV_AA);
	}
	*/
	cv::rectangle(field, cv::Point(0, 0), cv::Point(F_SIZE_X, F_SIZE_Y), cv::Scalar(200, 200, 0), -1, CV_AA);

	if (level == 0) {
		cv::rectangle(field, cv::Point(0, F_SIZE_Y - 50), cv::Point(F_SIZE_X, F_SIZE_Y), cv::Scalar(0, 0, 255), -1, CV_AA);
	}
	else if (level == 1) {
		cv::rectangle(field, cv::Point(0, F_SIZE_Y - 50), cv::Point(F_SIZE_X, F_SIZE_Y), cv::Scalar(0, 0, 255), -1, CV_AA);
		cv::rectangle(field, cv::Point(0, 0), cv::Point(1000, F_SIZE_Y - 250), cv::Scalar(0, 0, 255), -1, CV_AA);
		cv::rectangle(field, cv::Point(300, 0), cv::Point(800, F_SIZE_Y - 200), cv::Scalar(0, 0, 255), -1, CV_AA);
		cv::rectangle(field, cv::Point(1300, F_SIZE_Y - 120), cv::Point(2000, F_SIZE_Y), cv::Scalar(0, 0, 255), -1, CV_AA);
		cv::rectangle(field, cv::Point(1600, 0), cv::Point(2000, F_SIZE_Y - 200), cv::Scalar(0, 0, 255), -1, CV_AA);
		cv::rectangle(field, cv::Point(200, 200), cv::Point(300, 300), cv::Scalar(0, 200, 0), 5, 8);
		cv::rectangle(field, cv::Point(200, 350), cv::Point(300, 450), cv::Scalar(200, 0, 0), -1, CV_AA);


	}
	else if (level == 2) {

	}
	cv::rectangle(field, cv::Point(F_SIZE_X - D_SIZE_X, 0), cv::Point(F_SIZE_X - D_SIZE_X + 30, F_SIZE_Y), cv::Scalar(0, 255, 0), -1, CV_AA);

	return field;
}

bool time_manage(clock_t start, clock_t current) {
	if (current - start > 50) return true;
	else return false;
}

//当たり判定
int Collision_Detection(Player player, int hit_field[60][120]) {
	int result = NO_HIT;
	for (int y = player.get_y() / 5; y < (player.get_y() + player.get_h()) / 5; y++) {
		if (hit_field[y][int((player.get_x() + player.get_w()) / 5)] == BLOCK) {
			//std::cout << y << ", " << int((player.get_x() + player.get_w()) / 5) << std::endl;
			result = HIT_X;
		}
		else if (hit_field[y][int((player.get_x() + player.get_w()) / 5 - 1)] == CLEAR) {
			return CLEAR;
		}
	}
	for (int x = player.get_x() / 5; x < (player.get_x() + player.get_w()) / 5; x++) {
		if (hit_field[player.get_y() / 5][x] == BLOCK) {
			if (result == HIT_X)
				result = HIT_XY_UP;
			else if (result != HIT_XY_UP)
				result = HIT_Y_UP;
		}
	}
	for (int x = player.get_x() / 5; x < (player.get_x() + player.get_w()) / 5; x++) {
		if (hit_field[(player.get_y() + player.get_h()) / 5][x] == BLOCK) {
			if (result == HIT_X)
				result = HIT_XY_DOWN;
			else if (result != HIT_XY_DOWN)
				result = HIT_Y_DOWN;
		}
	}
	return result;

}

bool Failuer_Detection(int x, int y, int height) {
	if (x <= 0 || (y+height) >= F_SIZE_Y) return true;
	else return false;
}

void Start_CountDown(cv::Mat Start) {
	for (int i = 3; i > 0; i--) {
		cv::Mat count_display = Start.clone();
		cv::putText(count_display, std::to_string(i), cv::Point(250, 150), cv::FONT_HERSHEY_SIMPLEX, 5, cv::Scalar(0, 255, 255), 15, CV_AA);
		cv::imshow("drawing", count_display);
		cv::waitKey(1000);
	}
}

int main(int argc, char* argv[]){
	cv::Mat stage_0 = Make_Field(0);
	cv::Mat stage_1 = Make_Field(1);
	cv::Mat stage_2 = Make_Field(2);

	cv::Mat img = stage_0;

	int stride_count = 0;
	int player_x = 0;
	int player_y = 0;
	clock_t start = clock();

	Player player;
	player.initial_coordinate();

	bool flag = false;

	bool clear_flag = false;
	int stage_select = 0;
	//スタート画面
	while (true) {
		clock_t current = clock();
		if (time_manage(start, current)) {
			cv::Mat start_menu = cv::Mat::zeros(D_SIZE_Y, D_SIZE_X, CV_8UC3);

			cv::putText(start_menu, "Select Stage", cv::Point(150, 50), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 3, CV_AA);

			cv::putText(start_menu, "Level. 1", cv::Point(200, 150), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 2, CV_AA);
			cv::putText(start_menu, "Level. 2", cv::Point(200, 200), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 2, CV_AA);
			cv::putText(start_menu, "Level. 3", cv::Point(200, 250), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 2, CV_AA);
			
			int key = cv::waitKey(10);
			if (key == CV_WAITKEY_W) {
				if (stage_select > 0)
					stage_select -= 1;
			}
			else if (key == CV_WAITKEY_X) {
				if (stage_select < 2)
					stage_select += 1;
			}
			else if (key == CV_WAITKEY_Z) {
				break;
			}

			switch (stage_select) {
			case 0:
				cv::putText(start_menu, "Level. 1", cv::Point(200, 150), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(0, 0, 255), 3, CV_AA);
				break;
			case 1:
				cv::putText(start_menu, "Level. 2", cv::Point(200, 200), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(0, 0, 255), 3, CV_AA);
				break;
			case 2:
				cv::putText(start_menu, "Level. 3", cv::Point(200, 250), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(0, 0, 255), 3, CV_AA);
				break;
			}

			cv::namedWindow("drawing", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
			cv::imshow("drawing", start_menu);
			start = current;
		}

	}
	std::cout << "Select Stage: Level." << stage_select << std::endl;

	switch (stage_select) {
	case 1:
		img = stage_1;
		break;
	case 2:
		img = stage_2;
		break;
	}

	//ゲーム進行
	while (stride_count < F_SIZE_X - (F_SIZE_Y * 2)) {
		clock_t current = clock();
		
		int key = cv::waitKey(1);
		switch (key) {
		case CV_WAITKEY_W:
			player.change_state(JUMP);
			break;
		case CV_WAITKEY_X:
			player.change_state(BEND);
			break;
		case CV_WAITKEY_Z:
			player.change_state(STAND);
			break;
		}
		
		if (time_manage(start, current)) {

			stride_count += 5;
			cv::Mat test(img, cv::Rect(stride_count, 0, D_SIZE_X, D_SIZE_Y));
			cv::Mat display = test.clone();

			player.jump_process();

			int hit_field[int(D_SIZE_Y / 5)][int(D_SIZE_X / 5)];
			for (int y = 0; y < int(D_SIZE_Y / 5); y++) {
				for (int x = 0;x < int(D_SIZE_X / 5); x++) {
					if (display.at<cv::Vec3b>(y * 5, x * 5) == cv::Vec3b(0, 0, 255)) {
						hit_field[y][x] = BLOCK;
					}
					else if (display.at<cv::Vec3b>(y * 5, x * 5) == cv::Vec3b(0, 255, 0)) {
						hit_field[y][x] = CLEAR;
					}
					else {
						hit_field[y][x] = EMPTY;
					}
				}
			}

			int check_collision = Collision_Detection(player, hit_field);
			switch (check_collision) {
			case NO_HIT:
				player.set_hit_info(NO_HIT);
				break;
			case HIT_X:
				player.set_hit_info(HIT_X);
				break;
			case HIT_Y_UP:
				player.set_hit_info(HIT_Y_UP);
				break;
			case HIT_XY_UP:
				player.set_hit_info(HIT_XY_UP);
				break;
			case HIT_Y_DOWN:
				player.set_hit_info(HIT_Y_DOWN);
				break;
			case HIT_XY_DOWN:
				player.set_hit_info(HIT_XY_DOWN);
				break;
			case CLEAR:
				clear_flag = true;
			}

			std::cout << player.get_hit_info() << std::endl;

			player.hit_check();
			player.set_coordinate();

			if (Failuer_Detection(player.get_x(), player.get_y(), player.get_h())) {
				clear_flag = false;
				break;
			}

			cv::rectangle(display, cv::Point(player.get_x(), player.get_y()), 
				cv::Point(player.get_x() + player.get_w(), player.get_y() + player.get_h()), cv::Scalar(255, 255, 255), -1, CV_AA);
			cv::imshow("drawing", display);



			if (flag == false) {

				Start_CountDown(display);
				flag = true;
			}
			if (clear_flag == true) {
				break;
			}
			start = current;
		}
	}

	//クリア，失敗判定
	if (clear_flag == true) {
		cv::Mat clear = cv::Mat::zeros(D_SIZE_Y, D_SIZE_X, CV_8UC3);

		cv::putText(clear, "Conguratulation!!", cv::Point(50, 50), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 3, CV_AA);

		cv::putText(clear, "Push W: Start Menu", cv::Point(50, 150), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 2, CV_AA);
		cv::putText(clear, "Push X: Finish", cv::Point(50, 200), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 2, CV_AA);


		cv::namedWindow("drawing", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
		cv::imshow("drawing", clear);

		int key = cv::waitKey(0);
		if (key == CV_WAITKEY_W) {
			return 0;
		}
		else if (key == CV_WAITKEY_X) {
			return 0;
		}

	}
	else {
		cv::Mat failuer = cv::Mat::zeros(D_SIZE_Y, D_SIZE_X, CV_8UC3);

		cv::putText(failuer, "Stage Failuer...", cv::Point(50, 50), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 3, CV_AA);

		cv::putText(failuer, "Push W: Start Menu", cv::Point(50, 150), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 2, CV_AA);
		cv::putText(failuer, "Push X: Finish", cv::Point(50, 200), cv::FONT_HERSHEY_SIMPLEX, 1.5, cv::Scalar(255, 255, 255), 2, CV_AA);


		cv::namedWindow("drawing", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
		cv::imshow("drawing", failuer);

		int key = cv::waitKey(0);
		if (key == CV_WAITKEY_W) {
			return 0;
		}
		else if (key == CV_WAITKEY_X) {
			return 0;
		}
	}

	std::cout << "Finished" << std::endl;

	return 0;
}