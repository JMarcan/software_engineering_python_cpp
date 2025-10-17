#include <dirent.h>
#include <unistd.h>
#include <string>
#include <vector>
#include <iostream>

#include "linux_parser.h"
#include "process.h"

using std::stof;
using std::string;
using std::to_string;
using std::vector;

using std::cout;

// DONE: An example of how to read data from the filesystem
string LinuxParser::OperatingSystem() {
  string line;
  string key;
  string value;
  std::ifstream filestream(kOSPath);
  if (filestream.is_open()) {
    while (std::getline(filestream, line)) {
      std::replace(line.begin(), line.end(), ' ', '_');
      std::replace(line.begin(), line.end(), '=', ' ');
      std::replace(line.begin(), line.end(), '"', ' ');
      std::istringstream linestream(line);
      while (linestream >> key >> value) {
        if (key == "PRETTY_NAME") {
          std::replace(value.begin(), value.end(), '_', ' ');
          return value;
        }
      }
    }
  }
  return value;
}

// DONE: An example of how to read data from the filesystem
string LinuxParser::Kernel() {
  string os, version, kernel;
  string line;
  std::ifstream stream(kProcDirectory + kVersionFilename);
  if (stream.is_open()) {
    std::getline(stream, line);
    std::istringstream linestream(line);
    linestream >> os >> version >> kernel;
  }
  return kernel;
}

// BONUS: Update this to use std::filesystem
vector<int> LinuxParser::Pids() {
  vector<int> pids;

  //Implemented: Refactored to use std::filesystem, but commented as udacity compiler doesn't support std::filesystem
  /*
  for (const auto& item: std::filesystem::directory_iterator(kProcDirectory)) {
    if (item.is_directory()) {
      string filename = item.path().filename().string();
      if (std::all_of(filename.begin(), filename.end(), isdigit)) {
        int pid = stoi(filename);
        pids.push_back(pid);
      }
    }
  }
  */

  DIR* directory = opendir(kProcDirectory.c_str());
  struct dirent* file;
  while ((file = readdir(directory)) != nullptr) {
    // Is this a directory?
    if (file->d_type == DT_DIR) {
      // Is every character of the name a digit?
      string filename(file->d_name);
      if (std::all_of(filename.begin(), filename.end(), isdigit)) {
        int pid = stoi(filename);
        pids.push_back(pid);
      }
    }
  }
  closedir(directory);
  return pids;
}

// Implemented: Read and return the system memory utilization
float LinuxParser::MemoryUtilization() { 
  string line, name;
  int memory_total, memory_free, memory_buffers, memory_cached;

  std::ifstream filestream(kProcDirectory + kMeminfoFilename);
  if (filestream.is_open()) {
      // Read memory_total
      std::getline(filestream, line);
      //std::cout << line << '\n'; // DEBUG
      std::istringstream(line) >> name >> memory_total;

      // Read memory_free
      std::getline(filestream, line);
      //std::cout << line << '\n'; // DEBUG
      std::istringstream(line) >> name >> memory_free;
    
      // Skipp line with MemAvailable value
      std::getline(filestream, line);
    
     // Read memory_buffers
      std::getline(filestream, line);
      //std::cout << line << '\n'; // DEBUG
      std::istringstream(line) >> name >> memory_buffers;
    
    // Read memory_cached
      std::getline(filestream, line);
      //std::cout << line << '\n'; // DEBUG
      std::istringstream(line) >> name >> memory_cached;
    
      // Calculate memory utilization as ratio between memory used and memory total
      long memory_used = memory_free + memory_buffers + memory_cached;
      float memory_utilization = (static_cast<float>(memory_total - memory_used) / memory_total);
      return memory_utilization;
  }
  return 0.0f; 
}

// Implemented: Read and return the system uptime
long int LinuxParser::UpTime() { 
  string line;
  long int upTime;

  std::ifstream filestream(kProcDirectory + kUptimeFilename);
  if (filestream.is_open()) {
      std::getline(filestream, line);
      //std::cout << line << '\n'; // DEBUG

      std::istringstream stream(line);
      stream >> upTime;
      //std::cout << "Uptime in seconds:" << upTime << '\n'; // DEBUG
      return upTime;
  }
  return 0; 
}

