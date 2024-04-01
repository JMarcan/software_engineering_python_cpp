# CPPND: Snake Game

In this project, I had been extending a Snake Game
as part of the Udacity C++ Nanodegree.


## New Features
- Added AI snake navigating via simple heuristic
- Added moving obstacles
- Added static obstacles
- User score is compared against the best score, the best score is saved into a file
- User can choose starting speed for the game via console input

## Addressed Rubric Points
- 1. Processing console input, to allow user choose starting speed
- 2. Reading and writing data from file, to store the best score
- 3. Using vectors to store objects for obstacles
- 4. Organizing new functionalities into functions and controlling workflow via control structures
- 6. Adding new classes, to manage obstacles and ai snake
- 7. Utilizing in classes member initialization lists
- 8. Abstracting implementation details in classes from their interfaces
- 9. Utilizing inheritance hierarchy, to define interface for StaticObstacle and DynamicObstacle via virtual base class Obstacle
- 10. Using constant variables to avoid unexpected changes in underlaying objects
- 11. Using Pass-by-reference to optimize memory consumtion and performance, for example when creating obstacles

## Potential improvements
- Multithreading can be added and rendering, user input handling, and game updates could be processed in parallel.
  Sadly, Udacity environment haven't worked with the thread library where the linker consistently throwed undefined reference to symbol 'pthread_create@@HLIBC_2.2.5'
  so multithreading was not adopted during this project.

## Dependencies for Running Locally
* cmake >= 3.7
  * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1 (Linux, Mac), 3.81 (Windows)
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* SDL2 >= 2.0
  * All installation instructions can be found [here](https://wiki.libsdl.org/Installation)
  >Note that for Linux, an `apt` or `apt-get` installation is preferred to building from source. 
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools](https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)

## Build Instructions

1. Clone this repo.
2. Make a build directory in the top level directory: `mkdir build && cd build`
3. Compile: `cmake .. && make`
4. Run it: `./SnakeGame`.