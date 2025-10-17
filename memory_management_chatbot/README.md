# CPPND: Memory Management Chatbot

In this project, I had implemented memory management for a chatbot
as part of the Udacity C++ Nanodegree.

<img src="images/chatbot_demo.gif"/>

The ChatBot code creates a dialogue where users can ask questions about some aspects of memory management in C++. After the knowledge base of the chatbot has been loaded from a text file, a knowledge graph representation is created in computer memory, where chatbot answers represent the graph nodes and user queries represent the graph edges. After a user query has been sent to the chatbot, the Levenshtein distance is used to identify the most probable answer. The code is fully functional as-is and uses raw pointers to represent the knowledge graph and interconnections between objects throughout the project.

## Dependencies for Running Locally
* cmake >= 3.11
  * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1 (Linux, Mac), 3.81 (Windows)
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools](https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)
* wxWidgets >= 3.0
  * Linux: `sudo apt-get install libwxgtk3.0-gtk3-dev libwxgtk3.0-gtk3-0v5`. If you are facing unmet dependency issues, refer to the [official page](https://wiki.codelite.org/pmwiki.php/Main/WxWidgets30Binaries#toc2) for installing the unmet dependencies.
  * Mac: There is a [homebrew installation available](https://formulae.brew.sh/formula/wxmac).
  * Installation instructions can be found [here](https://wiki.wxwidgets.org/Install). Some version numbers may need to be changed in instructions to install v3.0 or greater.

## Basic Build Instructions

1. Clone this repo.
2. Make a build directory in the top level directory: `mkdir build && cd build`
3. Compile: `cmake .. && make`
4. Run it: `./membot`.

## Implementation Details

### Task 1 : Exclusive Ownership 1
In file `chatgui.h` / `chatgui.cpp`, implemented `_chatLogic` to be an exclusive resource to class `ChatbotPanelDialog` using a smart pointer. Updated the the code so that data structures and function parameters reflect the new structure. 

### Task 2 : The Rule Of Five
In file `chatbot.h` / `chatbot.cpp`, implemented the class `ChatBot` so that it complies with [the Rule of Five](https://www.geeksforgeeks.org/cpp/rule-of-five-in-cpp/). Allocating / deallocating memory resources on the heap and also copying member data where it makes sense.  In each of the methods (e.g. the copy constructor), a string like "ChatBot Copy Constructor" is printed to the console making visible which method is called in later examples. 

### Task 3 : Exclusive Ownership 2
In file `chatlogic.h` / `chatlogic.cpp`, adapted the vector `_nodes` in a way that the instances of `GraphNodes` to which the vector elements refer are exclusively owned by the class `ChatLogic`. Used a  smart pointer to achieve this. Updated the code so that data structures and function parameters reflect the changes. When passing the `GraphNode` instances to functions, the ownership is not transferred and changes are contained to to class `ChatLogic`.

### Task 4 : Moving Smart Pointers

In files `chatlogic.h` / `chatlogic.cpp` and `graphnode.h` / `graphnode.cpp` changed the ownership of all instances of `GraphEdge` so that each instance of `GraphNode` exclusively owns the outgoing `GraphEdges` and holds non-owning references to incoming `GraphEdges`. Used smart pointers and updated the code such that data structures and function parameters reflect the changes. When transferring ownership from class `ChatLogic`, where all instances of `GraphEdge` are created, into instances of `GraphNode`, move semantics is used. 

### Task 5 : Moving the ChatBot

In file `chatlogic.cpp`, created a local `ChatBot` instance on the stack at the bottom of function `LoadAnswerGraphFromFile`. Then, used move semantics to pass the `ChatBot` instance into the root node. Updated `ChatLogic` to have no ownership relation to the `ChatBot` instance and thus being no longer responsible for memory allocation and deallocation. Note that the member `_chatBot` of `ChatLogic` remains so it can be used as a communication handle between GUI and `ChatBot` instance. The changes were contained to `chatlogic.h` / `chatlogic.cpp` and `graphnode.h` / `graphnode.cpp`. When the program is executed, messages on which part of the Rule of Five components of `ChatBot` is called is printed to the console. When sending a query to the `ChatBot`, the output looks like the following: 

```
ChatBot Constructor
ChatBot Move Constructor
ChatBot Move Assignment Operator
ChatBot Destructor
ChatBot Destructor 
```
