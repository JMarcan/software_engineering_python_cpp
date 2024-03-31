#include "game.h"
#include <iostream>
#include "SDL.h"
#include "obstacle.h"

Game::Game(std::size_t grid_width, std::size_t grid_height)
  : snake(grid_width, grid_height),
    generator(device()),
    random_w(0, static_cast<int>(grid_width - 1)),
    random_h(0, static_cast<int>(grid_height - 1)) {

    // create static obstacles
    static_obstacles.push_back(StaticObstacle(device, grid_width, grid_height, snake.head, static_obstacles));
    static_obstacles.push_back(StaticObstacle(device, grid_width, grid_height, snake.head, static_obstacles));
    static_obstacles.push_back(StaticObstacle(device, grid_width, grid_height, snake.head, static_obstacles));
    static_obstacles.push_back(StaticObstacle(device, grid_width, grid_height, snake.head, static_obstacles));

    // create dynamic obstacles
    dynamic_obstacles.push_back(DynamicObstacle(device, grid_width, grid_height, snake.head, static_obstacles, dynamic_obstacles));
    dynamic_obstacles.push_back(DynamicObstacle(device, grid_width, grid_height, snake.head, static_obstacles, dynamic_obstacles));
      
    // place food
    PlaceFood();
}

void Game::Run(Controller const &controller, Renderer &renderer,
               std::size_t target_frame_duration, const float starting_speed) {
  Uint32 title_timestamp = SDL_GetTicks();
  Uint32 frame_start;
  Uint32 frame_end;
  Uint32 frame_duration;
  int frame_count = 0;
  bool running = true;

  // set starting speed for snake and dynamic obstacles
  snake.speed = starting_speed;
  for (auto &item : dynamic_obstacles) {
    item.SetSpeed(starting_speed);
  }

  while (running) {
    frame_start = SDL_GetTicks();

    // Input, Update, Render - the main game loop.
    controller.HandleInput(running, snake);
    Update();
    renderer.Render(snake, food, static_obstacles, dynamic_obstacles);

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
    x = random_w(generator);
    y = random_h(generator);
    // Check that the location is not occupied by a snake before placing food
    if (snake.SnakeCell(x, y)) 
      continue;

    // Check that the location is not occupied by a static obstacle before placing food
    for (auto const &item : static_obstacles) {
      if (x == item.GetPositionX() && y == item.GetPositionY()) 
        continue;
      }

    food.x = x;
    food.y = y;
    return;
  }
}

void Game::Update() {
  if (!snake.alive) return;

  // Update position of dynamic obstacles
  for (auto &item : dynamic_obstacles) {
    item.Update(snake.GridWidth(), snake.GridHeight());
  }

  // Uddate position of snake
  snake.Update();

  // Check if the snake has hit one of static obstacles
  for (auto const &item : static_obstacles) {
    if (snake.head.x == item.GetPositionX() && snake.head.y == item.GetPositionY()) {
      snake.alive = false;
      return;
    }
  }

  // Check if the snake has hit or was hit by one of the dynamic obstacle
  for (auto const &item : dynamic_obstacles) {
    if (snake.head.x == item.GetPositionX() && snake.head.y == item.GetPositionY()) {
      snake.alive = false;
      return;
    }
    if (snake.SnakeCell(item.GetPositionX(), item.GetPositionY())) {
      snake.alive = false;
      return;
    }
  }   

  // Check if there's food over here
  if (food.x == snake.head.x && food.y == snake.head.y) {
    score++;
    PlaceFood();
    // Grow snake and increase speed.
    snake.GrowBody();
    snake.speed += 0.02;
    // Update speed of dynamic obstacles
    for (auto &item : dynamic_obstacles) {
      item.SetSpeed(snake.speed);
    }
  }
}

int Game::GetScore() const { return score; }
int Game::GetSize() const { return snake.size; }