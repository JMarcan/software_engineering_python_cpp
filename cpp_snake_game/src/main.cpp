#include <iostream>
#include <fstream>
#include <string>
#include "controller.h"
#include "game.h"
#include "renderer.h"

using namespace std;

float get_starting_speed();
int load_previous_record();
void store_new_record(int score);

int main() {

  //Let user choose the starting speed
  const float starting_speed = get_starting_speed();

  constexpr std::size_t kFramesPerSecond{60};
  constexpr std::size_t kMsPerFrame{1000 / kFramesPerSecond};
  constexpr std::size_t kScreenWidth{640};
  constexpr std::size_t kScreenHeight{640};
  constexpr std::size_t kGridWidth{32};
  constexpr std::size_t kGridHeight{32};

  Renderer renderer(kScreenWidth, kScreenHeight, kGridWidth, kGridHeight);
  Controller controller;

  std::cout << "Before game creation\n";
  Game game(kGridWidth, kGridHeight);
  std::cout << "Before game run\n";
  game.Run(controller, renderer, kMsPerFrame, starting_speed);

  int const previous_best_score = load_previous_record();
  int const game_score = game.GetScore();

  std::cout << "Game has terminated successfully!\n";
  std::cout << "Your score: " << game_score << "\n";
  std::cout << "Record so far: " << previous_best_score << "\n";

  //Store the new record
  if (game_score > previous_best_score) {
    std::cout << "Wow! You set the new record!\n";
    store_new_record(game_score);
  }

  return 0;
}

float get_starting_speed(){
  string buffer;
  cout << "Choose the starting speed: (default: 0.1)\n";
  getline(cin, buffer);
  return stof(buffer);
}

int load_previous_record() {
  string buffer;
  ifstream file("best_score.txt");
  if (file) {
    file >> buffer;
    file.close();
    return stoi(buffer);
  }
  
  return 0;
}

void store_new_record(const int score) {
  ofstream file("best_score.txt");
  file << score;
  file.close();
  return;
}