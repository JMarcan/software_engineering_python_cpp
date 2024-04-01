#include <random>
#include "obstacles.h"

SDL_Point Obstacle::GetPosition() const { return position; }
int Obstacle::GetPositionX() const { return position.x; }
int Obstacle::GetPositionY() const { return position.y; }

StaticObstacle::StaticObstacle(std::random_device &device, int const grid_width, int const grid_height, SDL_Point const &snake_location_to_avoid, std::vector<StaticObstacle> const &existing_static_obstacles_to_avoid) {
    std::mt19937 generator(device());
    std::uniform_int_distribution<int> random_w(0, static_cast<int>(grid_width - 1));
    std::uniform_int_distribution<int> random_h(0, static_cast<int>(grid_height - 1));
    int x, y;
    while (true) {
        x = random_w(generator);
        y = random_h(generator);

        // Check that the location is not occupied by a snake before placing a static obstacle
        if (x == snake_location_to_avoid.x && y == snake_location_to_avoid.y)
            continue;

        // Check that the location is not occupied by already existing static obstacle before placing a static obstacle
        for (auto const &item : existing_static_obstacles_to_avoid) {
            if (x == item.GetPositionX() && y == item.GetPositionY()){
                continue;
            } 
        }
        position = SDL_Point{x, y};
        return;
    }
  }

  DynamicObstacle::DynamicObstacle(std::random_device &device, int const grid_width, int const grid_height, SDL_Point const &snake_location_to_avoid, std::vector<StaticObstacle> const &existing_static_obstacles_to_avoid, std::vector<DynamicObstacle> const &existing_dynamic_obstacles_to_avoid) {
    std::mt19937 generator(device());
    std::uniform_int_distribution<int> random_w(0, static_cast<int>(grid_width - 1));
    std::uniform_int_distribution<int> random_h(0, static_cast<int>(grid_height - 1));
    int x, y;
    while (true) {
        x = random_w(generator);
        y = random_h(generator);

        // Check that the location is not occupied by a snake before placing a static obstacle
        if (x == snake_location_to_avoid.x && y == snake_location_to_avoid.y)
            continue;

        // Check that the location is not occupied by a static obstacle before placing a dynamic obstacle
        for (auto const &item : existing_static_obstacles_to_avoid) {
        if (x == item.GetPositionX() && y == item.GetPositionY()) 
            continue;
        } 

        // Check that the location is not occupied by a dynamic obstacle before placing a dynamic obstacle
        for (auto const &item : existing_dynamic_obstacles_to_avoid) {
        if (x == item.GetPositionX() && y == item.GetPositionY()) 
            continue;
        } 
        position = SDL_Point{x, y};
        return;
  }
}

void DynamicObstacle::Update(int const grid_width, int const grid_height) {
    // Update dynamic obstacle position
    float_position_x += speed;
    // Wrap the dynamic obstacle around to the beginning if going off of the screen.
    float_position_x = fmod(float_position_x + grid_width, grid_width);
    position.x = static_cast<int>(float_position_x);
}

void DynamicObstacle::SetSpeed(float const new_speed) {
    // Update dynamic obstacle speed
    speed = new_speed;
}