#include "game.h"
#include <iostream>
#include "SDL.h"

Game::Game(std::size_t grid_width, std::size_t grid_height)
    : snake(grid_width, grid_height),
      engine(dev()),
      random_w(0, static_cast<int>(grid_width - 1)),
      random_h(0, static_cast<int>(grid_height - 1)) {
  PlaceStaticObstacle();
  PlaceStaticObstacle();
  PlaceStaticObstacle();
  PlaceDynamicObstacle();
  PlaceFood();
}

void Game::Run(Controller const &controller, Renderer &renderer,
               std::size_t target_frame_duration, float starting_speed) {
  Uint32 title_timestamp = SDL_GetTicks();
  Uint32 frame_start;
  Uint32 frame_end;
  Uint32 frame_duration;
  int frame_count = 0;
  bool running = true;
  snake.speed = starting_speed;

  while (running) {
    frame_start = SDL_GetTicks();

    // Input, Update, Render - the main game loop.
    controller.HandleInput(running, snake);
    Update();
    renderer.Render(snake, food, static_obstacles, dynamic_obstacle);

    frame_end = SDL_GetTicks();

    // Keep track of how long each loop through the input/update/render cycle
    // takes.
    frame_count++;
    frame_duration = frame_end - frame_start;

    // After every second, update the window title.
    if (frame_end - title_timestamp >= 1000) {
      renderer.UpdateWindowTitle(score, frame_count);
      frame_count = 0;
      title_timestamp = frame_end;
    }

    // If the time for this frame is too small (i.e. frame_duration is
    // smaller than the target ms_per_frame), delay the loop to
    // achieve the correct frame rate.
    if (frame_duration < target_frame_duration) {
      SDL_Delay(target_frame_duration - frame_duration);
    }
  }
}

void Game::PlaceFood() {
  int x, y;
  while (true) {
    x = random_w(engine);
    y = random_h(engine);
    // Check that the location is not occupied by a snake before placing food
    if (snake.SnakeCell(x, y)) 
      continue;

    // Check that the location is not occupied by an obstacle before placing food
    for (auto const &item : static_obstacles) {
      if (x == item.x && y == item.y) 
        continue;
      }

    food.x = x;
    food.y = y;
    return;
  }
}

void Game::PlaceStaticObstacle() {
  int x, y;
  while (true) {
    x = random_w(engine);
    y = random_w(engine);

    // Check that the location is not occupied by a snake before placing a static obstacle
    if (snake.SnakeCell(x, y))
      continue;
    
    SDL_Point obstacle = {x, y};
    static_obstacles.push_back(obstacle);
    return;
  }
}

void Game::PlaceDynamicObstacle() {
  int x, y;
  while (true) {
    x = random_w(engine);
    y = random_w(engine);

    // Check that the location is not occupied by a snake before placing a static obstacle
    if (snake.SnakeCell(x, y))
      continue;

    // Check that the location is not occupied by a static obstacle before placing a dynamic obstacle
    for (auto const &item : static_obstacles) {
      if (x == item.x && y == item.y) 
        continue;
    } 

    dynamic_obstacle  = SDL_Point{x, y};
    return;
  }

}

void Game::Update() {
  if (!snake.alive) return;

  // Update dynamic obstacle position
  dynamic_obstacle_x += snake.speed;
  // Wrap the dynamic obstacle around to the beginning if going off of the screen.
  dynamic_obstacle.x = fmod(dynamic_obstacle_x, snake.grid_width);

  // Uddate snake position
  snake.Update();

  int snake_new_x = static_cast<int>(snake.head_x);
  int snake_new_y = static_cast<int>(snake.head_y);

  // Check if the snake has hit one of static obstacles
  for (auto const &item : static_obstacles) {
    if (snake_new_x == item.x && snake_new_y == item.y) {
      snake.alive = false;
      return;
    }
  }

  // Check if the snake has hit the dynamic obstacle
  if (snake_new_x == dynamic_obstacle.x && snake_new_y == dynamic_obstacle.y) {
      snake.alive = false;
      return;
  }

  // Check if the snake's body has been hit by the dynamic obstacle
  if (snake.SnakeCell(dynamic_obstacle.x, dynamic_obstacle.y)) {
      snake.alive = false;
      return;
  }

  // Check if there's food over here
  if (food.x == snake_new_x && food.y == snake_new_y) {
    score++;
    PlaceFood();
    // Grow snake and increase speed.
    snake.GrowBody();
    snake.speed += 0.02;
  }
}

int Game::GetScore() const { return score; }
int Game::GetSize() const { return snake.size; }