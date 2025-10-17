# CPPND: Program a Concurrent Traffic Simulation

In this project, I had implemented a traffic simulation utilizing concurrency
as part of the Udacity C++ Nanodegree.

<img src="data/traffic_simulation.gif"/>

Throughout the Concurrency course, I've developed a traffic simulation in which vehicles are moving along streets and are crossing intersections. However, with increasing traffic in the city, traffic lights are needed for road safety. Each intersection  therefore needs to be equipped with a traffic light. In this project, I've build a suitable and thread-safe communication protocol between vehicles and intersections to complete the simulation. Mutexes, locks and message queues are used to implement the traffic lights and integrate them properly in the code base.

## Dependencies for Running Locally
* cmake >= 2.8
  * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1 (Linux, Mac), 3.81 (Windows)
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* OpenCV >= 4.1
  * The OpenCV 4.1.0 source code can be found [here](https://github.com/opencv/opencv/tree/4.1.0)
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools](https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)

## Basic Build Instructions

1. Clone this repo.
2. Make a build directory in the top level directory: `mkdir build && cd build`
3. Compile: `cmake .. && make`
4. Run it: `./traffic_simulation`.

## Project Tasks

When the project is built initially, all traffic lights will be green. When you are finished with the project, your traffic simulation should run with red lights controlling traffic, just as in the .gif file above. See the classroom instruction and code comments for more details on each of these parts. 

- **Task FP.1** : Defined a class `TrafficLight` which is a child class of `TrafficObject`. The class have the public methods `void waitForGreen()` and `void simulate()` as well as `TrafficLightPhase getCurrentPhase()`, where `TrafficLightPhase` is an enum that can be either `red` or `green`. Added the private method `void cycleThroughPhases()` together with private member `_currentPhase` which can take `red` or `green` as its value.
- **Task FP.2** : Implemented the function with an infinite loop that measures the time between two loop cycles and toggles the current phase of the traffic light between red and green and sends an update method to the message queue using move semantics. The cycle duration is a random value between 4 and 6 seconds. The while-loop uses `std::this_thread::sleep_`for to wait 1ms between two cycles. The private method `cycleThroughPhases` should is started in a thread when the public method `simulate` is called. Thread queue is used in the base class for this.
- **Task FP.3** : Defined a class `MessageQueue` which has the public methods send and receive. Send takes an value reference of type TrafficLightPhase whereas receive returns this type. The class defines an `std::dequeue` called `_queue`, which stores objects of type `TrafficLightPhase`. Finally, there is an `std::condition_variable` as well as an `std::mutex` as private members.
- **Task FP.4** : Implemented the method `Send`, which uses the mechanisms `std::lock_guard<std::mutex>` as well as `_condition.notify_one()` to add a new message to the queue and afterwards sends a notification. Also, in class `TrafficLight`, creates a private member of type `MessageQueue` for messages of type `TrafficLightPhase` and uses it within the infinite loop to push each new `TrafficLightPhase` into it by calling send in conjunction with move semantics.
- **Task FP.5** : The method receive uses `std::unique_lock<std::mutex>` and `_condition.wait()` to wait for and receive new messages and pull them from the queue using move semantics. The received object is then returned by the receive function. Implemented the method `waitForGreen`, in which an infinite while-loop runs and repeatedly calls the `receive` function on the message queue. Once it receives `TrafficLightPhase::green`, the method returns.
- **Task FP.6** : In class Intersection, added a private member `_trafficLight` of type `TrafficLight`. In method `Intersection::simulate()`, starts the simulation of `_trafficLight`. The method `Intersection::addVehicleToQueue` uses the methods `TrafficLight::getCurrentPhase` and `TrafficLight::waitForGreen` to block the execution until the traffic light turns green.
