#include <iostream>
#include "SDL.h"
#include "game.h"
#include "snake.h"
#include "snake_ai.h"
#include "obstacles.h"

Game::Game(std::size_t grid_width, std::size_t grid_height)
  : snake_user(grid_width, grid_height, grid_width/2, grid_height/2),
    snake_ai(grid_width, grid_height, 0.0, 0.0),
    generator(device()),
    random_w(0, static_cast<int>(grid_width - 1)),
    random_h(0, static_cast<int>(grid_height - 1)) {

    // create static obstacles
    static_obstacles.push_back(StaticObstacle(device, grid_width, grid_height, snake_user.head, static_obstacles));
    static_obstacles.push_back(StaticObstacle(device, grid_width, grid_height, snake_user.head, static_obstacles));
    static_obstacles.push_back(StaticObstacle(device, grid_width, grid_height, snake_user.head, static_obstacles));
    static_obstacles.push_back(StaticObstacle(device, grid_width, grid_height, snake_user.head, static_obstacles));

    // create dynamic obstacles
    // dynamic_obstacles.push_back(DynamicObstacle(device, grid_width, grid_height, snake_user.head, static_obstacles, dynamic_obstacles));
    // dynamic_obstacles.push_back(DynamicObstacle(device, grid_width, grid_height, snake_user.head, static_obstacles, dynamic_obstacles));
      
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
  snake_user.speed = starting_speed;
  snake_ai.speed = starting_speed;
  for (auto &item : dynamic_obstacles) {
    item.SetSpeed(starting_speed);
  }

  while (running) {
    frame_start = SDL_GetTicks();

    // Input, Update, Render - the main game loop.
    controller.HandleInput(running, snake_user);
    snake_ai.DecideNextMove(snake_ai, food, static_obstacles, dynamic_obstacles);
    Update();
    renderer.Render(snake_user, food, static_obstacles, dynamic_obstacles, snake_ai);

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
    if (snake_user.SnakeCell(x, y) or snake_ai.SnakeCell(x, y)) 
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
  if (!snake_user.alive) return;

  // Update position of dynamic obstacles
  for (auto &item : dynamic_obstacles) {
    item.Update(snake_user.GridWidth(), snake_user.GridHeight());
  }

  // Uddate snake_user and snake_ai position
  snake_user.Update();
  snake_ai.Update();

  // Check if the snake_user and snake_ai has hit one of static obstacles
  for (auto const &item : static_obstacles) {
    if (snake_user.head.x == item.GetPositionX() && snake_user.head.y == item.GetPositionY()) {
      snake_user.alive = false;
      return; // end the game if user died
    }
    if (snake_ai.head.x == item.GetPositionX() && snake_ai.head.y == item.GetPositionY()) {
      snake_ai.alive = false;
    }
  }

  // Check if the snake_user and snake_ai has hit or was hit by one of the dynamic obstacle
  for (auto const &item : dynamic_obstacles) {
    if (snake_user.SnakeCell(item.GetPositionX(), item.GetPositionY())) {
      snake_user.alive = false;
      return; // end the game if user died
    }
    if (snake_ai.SnakeCell(item.GetPositionX(), item.GetPositionY())) {
      snake_ai.alive = false;
    }
  }  

  // // Check if the snake_user has hit itself
  // if (snake_user.SnakeCell(snake_user.head.x, snake_user.head.y)) {
  //     snake_user.alive = false;
  //     return; // end the game if user died
  // }
  
  // Check if the snake_user has hit the snake_ai
  if (snake_user.head.x == snake_ai.head.x && snake_user.head.y == snake_ai.head.y) {
      snake_user.alive = false;
      snake_ai.alive = false;
      return;
  }

  //Check if the snake_user was hit by the snake_ai
  if (snake_ai.SnakeCell(snake_user.head.x, snake_user.head.y)) {
      snake_user.alive = false;
      snake_ai.alive = false;
      return; // end the game if user died
  }

  // Check if the snake_user entered food field
  if (food.x == snake_user.head.x && food.y == snake_user.head.y) {
    score++;
    EatFood(snake_user);
  }
  // Check if the snake_ai entered food field
  else if (food.x == snake_ai.head.x && food.y == snake_user.head.y)
    EatFood(snake_ai);
}
void Game::EatFood(Snake &snake) {
  PlaceFood();
  // Grow snake_user and increase speed.
  snake.GrowBody();
  snake.speed += 0.02;
}
int Game::GetScore() const { return score; }
int Game::GetSize() const { return snake_user.size; }