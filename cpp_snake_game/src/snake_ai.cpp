#include <vector>
#include "SDL.h"
#include "snake.h"
#include "snake_ai.h"
#include "obstacles.h"
#include <iostream>

void SnakeAI::DecideNextMove(Snake &snake, SDL_Point const food, std::vector<StaticObstacle> const &static_obstacles) {

    // Loop through current node's potential neighbours
    const int delta[4][2]{{-1, 0}, {0, -1}, {1, 0}, {0, 1}};

    int h_best = 9999;
    Snake::Direction next_move = Snake::Direction::kUp;

    for (int i = 0; i < 4; i++) {
        int neighbour_x = snake.head.x + delta[i][0];
        int neighbour_y = snake.head.y + delta[i][1];

        // Check that the potential neighbor's field is available
        if (CheckCellAvailability(neighbour_x, neighbour_y, snake, static_obstacles)) {
            // Select neighbor with the best (lowest) heuristic result towards the destination
            int neighbour_h = Heuristic(neighbour_x, neighbour_y, food.x, food.y);
            if (neighbour_h < h_best) {
                h_best = neighbour_h;

                // update the next_move direction
                switch (i) {
                    case 0: {
                        next_move = Snake::Direction::kLeft;
                        break;
                    }
                    case 1: {
                        next_move = Snake::Direction::kUp; 
                        break;
                    }
                    case 2: {
                        next_move = Snake::Direction::kRight;
                        break;
                    }
                    case 3: {
                        next_move = Snake::Direction::kDown;
                        break;
                    }
                }
            }
        }
    }
    snake.direction = next_move;
  }

// Calculate Manhattan Distance
int SnakeAI::Heuristic(int const current_x, int const current_y, int const goal_x, int const goal_y) {
    return abs(goal_x - current_x) + abs(goal_y - current_y);
}

// Calculate whether cell is available for the move of ai snake
bool SnakeAI::CheckCellAvailability(int const x, int const y, Snake const &snake, std::vector<StaticObstacle> const &static_obstacles) {
    // Check whether cell is outside of the grid
    if (x < 0 || x > snake.GridWidth()-1) return false;
    if (y < 0 || y > snake.GridHeight()-1) return false;

    // Check whether cell is occupied by the snake
    if (snake.SnakeCell(x, y)) return false;

    // Check whether cell is occupied by one of static obstacles
    for (auto const &item : static_obstacles) {
        if (x == item.GetPositionX() && y == item.GetPositionY()){
            return false;
        } 
    }

    return true;
}