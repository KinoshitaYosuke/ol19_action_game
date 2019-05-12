#include <iostream>
#include <opencv2/opencv.hpp>
#include <time.h>

#include <random>

//ステージの大きさ
#define F_SIZE_X 2000
#define F_SIZE_Y 300
#define D_SIZE_X 600
#define D_SIZE_Y 300

//ステージギミック
#define EMPTY 0
#define BLOCK 1
#define NEEDLE 2
#define COIN 3

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
		if (hit_info != HIT_Y_DOWN && hit_info != HIT_XY_DOWN)
			break;
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
cv::Mat Make_Field() {
	cv::Mat field = cv::Mat::zeros(F_SIZE_Y, F_SIZE_X, CV_8UC3);

	

	for (int x = 0; x <= F_SIZE_X-60; x += 60) {
		std::random_device rand;
		std::mt19937 mt(rand());
		std::uniform_int_distribution<> rand255(0, 255);
		std::cout << x << std::endl;
		cv::rectangle(field, cv::Point(x, 0), cv::Point(x+30, F_SIZE_Y), cv::Scalar(rand255(mt), rand255(mt), rand255(mt)), -1, CV_AA);
	}

	//cv::rectangle(field, cv::Point(0, 0), cv::Point(F_SIZE_X, F_SIZE_Y), cv::Scalar(255, 50, 50), -1, CV_AA);

	cv::rectangle(field, cv::Point(0, F_SIZE_Y - 50), cv::Point(F_SIZE_X, F_SIZE_Y), cv::Scalar(0, 0, 255), -1, CV_AA);
	cv::rectangle(field, cv::Point(500, 0), cv::Point(1000, F_SIZE_Y - 250), cv::Scalar(0, 0, 255), -1, CV_AA);
	cv::rectangle(field, cv::Point(800, 0), cv::Point(1000, F_SIZE_Y - 200), cv::Scalar(0, 0, 255), -1, CV_AA);
	cv::rectangle(field, cv::Point(1300, F_SIZE_Y - 120), cv::Point(2000, F_SIZE_Y), cv::Scalar(0, 0, 255), -1, CV_AA);


	cv::rectangle(field, cv::Point(200, 200), cv::Point(300, 300), cv::Scalar(0, 200, 0), 5, 8);
	cv::rectangle(field, cv::Point(200, 350), cv::Point(300, 450), cv::Scalar(200, 0, 0), -1, CV_AA);

	return field;
}

bool time_manage(clock_t start, clock_t current) {
	if (current - start > 50) return true;
	else return false;
}

//当たり判定
int Collision_Detection(int player[], int block[]) {
	//IoU計算

	return 0;

}


int main(int argc, char* argv[]){
	cv::Mat img = Make_Field();

	int stride_count = 0;
	int player_x = 0;
	int player_y = 0;
	clock_t start = clock();

	Player player;
	player.initial_coordinate();

	bool flag = false;

	//ステージ描画
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
			//std::cout << player.get_x() << std::endl;
			//std::cout << player.get_y() << std::endl;
			//std::cout << player.get_w() << std::endl;
			//std::cout << player.get_h() << std::endl;
			//std::cout <<  player.get_hit_info()<<", " << player.get_state()<< ", " << player.get_w() << ", " << player.get_h()  << std::endl;

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
					else {
						hit_field[y][x] = EMPTY;
					}
				}
				//std::cout << std::endl;
			}

			//int check_collision = Collision_Detection();
			player.set_hit_info(NO_HIT);
			for (int y = player.get_y() / 5; y < (player.get_y() + player.get_h()) / 5; y++) {
				if (hit_field[y][int((player.get_x() + player.get_w()) / 5)] == BLOCK) {
					//std::cout << y << ", " << int((player.get_x() + player.get_w()) / 5) << std::endl;
					player.set_hit_info(HIT_X);
				}
			}
			for (int x = player.get_x() / 5; x < (player.get_x() + player.get_w()) / 5; x++) {
				if (hit_field[player.get_y() / 5][x] == BLOCK) {
					if (player.get_hit_info() == HIT_X)
						player.set_hit_info(HIT_XY_UP);
					else if(player.get_hit_info() != HIT_XY_UP)
						player.set_hit_info(HIT_Y_UP);
				}
			}
			for (int x = player.get_x() / 5; x < (player.get_x() + player.get_w()) / 5; x++) {
				if (hit_field[(player.get_y() + player.get_h()) / 5][x] == BLOCK) {
					if (player.get_hit_info() == HIT_X)
						player.set_hit_info(HIT_XY_DOWN);
					else if(player.get_hit_info() != HIT_XY_DOWN)
						player.set_hit_info(HIT_Y_DOWN);
				}
			}
			std::cout << player.get_hit_info() << std::endl;

			player.hit_check();
			player.set_coordinate();

			cv::rectangle(display, cv::Point(player.get_x(), player.get_y()), 
				cv::Point(player.get_x() + player.get_w(), player.get_y() + player.get_h()), cv::Scalar(255, 255, 255), -1, CV_AA);
			cv::imshow("drawing", display);



			if (flag == false) {
				cv::waitKey(0);
				flag = true;
			}
			/*
			for (int y = 0; y < int(D_SIZE_Y / 5); y++) {
				for (int x = 0; x < int(D_SIZE_X / 5); x++) {
					if (display.at<cv::Vec3b>(y * 5, x * 5) == cv::Vec3b(0, 0, 255)) {
						std::cout << "#";
					}
					else if (display.at<cv::Vec3b>(y * 5, x * 5) == cv::Vec3b(255, 255, 255))
						std::cout << "O";
					else {
						std::cout << " ";
					}
				}
				std::cout << std::endl;
			}
			*/
			//cv::waitKey(5);
			start = current;

		}
		

	}

	std::cout << "Finished" << std::endl;

	return 0;
}