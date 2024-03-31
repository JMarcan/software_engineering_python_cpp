# CPPND: Snake Game

In this project, I had been extending a Snake Game
as part of the Udacity C++ Nanodegree.


## New Features
- User score is compared against the best score, the best score is saved into a file
- Added static obstacles to the game
- Added dynamic obstacle to the game
- User can choose starting speed for the game via console input

## Addressed Rubric Points

Loops, Functions, I/O
- New functionalities are organized in functions
- The best score is saved into a file
- The best score is loaded from the file, compared against the user score, and if user set a new record it's stored in the file 
- Project uses vectors to store objects for obstacles
- User can choose starting speed for the game via console input

Object Oriented Programming
- Added new classes for obstacles
- Classes utilize member initialization lists
- Classes abstract implementation details from their interfaces
- Inheritance hierarchy for StaticObstacle and DynamicObstacle class with virtual class Obstacle

Memory Management
- Using pass-by-reference in classes for obstacles
-
-

Concurrency
-
-
-

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


## CC Attribution-ShareAlike 4.0 International
Shield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg