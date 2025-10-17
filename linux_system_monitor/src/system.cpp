#include <unistd.h>
#include <cstddef>
#include <set>
#include <string>
#include <vector>

#include "process.h"
#include "processor.h"
#include "system.h"

#include "linux_parser.h"

using std::set;
using std::size_t;
using std::string;
using std::vector;

// Implemented: Return the system's CPU
Processor& System::Cpu() { return cpu_; }

// Implemented: Return a container composed of the system's processes
vector<Process>& System::Processes() { 
    static std::vector<Process> _processes;

    _processes.clear();
    vector<int> pids = LinuxParser::Pids();

    for (int pid: pids) {
        _processes.push_back(Process(pid));
    }

    // Implemented: Sort processes based on their CPU utilization
    std::sort(_processes.begin(), _processes.end());

    return _processes; 
}

// Implemented: Return the system's kernel identifier (string)
std::string System::Kernel() { return LinuxParser::Kernel(); }

// Implemented: Return the system's memory utilization
float System::MemoryUtilization() { return LinuxParser::MemoryUtilization(); }

// Implemented: Return the operating system name
std::string System::OperatingSystem() { return LinuxParser::OperatingSystem(); }

// Implemented: Return the number of processes actively running on the system
int System::RunningProcesses() { return LinuxParser::RunningProcesses(); }

// Implemented: Return the total number of processes on the system
int System::TotalProcesses() {return LinuxParser::TotalProcesses(); }

// Implemented: Return the number of seconds since the system started running
long int System::UpTime() { return LinuxParser::UpTime(); }