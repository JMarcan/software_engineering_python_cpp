#include <vector>
#include "SDL.h"
#include "snake.h"
#include "obstacles.h"

class SnakeAI {
    public:
        static void DecideNextMove(Snake &snake, SDL_Point const food, std::vector<StaticObstacle> const &static_obstacles);

    private:
        static int Heuristic(int const current_x, int const current_y, int const goal_x, int const goal_y);
        static bool CheckCellAvailability(int const x, int const y, Snake const &snake, std::vector<StaticObstacle> const &static_obstacles);
};