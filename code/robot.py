import numpy as np
import json

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''

        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim
        
        self.maze_area = maze_dim ** 2.
        self.maze_grid = np.zeros((maze_dim, maze_dim), dtype=np.int) # Grid for wall locations for each maze.
        self.path_grid = np.zeros((maze_dim, maze_dim), dtype=np.int)
        self.step_count = 0
        
        # Text file in which the travelled path will be logged.
        self.log_filename = 'travelled_path.json'
        
        self.backwards = 0
        
        #path_grid values
        self.unvisited = 0
        self.visited_once = 1
        self.visited_twice = 2
        
        # create file logging visited path and write head line
        with open(self.log_filename, 'w+') as file:
            file.write('[robot_x, robot_y, visited, heading]\n')
    
        self.DEBUG = True
    def print_debug(self, debug_message):
        """Prints debug message if Debug mode is set to True
         
        Args: 
            debug_message: string to be printed
            
        Returns: 
            None
            
        Examples:
            >>> print_debug("move robot to the right")
        """
        
        if self.DEBUG == True:
            print("[ Debug message ]: {0}".format(debug_message))
        
    def wall_follower(self, sensors):
        """Wall follower algorithm deciding on the next step
        
        The wall follower algorithm works only for simply connected maze types.
        Left-hand rule is used.
        
        Args: 
            sensors: list of three int values indicating number of open squares 
                in front of the left, center, and right sensors (in that order)
        
        Returns: 
            rotation, movement
            
            - rotation: integer indicating the robot’s rotation on that timestep.
                taking one of three values: -90, 90, or 0 
                for counterclockwise, clockwise, or no rotation (in that order)
            - movement: integer indicating the robot’s movement on that timestep
                movement follows the rotiation in the range [-3, 3] inclusive
            
        Examples:
            >>> sensors=[0, 10, 0]
            >>> rotation, movement = self.wall_follower(sensors)
        """
        
        movement = 0
        rotation = 0
        
        # 1. If you can turn left, do it
        if sensors[0] > 0:
            movement = 1
            rotation = -90
            self.print_debug("move left")
            
        # 2. Else (If you can't turn left), if you can continue going straight,
        # do it    
        elif sensors[1] > 0:
            movement = 1
            rotation = 0
            self.print_debug("move 1 forward")
            
        # 3. Else (If you can't do either of the previous steps), 
        # if you can turn right,do it    
        elif sensors[2] > 0:
            movement = 1
            rotation = 90
            self.print_debug("move right")
            
        # 4. If you reached a dead end, turn back 180 degrees
        # if you can turn right,do it        
        else:
            movement = 1
            rotation = self.turn_backwards()
            self.print_debug("move backward")
            
        return rotation, movement
   
    def turn_backwards(self):
        """Turns the robot backwards 180°degrees
            
        Args: 
            None
        
        Returns: 
            rotation
        Examples:
            >>> rotation = 90
            >>> rotation = self.turn_backwards()
        """
        rotation = 0
        
        if rotation == 0:
            rotation = 180
        elif rotation == 90:
            rotation = -90
        elif rotation == -90:
            rotation = 90
            
        return rotation
    
    def update_map(self, possible_directions):
        """Update the robot's internal map using the unblocked (open)
            directions detected by the current sensor readings.
            
        Args: 
            possible_directions: list of possible directions
                can contain those values: 'left', 'right', 'forward'
        
        Returns: 
            None
            
        Examples:
            >>> possible_directions=['left', 'forward']
            >>> rotation, movement = self.update_map(possible_directions)
        """
        
        # Get the unit vector which points in the direction of the robot's heading
        movement_vec = np.array(self.direction_to_vec[self.heading])

        # First, translate the detected openings into global directions
        for direction in possible_directions:
            global_dir = None
            if direction == 'left':
                global_dir = self.dict_rotation[self.heading][0]
            elif direction == 'right':
                global_dir = self.dict_rotation[self.heading][1]
            elif direction == 'forward':
                global_dir = self.heading

            # Get the corresponding wall value for an wall opening in the given direction
            wall_value = self.wall_values[global_dir]
            # Update the current map cell with the new wall value
            self.maze_map[self.x][self.y] |= wall_value
            # Rotate robot's direction vector to given direction
            dir_vec = np.dot(movement_vec, self.rot_matrices[direction])
            # Get the wall opening value for the next cell
            wall_value = self.wall_values[self.opposite[global_dir]]
            # Update the next map cell with the opening that can be seen from this cell.
            # If this step is omitted, the robot never maps entries to deadends.
            self.maze_map[self.x + dir_vec[0]][
                self.y + dir_vec[1]] |= wall_value
    
    def check_possible_directions(self, sensors):
        """Check which directions are not blocked return them."""
        possible_directions = []
        if sensors[0] > 0:
            possible_directions.append('left')
        if sensors[1] > 0:
            possible_directions.append('forward')
        if sensors[2] > 0:
            possible_directions.append('right')
        return possible_directions
    
    def tremaux_algo(self, sensors):
        """Tremaux algorithm deciding on the next step
                
        Args: 
            sensors: list of three int values indicating number of open squares 
                in front of the left, center, and right sensors (in that order)
        
        Returns: 
            rotation, movement
            
            - rotation: integer indicating the robot’s rotation on that timestep.
                taking one of three values: -90, 90, or 0 
                for counterclockwise, clockwise, or no rotation (in that order)
            - movement: integer indicating the robot’s movement on that timestep
                movement follows the rotiation in the range [-3, 3] inclusive
        
            
        Examples:
            >>> sensors=[0, 10, 0]
            >>> rotation, movement = self.tremaux_algo(sensors)
        """
        
        movement = 0
        rotation = 0
        
        possible_directions = self.check_possible_directions(sensors)
        #self.update(map(possible_directions))
        
            
        return rotation, movement
               
        
    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''

        self.step_count +=1 # measure number of steps to solve maze
        self.print_debug("=== {0}.step ===".format(self.step_count))
        
        x = self.location[0]
        y = self.location[1]
        self.print_debug("Location: {0}".format(self.location))
        
        # add recent step to robot's travelled path
        self.path_grid[x][y] = 1       
        
        # Calculate the percentage of the maze the robot has visited
        self.print_debug("Robot has explored {:04.2f}% of the maze.\n".format(self.explored_percentage()))
        
        self.print_debug(self.path_grid)
        
        # Execute the next move
        rotation, movement = self.wall_follower(sensors)

        # Update the heading and location
        self.update_heading(rotation, movement)
        self.log_location()

        return rotation, movement
    
    def explored_percentage(self):
        """Calculate the percentage of the maze the robot has visited
                
        Args: 
            None
        
        Returns: 
            explored_perct: float with percentage of the maze the robot has visited
            
        Examples:
            >>> explored_perct = self.explored_percentage()
        """
        explored = 0
        for x in range(self.maze_dim):
            for y in range(self.maze_dim):
                if self.path_grid[x][y] > 0:
                    explored += 1
                    
        explored_perct = (explored/self.maze_area) * 100
        
        return explored_perct
    
    
    def log_location(self):
        """Append current robot movement in a log file.
        
        Args: 
            None
            
        Returns: 
            None
        """
        

        # Data format: [Pos-X, Pos-Y, CellValue, Heading]
        x = self.location[0]
        y = self.location[1]
        
        data = [x, y, int(self.path_grid[x][y]), self.heading]
        with open(self.log_filename, 'a') as file:
            json.dump(data, file)
            file.write('\n')
            
            
    def update_heading(self, rotation, movement):
        """Updates the direction of the robot and its location in the maze
          according to the last move
                
        Args: 
            rotation: integer indicating the robot’s rotation on that timestep.
                taking one of three values: -90, 90, or 0 
                for counterclockwise, clockwise, or no rotation (in that order)
            movement: integer indicating the robot’s movement on that timestep
                movement follows the rotiation in the range [-3, 3] inclusive
        
        Returns: 
            None
            
        Examples:
            >>> rotation = 0
            >>> movement = 1
            >>> self.update_heading(rotation, movement)
        """
        
        x = self.location[0]
        y = self.location[1]
        
        if rotation != 0: #change in direction
            if rotation == 90: # turn right
                if self.heading == 'up':
                    self.heading = 'right'
                elif self.heading == 'right':
                     self.heading = 'down'   
                elif self.heading == 'down':
                     self.heading = 'left'  
                elif self.heading == 'left':
                     self.heading = 'up'    
            elif rotation == -90: # turn left
                if self.heading == 'up':
                    self.heading = 'left'
                elif self.heading == 'left':
                     self.heading = 'down'   
                elif self.heading == 'down':
                     self.heading = 'right'  
                elif self.heading == 'right':
                     self.heading = 'up'   
            elif rotation == 180:
                if self.heading == 'up':
                    self.heading = 'down'
                elif self.heading == 'right':
                     self.heading = 'left'   
                elif self.heading == 'down':
                     self.heading = 'up'  
                elif self.heading == 'left':
                     self.heading = 'right'    
                
            
        if self.heading == 'up':
            self.location = [x, y+1]
        elif self.heading == 'right':
            self.location = [x+1, y]
        elif self.heading == 'left':
            self.location = [x-1, y]
        elif self.heading == 'down':
            self.location = [x, y-1]

        