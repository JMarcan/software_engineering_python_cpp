#include <iostream>
#include <string>
#include "renderer.h"
#include "obstacles.h"

Renderer::Renderer(const std::size_t screen_width,
                   const std::size_t screen_height,
                   const std::size_t grid_width, const std::size_t grid_height)
    : screen_width(screen_width),
      screen_height(screen_height),
      grid_width(grid_width),
      grid_height(grid_height) {
  // Initialize SDL
  if (SDL_Init(SDL_INIT_VIDEO) < 0) {
    std::cerr << "SDL could not initialize.\n";
    std::cerr << "SDL_Error: " << SDL_GetError() << "\n";
  }

  // Create Window
  sdl_window = SDL_CreateWindow("Snake Game", SDL_WINDOWPOS_CENTERED,
                                SDL_WINDOWPOS_CENTERED, screen_width,
                                screen_height, SDL_WINDOW_SHOWN);

  if (nullptr == sdl_window) {
    std::cerr << "Window could not be created.\n";
    std::cerr << " SDL_Error: " << SDL_GetError() << "\n";
  }

  // Create renderer
  sdl_renderer = SDL_CreateRenderer(sdl_window, -1, SDL_RENDERER_ACCELERATED);
  if (nullptr == sdl_renderer) {
    std::cerr << "Renderer could not be created.\n";
    std::cerr << "SDL_Error: " << SDL_GetError() << "\n";
  }
}

Renderer::~Renderer() {
  SDL_DestroyWindow(sdl_window);
  SDL_Quit();
}

void Renderer::Render(const Snake &snake, const SDL_Point &food, const std::vector<StaticObstacle> &static_obstacles, const std::vector<DynamicObstacle> &dynamic_obstacles, const Snake &snake_ai) {
  SDL_Rect block;
  block.w = screen_width / grid_width;
  block.h = screen_height / grid_height;

  // Clear screen
  SDL_SetRenderDrawColor(sdl_renderer, 0x1E, 0x1E, 0x1E, 0xFF);
  SDL_RenderClear(sdl_renderer);

  // Render static obstacles
  SDL_SetRenderDrawColor(sdl_renderer, 0x69, 0x69, 0x69, 0xFF); // Grey
  for (auto const &item : static_obstacles) {
    block.x = item.GetPositionX() * block.w;
    block.y = item.GetPositionY() * block.h;
    SDL_RenderFillRect(sdl_renderer, &block);
  }

  // Render dynamic obstacle
  SDL_SetRenderDrawColor(sdl_renderer, 0xE6, 0x7E, 0x22, 0xFF); // Orange
  for (auto const &item : dynamic_obstacles) {
    block.x = item.GetPositionX() * block.w;
    block.y = item.GetPositionY() * block.h;
    SDL_RenderFillRect(sdl_renderer, &block);
  }

  // Render food
  SDL_SetRenderDrawColor(sdl_renderer, 0x18, 0x6A, 0x3B, 0xFF); // Green
  block.x = food.x * block.w;
  block.y = food.y * block.h;
  SDL_RenderFillRect(sdl_renderer, &block);

  // Render snake_users's body
  SDL_SetRenderDrawColor(sdl_renderer, 0xFF, 0xFF, 0xFF, 0xFF); // White
  for (SDL_Point const &point : snake.body) {
    block.x = point.x * block.w;
    block.y = point.y * block.h;
    SDL_RenderFillRect(sdl_renderer, &block);
  }

  // Render snake_user's head
  block.x = snake.head.x * block.w;
  block.y = snake.head.y * block.h;
  if (snake.alive) {
    SDL_SetRenderDrawColor(sdl_renderer, 0x00, 0x7A, 0xCC, 0xFF); // Blue
  } else {
    SDL_SetRenderDrawColor(sdl_renderer, 0xFF, 0x00, 0x00, 0xFF);
  }
  SDL_RenderFillRect(sdl_renderer, &block);

  // Render snake_ai's body
  SDL_SetRenderDrawColor(sdl_renderer, 0xFC, 0x4E, 0x03, 0xFF); // Orange
  for (SDL_Point const &point : snake_ai.body) {
    block.x = point.x * block.w;
    block.y = point.y * block.h;
    SDL_RenderFillRect(sdl_renderer, &block);
  }

  // Render snake_ai's head // Purple
  block.x = snake_ai.head.x * block.w;
  block.y = snake_ai.head.y * block.h;
  if (snake_ai.alive) {
    SDL_SetRenderDrawColor(sdl_renderer, 0x90, 0x20, 0xa1, 0xFF);
  } else {
    SDL_SetRenderDrawColor(sdl_renderer, 0xFF, 0x00, 0x00, 0xFF);
  }
  SDL_RenderFillRect(sdl_renderer, &block);

  // Update Screen
  SDL_RenderPresent(sdl_renderer);
}

void Renderer::UpdateWindowTitle(int score, int fps) {
  std::string title{"Snake Score: " + std::to_string(score) + " FPS: " + std::to_string(fps)};
  SDL_SetWindowTitle(sdl_window, title.c_str());
}
