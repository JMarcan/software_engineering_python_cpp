#ifndef OBSTACLE_H
#define OBSTACLE_H

#include <random>
#include "SDL.h"
#include "snake.h"

class Obstacle {
    public:
        SDL_Point GetPosition() const;
        int GetPositionX() const;
        int GetPositionY() const;

    protected:
        SDL_Point position;
};

class StaticObstacle: virtual public Obstacle {
    public:
        StaticObstacle(std::random_device &device, int const grid_width, int const grid_height, SDL_Point const &snake_location_to_avoid, std::vector<StaticObstacle> const &existing_static_obstacles_to_avoid);
};

class DynamicObstacle: virtual public Obstacle {
    public:
        DynamicObstacle(std::random_device &device, int const grid_width, int const grid_height, SDL_Point const &snake_location_to_avoid, std::vector<StaticObstacle> const &existing_static_obstacles_to_avoid, std::vector<DynamicObstacle> const &existing_dynamic_obstacles_to_avoid);
        void Update(int const grid_width, int const grid_height);
        void SetSpeed(float const new_speed);
        
    private:
        float float_position_x;
        float float_position_y;
        float speed{0.1f};
};



#endif