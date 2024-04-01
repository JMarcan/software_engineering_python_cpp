#include <vector>
#include <cmath>
#include "snake.h"

void Snake::Update() {
  SDL_Point prev_cell{
      static_cast<int>(head_x),
      static_cast<int>(
          head_y)};  // We first capture the previous head's cell before updating.
  UpdateHead();

  // Update all of the body vector items if the snake head has moved to a new
  // cell.
  if (head.x != prev_cell.x || head.y != prev_cell.y) {
    UpdateBody(prev_cell);
  }
}

void Snake::UpdateHead() {
  switch (direction) {
    case Direction::kUp:
      head_y -= speed;
      break;

    case Direction::kDown:
      head_y += speed;
      break;

    case Direction::kLeft:
      head_x -= speed;
      break;

    case Direction::kRight:
      head_x += speed;
      break;
  }

  // Wrap the Snake around to the beginning if going off of the screen.
  head_x = fmod(head_x + grid_width, grid_width);
  head_y = fmod(head_y + grid_height, grid_height);
  head.x = static_cast<int>(head_x);
  head.y = static_cast<int>(head_y);
}

void Snake::UpdateBody(SDL_Point &prev_head_cell) {
  // Add previous head location to vector
  body.push_back(prev_head_cell);

  if (!growing) {
    // Remove the tail from the vector.
    body.erase(body.begin());
  } else {
    growing = false;
    size++;
  }
}

void Snake::GrowBody() { growing = true; }

bool Snake::SnakeCell(int x, int y) {
  if (x == head.x && y == head.y) {
    return true;
  }
  for (auto const &item : body) {
    if (x == item.x && y == item.y) {
      return true;
    }
  }
  return false;
}

int Snake::GridWidth() const { return grid_width; }
int Snake::GridHeight() const { return grid_height; }