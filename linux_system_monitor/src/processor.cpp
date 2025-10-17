#include "processor.h"
#include "linux_parser.h"


// Implemented: Return the aggregate CPU utilization
float Processor::Utilization() { 
    long int total = LinuxParser::Jiffies();
    long int active = LinuxParser::ActiveJiffies();
    
    return (1.0 / total) * active;
}