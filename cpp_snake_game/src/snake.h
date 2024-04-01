#ifndef SNAKE_H
#define SNAKE_H

#include <vector>
#include "SDL.h"

class Snake {
 public:
  enum class Direction { kUp, kDown, kLeft, kRight };
  Snake(int const grid_width, int const grid_height, float const start_pos_x, float const start_pos_y) {
	  this->grid_width = grid_width;
    this->grid_height = grid_height;

    head_x = start_pos_x;
    head_y = start_pos_y;

    head = SDL_Point{static_cast<int>(head_x), static_cast<int>(head_y)};
  }

  void Update();

  void GrowBody();
  bool SnakeCell(int x, int y);
  int GridWidth() const;
  int GridHeight() const;

  Direction direction = Direction::kUp;

  float speed{0.1f};
  int size{1};
  bool alive{true};
  SDL_Point head;
  float head_x;
  float head_y;
  std::vector<SDL_Point> body;

 private:
  int grid_width;
  int grid_height;
  void UpdateHead();
  void UpdateBody(SDL_Point &prev_head_cell);
  bool growing{false};
  
};

#endif