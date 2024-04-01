#ifndef GAME_H
#define GAME_H

#include <random>
#include "SDL.h"
#include "controller.h"
#include "renderer.h"
#include "snake.h"
#include "snake_ai.h"
#include "obstacles.h"

class Game {
 public:
  Game(std::size_t grid_width, std::size_t grid_height);
  void Run(Controller const &controller, Renderer &renderer,
           std::size_t target_frame_duration, float starting_speed);
  int GetScore() const;
  int GetSize() const;

 private:
  Snake snake_user;
  Snake snake_ai;
  std::vector<StaticObstacle> static_obstacles;
  std::vector<DynamicObstacle> dynamic_obstacles;
  SDL_Point food;

  std::random_device device;
  std::mt19937 generator;
  std::uniform_int_distribution<int> random_w;
  std::uniform_int_distribution<int> random_h;

  int score{0};

  void PlaceFood();
  void EatFood(Snake &snake);
  void PlaceStaticObstacle();
  void Update();
};

#endif