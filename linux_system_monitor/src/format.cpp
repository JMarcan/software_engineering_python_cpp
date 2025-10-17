#include <string>
#include <iostream>
#include <sstream>
#include <iomanip>
#include "format.h"

using std::string;

string Format::ElapsedTime(long int seconds) { 
    int hours = seconds / 3600;
    int minutes = (seconds % 3600) / 60;
    int remaining_seconds = seconds % 60;

    // Format string as HH:MM:SS
  	std::stringstream ss;
  	ss << std::setfill('0') << std::setw(2) << hours \
      << ":" << std::setfill('0') << std::setw(2) << minutes \
      << ":" << std::setfill('0') << std::setw(2) << remaining_seconds;
  
  	string timeformat = ss.str();

    return timeformat; 
}