// Implemented: Read and return the number of jiffies for the system
long int LinuxParser::Jiffies() { 
  string line, name;
  long int user, nice, system, idle, iowait, irq, softirq, steal, guest;

  std::ifstream filestream(kProcDirectory + kStatFilename);
  if (filestream.is_open()) {
    while (std::getline(filestream, line)) {
      //std::cout << line << '\n'; // DEBUG

      std::istringstream stream(line);
      stream >> name;
      //std::cout << "name:" << name << '\n'; // DEBUG
      if (name == "cpu") {
        stream >> user >> nice >> system >> idle >> iowait >> irq >> softirq >> steal >> guest;
        long int totalJiffies = user + nice + system + idle + iowait + irq + softirq + steal + guest;
        return totalJiffies;
      }
    }
  }
  return 0; 
}

// Implemented: Read and return the number of active jiffies for a PID
long int LinuxParser::ActiveJiffies(int pid) { 
  Process process = Process(pid);
  return process.ActiveJiffies();
}

// Implemented: Read and return the number of active jiffies for the system
long int LinuxParser::ActiveJiffies() { 
  string line, name;
  long int user, nice, system, idle, iowait, irq, softirq, steal, guest;

  std::ifstream filestream(kProcDirectory + kStatFilename);
  if (filestream.is_open()) {
    while (std::getline(filestream, line)) {
      //std::cout << line << '\n'; // DEBUG

      std::istringstream stream(line);
      stream >> name;
      //std::cout << "name:" << name << '\n'; // DEBUG
      if (name == "cpu") {
        stream >> user >> nice >> system >> idle >> iowait >> irq >> softirq >> steal >> guest;
        long int activeJiffies = user + nice + system + guest;
        return activeJiffies;
      }
    }
  }
  return 0;
}

// Implemented: Read and return the number of idle jiffies for the system
long int LinuxParser::IdleJiffies() { 
  string line, name;
  long int user, nice, system, idle, iowait, irq, softirq, steal, guest;

  std::ifstream filestream(kProcDirectory + kStatFilename);
  if (filestream.is_open()) {
    while (std::getline(filestream, line)) {
      //std::cout << line << '\n'; // DEBUG

      std::istringstream stream(line);
      stream >> name;
      //std::cout << "name:" << name << '\n'; // DEBUG
      if (name == "cpu") {
        stream >> user >> nice >> system >> idle >> iowait >> irq >> softirq >> steal >> guest;
        long int idleJiffies = idle + iowait;
        return idleJiffies;
      }
    }
  }
  return 0;
}

// Implemented: Read and return average CPU utilization during OS runtime
// Calculation logic implemented based on https://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux
vector<string> LinuxParser::CpuUtilization() { 
  string line, value;
  vector <string> cpu_values;

  std::ifstream filestream(kProcDirectory + kStatFilename);
  if (filestream.is_open()) {
    std::getline(filestream, line);
    //std::cout << line << '\n'; // DEBUG

    std::istringstream stream(line);
    while (stream >> value) {
      //std::cout << "cpu_value:" << value << '\n'; // DEBUG
      cpu_values.push_back(value);
    }
  }
  return cpu_values; 
}

// Implemented: Read and return the total number of processes
int LinuxParser::TotalProcesses() { 
  string line, name;
  int value;
  std::ifstream filestream(kProcDirectory + kStatFilename);
  if (filestream.is_open()) {
    while (std::getline(filestream, line)) {
      //std::cout << line << '\n'; // DEBUG

      std::istringstream stream(line);
      stream >> name >> value;
      //std::cout << "name:" << name << '\n'; // DEBUG
      if (name == "processes") {
        return value;
      }
    }
  }
  return 0; 
}

// Implemented: Read and return the number of running processes
int LinuxParser::RunningProcesses() { 
  string line, name;
  int value;
  std::ifstream filestream(kProcDirectory + kStatFilename);
  if (filestream.is_open()) {
    while (std::getline(filestream, line)) {
      //std::cout << line << '\n'; // DEBUG

      std::istringstream stream(line);
      stream >> name >> value;
      //std::cout << "name:" << name << '\n'; // DEBUG
      if (name == "procs_running") {
        return value;
      }
    }
  }
  return 0; 
}

// Implemented: Read and return the command associated with a process
string LinuxParser::Command(int pid) { 
  Process process = Process(pid);
  return process.Command(); 
}

// Implemented: Read and return the memory used by a process
string LinuxParser::Ram(int pid) {
  Process process = Process(pid);
  return process.Ram();
}

// Implemented: Read and return the user ID associated with a process
string LinuxParser::Uid(int pid) { 
  Process process = Process(pid);
  return process.Uid(); 
}

// Implemented: Read and return the user associated with a process
string LinuxParser::User(int pid) { 
  Process process = Process(pid);
  return process.User();
}

// Implemented: Read and return the uptime of a process
long int LinuxParser::UpTime(int pid) { 
  Process process = Process(pid);
  return process.UpTime(); 
}
