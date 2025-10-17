#include <unistd.h>
#include <cctype>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <pwd.h> //enabling uid to username translation

#include "process.h"
#include "linux_parser.h"

using std::string;
using std::to_string;
using std::vector;

using namespace LinuxParser;

Process::Process(int pid) {
    _pid = pid;
}

// Implemented: Return this process's ID
int Process::Pid() { return _pid; }

long int Process::ActiveJiffies() { 
    string line, value;
    long int utime, stime, cutime, cstime;

    std::ifstream filestream(kProcDirectory + '/' + std::to_string(_pid) + kStatFilename);
    if (filestream.is_open()) {
        std::getline(filestream, line);

        std::istringstream stream(line);
        for (int i=1; i<=17; i++) {
            stream >> value;

            switch(i) {
                case 14: //utime time is the 14th field in the first line of the file
                    utime = stoi(value);
                    break;
                case 15:
                    stime = stoi(value);
                    break;
                case 16:
                    cutime = stoi(value);
                    break;
                case 17:
                    cstime = stoi(value);
                    break;
            }
        }
        long int activeJiffies = utime + stime + cutime + cstime;
        return activeJiffies;
    }
    return 0; 
}


// Implemented: Return this process's CPU utilization during process's runtime
// Calculation logic implemented based on https://stackoverflow.com/questions/16726779/how-do-i-get-the-total-cpu-usage-of-an-application-from-proc-pid-stat/16736599#16736599
float Process::CpuUtilization() { 
    long int total = Process::UpTime();
    long int active = Process::ActiveJiffies() / sysconf(_SC_CLK_TCK);  
  
  	// Prevent divisions by zero when process is newly started
  	if (total == 0) {
  		return 0.0;
    } else {
        return (1.0 / total) * active;
    }
}

// Implemented: Return the command that generated this process
string Process::Command() { 
    string line;

    std::ifstream filestream(kProcDirectory + '/' + std::to_string(_pid) + kCmdlineFilename);
    if (filestream.is_open()) {
        std::getline(filestream, line);
        return line;
    }
    return string(); 
}

// Implemented: Return this process's memory utilization
string Process::Ram() { 
    string line, name, value;
    int processMemoryInMBs, processMemoryInKBs;

    std::ifstream filestream(kProcDirectory + "/" + std::to_string(_pid) + kStatusFilename);
    if (filestream.is_open()) {
        // Read memory_total
        while (std::getline(filestream, line)) {
            //std::cout << line << '\n'; // DEBUG
            std::istringstream stream(line);
            stream >> name;
            //std::cout << "name:" << name << '\n'; // DEBUG
            if (name == "VmSize:") {
                stream >> value;
                processMemoryInKBs = stoi(value);
                break;
            }
        }
        processMemoryInMBs = processMemoryInKBs / 1024;
        return std::to_string(processMemoryInMBs);
    }
    return string(); 
}

string Process::Uid() { 
    string line, name, uid;
    std::ifstream filestream(kProcDirectory + "/" + std::to_string(_pid) + kStatusFilename);

    if (filestream.is_open()) {
        while (std::getline(filestream, line)) {
            //std::cout << line << '\n'; // DEBUG

            std::istringstream stream(line);
            stream >> name;
            //std::cout << "name:" << name << '\n'; // DEBUG
            if (name == "Uid:") {
                stream >> uid;
                //std::cout << "line:" << line << '\n'; // DEBUG
                //std::cout << "Uid:" << uid << '\n'; // DEBUG
                break;
            }
        }
    }
    return uid; 
}

// Implemented: Return the user (name) that generated this process
string Process::User() { 
    string uid = Process::Uid();
    struct passwd* pw = getpwuid(stoi(uid)); // Get corresponding username for a given uid with getpwuid function
    if (pw != nullptr) {
        return string(pw->pw_name);
    }
    return string(); 
}

// Implemented: Return the age of this process (in seconds)
long int Process::UpTime() { 
    string line, value;
    long int processStartTimeInClockTicks=0;

    std::ifstream filestream(kProcDirectory + '/' + std::to_string(_pid) + kStatFilename);
    if (filestream.is_open()) {
        std::getline(filestream, line);

        std::istringstream stream(line);
        for (int i=1; i<=22; i++) {
            stream >> value;
            if (i == 22) { // start time is the 22th field in the first line of the file
                //std::cout << "value:" << value << '\n'; // DEBUG
                processStartTimeInClockTicks = stoi(value);
            }
        }
    }
    //std::cout << "Uptime in seconds:" << upTime << '\n'; // DEBUG
    if (processStartTimeInClockTicks > 0) {
        long int systemUptime = LinuxParser::UpTime();
        long int processStartTime = processStartTimeInClockTicks / sysconf(_SC_CLK_TCK);
        long int processUpTime = systemUptime - processStartTime;

        return processUpTime;
    }
    return 0; 
}

// Implemented: Overload the "less than" comparison operator for Process objects
bool Process::operator<(Process & a){ 
    return CpuUtilization() > a.CpuUtilization(); 
}