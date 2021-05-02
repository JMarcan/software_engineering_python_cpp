import numpy as np
import json
import random
from sys import stderr

class Robot(object):
    def __init__(self, maze_dim):
        """
        set up attributes that the robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        
        Args: 
                maze_dim: int providing maze dimensions 
                (e.g. 12 means that maze has dimensions 12x12)
            
        Returns: 
                None
        """
        self.maze_dim = maze_dim
        self.maze_area = maze_dim ** 2.
        
        # robot location tracking variables
        self.location_orig = [0, 0]
        self.location = [0, 0]
        self.location_last = [0, 0]
        
        self.heading = 'up'
        
        # variables to create robot's internal map of the maze
        self.maze_grid = np.zeros((maze_dim, maze_dim), dtype=np.int) # Grid for wall locations for each maze.
        self.path_grid = np.zeros((maze_dim, maze_dim), dtype=np.int)
        self.visited_grid = np.zeros((maze_dim, maze_dim), dtype=np.int) #visited paths used for Treumax algo
        self.visited_grid_previous_heading = np.zeros((maze_dim, maze_dim), dtype=object) #visited paths used for Treumax algo
        
        # measuring number of steps in which the maze was solved
        self.step_count = 0
        
         # Maximum allowed movement units per turn
        self.max_movement = 3
        
        self.backtracking = False
        self.is_reversing = False  #to indicate that 180 degrees turn must be completed (done by two right turns)
        
        
        # Robot's operational mode
        # This decides robot's action when next_move() is called.
        self.mode = "explore"
        
        # Flag that indicates the first step of exploration
        self.is_beginning = True
        
        #possible path grid values
        self.UNVISITED = 0
        self.VISITED = 1
        self.DOUBLE_VISITED = 2
        self.SHORTEST = 3 # marking shortest path, so it can be visualized
        
        # Numbers assigned to open walls in cells.
        self.wall_values = {'up': 1,
                            'right': 2,
                            'down': 4,
                            'left': 8}
        
        # Internal robot's maze cell map
        # Each number represents a four-bit number that has a bit value of 0 if an edge is closed (walled) and
        # 1 if an edge is open (no wall); the 1s register corresponds with the upwards-facing side, the 2s register
        # the right side, the 4s register the bottom side, and the 8s register the left side. For example,
        # the number 10 means that a square is open on the left and right,
        # with walls on top and bottom (0*1 + 1*2 + 0*4 + 1*8 = 10).
        # The index origin (0, 0) is at the bottom left
        
        self.maze_map = [[0 for _ in range(maze_dim)] for _ in range(maze_dim)]
        
        # Corresponding new headings after rotating
        self.dict_rotation = {'up': ['left', 'right'],
                              'right': ['up', 'down'],
                              'down': ['right', 'left'],
                              'left': ['down', 'up']}
        # Opposite directions
        self.opposite = {'up': 'down',
                         'right': 'left',
                         'down': 'up',
                         'left': 'right'}
        
         # Vectors for different directions
        self.direction_to_vec = {'up': [0, 1],
                                 'right': [1, 0],
                                 'down': [0, -1],
                                 'left': [-1, 0]}
        
        # Rotation matrices
        self.rot_matrices = {'left': np.array([(0, 1), (-1, 0)]),
                             'up': np.array([(1, 0), (0, 1)]),
                             'right': np.array([(0, -1), (1, 0)])}
         # Dictionary for backtracking, translates robot's headings into direction relative to the maze
        self.direction_to_rotation = {
                heading: {directions[0]: -90, directions[1]: 90}
                for heading, directions in self.dict_rotation.items()}
        
        # Policy grid which will be created after performing a search algorithm.
        self.policy_grid = [['' for _ in range(self.maze_dim)] for _ in
                            range(self.maze_dim)]
        # Text file in which the travelled path will be logged.
        self.log_filename = 'robot_path.json'
        
        # create file logging visited path and write head line
        with open(self.log_filename, 'w+') as file:
            file.write('[step_count, robot_x, robot_y, visited, heading]\n')
            
        # decides whether debug message will be displayed
        self.DEBUG = False
        
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
        # (done in two steps by turning right)        
        else:
            movement = 0
            rotation = 90
            self.print_debug("dead end, turn to the right, no movement")
            
        return rotation, movement
   
    
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
            elif direction == 'up':
                global_dir = self.heading

            # Get the corresponding wall value for an wall opening in the given direction
            wall_value = self.wall_values[global_dir]
            # Update the current map cell with the new wall value
            self.maze_map[self.location[0]][self.location[1]] |= wall_value
            # Rotate robot's direction vector to given direction
            dir_vec = np.dot(movement_vec, self.rot_matrices[direction])
            # Get the wall opening value for the next cell
            wall_value = self.wall_values[self.opposite[global_dir]]
            # Update the next map cell with the opening that can be seen from this cell.
            # maps entries to deadends.
            self.maze_map[self.location[0] + dir_vec[0]][
                self.location[1] + dir_vec[1]] |= wall_value   
 
            
    def next_move(self, sensors):
        """
        This function determines the next move the robot should make,
        based on the input from the sensors after its previous move. 
        
         Args: 
            sensors: inputs are a list of three distances from the robot's left, 
                front, and right-facing sensors, in that order
        
        Returns: 
            rotation: indicates desired robot rotation (if any) as a number: 
                0 for no rotation, +90 for a 90-degree rotation clockwise, 
                and -90 for a 90-degree rotation counterclockwise. 
                Other values will result in no rotation.
            movement: indicates robot movement, and the robot will attempt 
                to move the number of indicated squares: a positive number 
                indicates forwards movement, while a negative number indicates 
                backwards movement. The robot may move a 
                maximum of three units per turn. Any excess movement is ignored.
                
            If the robot wants to end a run (e.g. during the first training run in
            the maze) then returing the tuple ('Reset', 'Reset') will indicate to
            the tester to end the run and return the robot to the start.  
        """
        
        rotation = 0
        movement = 0
        
        # measure number of steps to solve maze
        self.step_count +=1 
        self.print_debug("=== {0}.step ===".format(self.step_count))
        
        if self.mode == "explore":
            # explore and map the complete maze
            rotation, movement = self.explore(sensors)
            if rotation == "Reset":
                # leave exploration mode
                return rotation, movement
            
            self.log_location() # store location before its movemenet
            # print location and explore maze percentage
            x = self.location[0]
            y = self.location[1]
            self.path_grid[x][y] = 1    
            print("Robot has explored {:04.2f}% of the maze.\n".format(self.explored_percentage()))
            
        elif self.mode == "search":
            self.find_shortest_path()
            self.start_racing()
        elif self.mode == "race":
            # Race to the goal room on the shortest path through the maze.
            # The robot still moves iteratively on every call of next_move().
            rotation, movement = self.race_to_goal()
            # Perform rotations and movements determined by the racing function
            # This marks the racing path and logs it to the logfile
            self.mark_path(self.SHORTEST)
            self.log_location()
        
        if self.movement_allowed(sensors, rotation, movement) == False:
            # check that intended movement is possible
            print("ERROR: Robot cannot move in a chosen direction. Stopping the robot. [Heading: {0} | Rotation: {1} | Movement: {2} | Location: {3}]".format(self.heading, rotation, movement, self.location), file=stderr)
            rotation = 0
            movement = 0
        else:
            self.update_heading(rotation, movement)
            print("Location new: {0} | location_last: {1}".format(self.location, self.location_last))


        return rotation, movement
    def start_racing(self):
        """Start the robot's racing mode
            
        Args: 
            None
        
        Returns: 
            None
        """
        self.mode = "race"
        self.step_count = 0
        self.mark_path(self.SHORTEST)
        self.log_location()
        
    def race_to_goal(self):
        """Move robot on the shortest path to the goal
            
        Args: 
            None
        
        Returns: 
            rotation, movement
            - rotation: integer indicating the robot’s rotation on that timestep.
                taking one of three values: -90, 90, or 0 
                for counterclockwise, clockwise, or no rotation (in that order)
            - movement: integer indicating the robot’s movement on that timestep
                movement follows the rotiation in the range [-3, 3] inclusive     
        """

        rotation = 0
        movement = 0
        
        # First, collect up to three actions in a line if they are the same
        actions = []
        x, y = self.location[0], self.location[1]
        abort = False
        while len(actions) < self.max_movement and not abort:
            current_action = self.policy_grid[x][y]

            if not current_action:
                abort = True
            else:
                actions.append(current_action)
                dx, dy = self.direction_to_vec[current_action]
                nx, ny = x + dx, y + dy
                # Check if the next cell (nx, ny) has the same action.
                if (0 <= nx < self.maze_dim and
                        0 <= ny < self.maze_dim and
                        self.policy_grid[nx][ny] == current_action):
                    x = nx
                    y = ny
                else:
                    abort = True

        # Secondly, set rotation and movement according to the collected actions
        rotation = self.direction_to_rotation[self.heading].get(
            actions[0], 0)
        movement = len(actions)
        
        return rotation, movement
        
    def movement_allowed(self, sensors, rotation, movement):
        """Check if desired movement is allowed or blocked by wall
            
        Args: 
            sensors:  three values input from the robot's sensors
            rotation: integer indicating the robot’s rotation on that timestep.
                taking one of three values: -90, 90, or 0 
                for counterclockwise, clockwise, or no rotation (in that order)
            movement: integer indicating the robot’s movement on that timestep
                movement follows the rotiation in the range [-3, 3] inclusive 
        
        Returns: 
            True if movement is allowed. False if not.
            
        Examples:
            >>> rotation = 0
            >>> movement = 1
            >>> is_movement_allowed = self.movement_allowed(sensors, rotation, movement)
        """
        if rotation == -90:
            return sensors[0] >= movement
        elif rotation == 90:
            return sensors[2] >= movement
        elif rotation == 0:
            return sensors[1] >= movement
        else:
            return False
        
    def explore(self, sensors):
        """Explore a maze using Trémaux' algorithm
                
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
            >>> rotation, movement = self.explore(sensors)
        """
        rotation = 0
        movement = 0
        
        if self.is_beginning:
            # This prevents the robot from immediately cancelling exploration
            self.is_beginning = False
            
        elif self.finished_exploration():
            # When back at the start, end the exploration
            rotation, movement = self.end_exploration()

            return rotation, movement
        
        # When in reversing mode, just finish the rotation and move forward
        if self.is_reversing:
            rotation = 90
            movement = 1
            self.is_reversing = False
            self.print_debug("explore: Reversing. Decided rotation: {0} | Movement: {1} | Visited grid: {2} | Backtracking: {3}".format(rotation, movement, self.visited_grid[self.location[0], self.location[1]], self.backtracking))

            return rotation, movement
        
        # Translate sensor readings into unblocked directions
        open_directions = self.check_open_directions(sensors)
        # Update the internal mapping of the maze
        self.update_map(open_directions)

        # --------------------------------------
        # Trémaux' algorithm
        # --------------------------------------

        x = self.location[0]
        y = self.location[1]
        
        if len(open_directions) == 0:
            # Robot is at a deadend
            # Start backtracking
            rotation, movement = self.start_backtracking()
            self.mark_path(self.DOUBLE_VISITED)
            self.print_debug("explore: 0 - START backtracking. No open directions. ")

        elif len(open_directions) == 1:
            # Robot is on a path to the next junction
            rotation, movement = self.follow_path(self.random_path_choice(open_directions[0]))
            if self.backtracking == True:
                self.mark_path(self.DOUBLE_VISITED)
            else:
                self.mark_path(self.VISITED)

        elif len(open_directions) > 1:
            
            if self.path_is(self.UNVISITED):
                
                # Store the direction to the path which has led to this junction, used for backtracking.
                self.visited_grid_previous_heading[x][y] = self.opposite[self.heading]
                
                unvisited_paths = self.get_paths(open_directions, self.UNVISITED)
                if len(unvisited_paths) > 0:
                    # Still unvisited paths from this junction
                    
                    rotation, movement = self.follow_path(self.random_path_choice(unvisited_paths))
                    # Mark this junctions for the first time
                    self.mark_path(self.VISITED)
                    
                    if self.backtracking == True:
                        self.backtracking = False
                else:
                    # no more unvisited paths from this junction, threat is as dead-end
                    rotation, movement = self.start_backtracking()
                    self.mark_path(self.DOUBLE_VISITED)
                    
            elif self.path_is(self.VISITED):
                # Robot has already visited this junction
                if self.backtracking == True:
                    # robot stepped into already visited junction while backtracking
                    unvisited_paths = self.get_paths(open_directions, self.UNVISITED)
                    if len(unvisited_paths) > 0:
                        # Still unvisited paths from this junction
                        rotation, movement = self.follow_path(self.random_path_choice(unvisited_paths))
                        
                        if self.backtracking == True:
                            self.backtracking = False
                    else:
                        # no more unvisited paths from this junction, threat is as dead-end
                        
                        if self.location == self.location_last:
                            # prevention to stucking in backtracking loop in case it goes through multiple junctions
                            # robot stays on the same position, choose random direction visite once
                            visited_paths = self.get_paths(open_directions, self.VISITED)
                            if len(visited_paths) > 0:
                                rotation, movement = self.follow_path(self.random_path_choice(visited_paths))
                                self.print_debug("explore: 2: Warrning: Backtracking stuck robot in the same position. Choosing random path VISITED_ONCE. ")
                                self.mark_path(self.DOUBLE_VISITED)
                            else:
                                self.print_debug("explore: 3: Error: Backtracking stuck robot in the same position. No path visited less than TWICE left")

                        else:
                            rotation, movement = self.continue_backtracking()
                            self.mark_path(self.DOUBLE_VISITED)
                else:
                    # robot stepped into already visited junction while NOT backtracking
                    # threat it as dead-end
                    rotation, movement = self.start_backtracking()

        self.print_debug("explore: Decided rotation: {0} | Movement: {1} | Visited grid: {2} | Backtracking: {3}".format(rotation, movement, self.visited_grid[self.location[0], self.location[1]], self.backtracking))
        
        return rotation, movement
    
    def find_shortest_path(self):
        """Find the shortest path to the  using breadth-first search 
             and plan robot next actions based on this
        Args: 
            None
        
        Returns: 
            None
        """

        init = [self.location_orig[0], self.location_orig[1]]

        # The center cells which make up the goal room.
        goal_room = [[self.maze_dim / 2, self.maze_dim / 2],
                     [self.maze_dim / 2 - 1, self.maze_dim / 2],
                     [self.maze_dim / 2, self.maze_dim / 2 - 1],
                     [self.maze_dim / 2 - 1, self.maze_dim / 2 - 1]]

        # This could be used to change the movement costs.
        cost = 1

        # Connects movement delta vectors and
        # their corresponding directional actions.
        delta_to_action = {(0, 1): 'up',
                           (1, 0): 'right',
                           (0, -1): 'down',
                           (-1, 0): 'left'}

        # This grid holds the action delta at every position of the maze.
        delta_grid = [[(0, 0) for _ in range(self.maze_dim)] for _ in
                      range(self.maze_dim)]

        # Initialize some values and lists for the search algorithm
        g = 0
        open_cells = [[g, init[0], init[1]]]
        visited = [init]
        end = []

        # Search through the maze with Dijkstra.
        while True:

            if not open_cells:
                break

            open_cells.sort()
            # Get the cell from the open list with the lowest cost-value (G-Value).
            g, x, y = open_cells.pop(0)

            if [x, y] in goal_room:
                # Stop when entering the goal room.
                end = [x, y]
                break

            # Check the current position in the maze map for wall openings.
            # For every wall opening, the corresponding directional delta vector is added
            # to the deltas list. This essentially creates a list of deltas to cells connected to
            # the current cell in the map.
            deltas = []
            for direction, value in self.wall_values.items():
                if self.maze_map[x][y] & value != 0:
                    deltas.append(self.direction_to_vec[direction])

            # Now, loop through all the connected cells
            for dx, dy in deltas:
                # Use delta to calculate the coords of the next cell (nx, ny)
                nx, ny = x + dx, y + dy
                if [nx, ny] not in visited:
                    # The next cell is not yet visited
                    open_cells.append([g + cost, nx, ny])
                    visited.append([nx, ny])
                    # Save the action delta vector needed to get to this next cell (nx, ny)
                    delta_grid[nx][ny] = (dx, dy)

        # Create policy path by travelling from end to start
        x, y = end
        self.policy_grid[x][y] = '*'
        while [x, y] != init:
            # Apply the previously saved action deltas backwards.
            nx = x - delta_grid[x][y][0]
            ny = y - delta_grid[x][y][1]
            # Save the action string to the policy grid.
            self.policy_grid[nx][ny] = delta_to_action[delta_grid[x][y]]
            # Continue with the next position
            x, y = nx, ny
        
    def random_path_choice(self, paths):
        """
        Make predictable random path choice, to make robot movement in a known maze predictable
        which simplified analysis

        Args: 
            paths as tuple
                with possible values "up" and "right" and "left"
        
        Returns: 
            path as string
                with possible values: "up" or "right" or "left"
        """
        
        if "up" in paths:
            return "up"
        
        elif "right" in paths:
            return "right"
        elif "left" in paths:
            return "left"
 
        else:
            print("The unkown path in " + str(paths), file=stderr)
            return "error"
        

    def continue_backtracking(self):
        """
        Continue backtracking. Follow the way from which robot came from

        Args: 
            None
        
        Returns: 
            rotation, movement
            
            - rotation: integer indicating the robot’s rotation on that timestep.
                taking one of three values: -90, 90, or 0 
                for counterclockwise, clockwise, or no rotation (in that order)
            - movement: integer indicating the robot’s movement on that timestep
                movement follows the rotiation in the range [-3, 3] inclusive
        """

        movement = 1
        rotation = 0
        
        # Get direction to which we wish to backtrack to
        direction = self.visited_grid_previous_heading[self.location[0]][self.location[1]]
        # Translate that direction into a possibly needed rotation of the robot,
        # considering the current heading
        rotation = self.direction_to_rotation[self.heading].get(direction,0)
        
        self.print_debug("Continue backtracking | direction: {0} | rotation: {1}".format(direction, rotation))
        
        return rotation, movement

    
    def get_paths(self, open_directions, value):
        """
        Return paths possible to take from the junction with a given value

        Args: 
            open_directions: list of possible directions from the junction
            value: value of paths to be filtered for 
             - self.UNVISITED or self.VISITED
        
        Returns: 
            direction_with_value: list of possible directions from the junction
                with a given value
        """
        direction_with_value = []
        
        for direction in open_directions:
            next_step_location = self.get_next_step_coordinates(direction, 1)
            if self.visited_grid[next_step_location[0]][next_step_location[1]] == value:
                direction_with_value.append(direction)
                
        return direction_with_value
     
    def path_is(self, value, x=None, y=None):
        """
        Returns true if the path at the given position has the specified value.
        If no position parameters are given, checks at the robot's current position
        
        Args: 
            value: value agains which the path is tested 
             - self.UNVISITED or self.VISITED or self.DOUBLE_VISITED
        
        Returns: 
            True if path has given value. False otherwise
        """
        
        if x is None:
            x = self.location[0]
        if y is None:
            y = self.location[1]

        return self.visited_grid[x][y] == value
    def follow_path(self, direction):
        """Follow path in the given direction.

        Args: 
            direction: direction in which shall the robot move
                - "left" or "up" or "right"
        
        Returns: 
           rotation, movement
            
            - rotation: integer indicating the robot’s rotation on that timestep.
                taking one of three values: -90, 90, or 0 
                for counterclockwise, clockwise, or no rotation (in that order)
            - movement: integer indicating the robot’s movement on that timestep
                movement follows the rotiation in the range [-3, 3] inclusive
        """
        
        rotation = 0
        movement = 0
        
        if direction == "left":
            rotation = -90
            movement = 1
        elif direction == "up":
            rotation = 0
            movement = 1
        elif direction == "right":
            rotation = 90
            movement = 1
        else:
            print(
                "Can't follow path, chosen direction " + direction + "is invalid.",
                file=stderr)
        
        return rotation, movement
    
    def mark_path(self, new_value=None):
        """
        Mark a traveled path to a specified value. 
        
        Args: 
            new_value: value for the path
             - self.UNVISITED or self.VISITED or self.DOUBLE_VISITED or self.SHORTEST
        
        Returns: 
            None
        """
        
        x = self.location[0]
        y = self.location[1]
        
        if new_value is None:
            if self.visited_grid[x][y] == self.UNVISITED:
               self.visited_grid[x][y] = self.VISITED
            else:
               self.visited_grid[x][y] = self.DOUBLE_VISITED
              
        else:
            self.visited_grid[x][y] = new_value

            
    def check_open_directions(self, sensors):
        """Check which directions are not blocked return them.
        
        Args: 
            sensors: list of three int values indicating number of open squares 
                in front of the left, center, and right sensors (in that order)
        
        Returns: 
            open_directions
                - list of directions with possible values "left" and "up" and "right"
        """
       
        open_directions = []
        if sensors[0] > 0:
            open_directions.append('left')
        if sensors[1] > 0:
            open_directions.append('up')
        if sensors[2] > 0:
            open_directions.append('right')
        return open_directions
    
    def start_backtracking(self):
        """Start reversing the robot to perform a 180 degree rotation.
        
        Args: 
            None
        
        Returns: 
            None
        """
        self.is_reversing = True
        self.backtracking = True
        
        movement = 0
        rotation = 90
        
        return rotation, movement
        
    def finished_exploration(self):
        """Returns true when the robot is back at the origin.
        
        Args: 
            None
        
        Returns: 
            None
        """
        
        return self.location == self.location_orig
    
    def end_exploration(self):
        """Stop the robot's exploration mode and reset the run.
        
        Args: 
            None
        
        Returns: 
            None
        """
        
        print("Robot has reached the origin again. Finishing exploration.")
        # Reset some localization-specific values
        self.heading = "up"
        self.location = self.location_orig

        self.mode = "search"

        # Set the reset signals
        movement = "Reset"
        rotation = "Reset"
        
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
        # Data format: [step_count, Pos-X, Pos-Y, CellValue, Heading]
        x = self.location[0]
        y = self.location[1]

        data = [self.step_count, x, y, int(self.visited_grid[x][y]), self.heading]
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
        
        self.location_last = self.location
        
        x = self.location[0]
        y = self.location[1]
        
        
        # update heading
        if rotation != 0: #change in direction
            if rotation == 90: # turn right
                if self.heading == "up":
                    self.heading = "right"
                elif self.heading == "right":
                     self.heading = "down"   
                elif self.heading == "down":
                     self.heading = "left"  
                elif self.heading == "left":
                     self.heading = "up"    
            elif rotation == -90: # turn left
                if self.heading == "up":
                    self.heading = "left"
                elif self.heading == "left":
                     self.heading = "down"   
                elif self.heading == "down":
                     self.heading = "right"  
                elif self.heading == "right":
                     self.heading = "up"   
            elif rotation == 180:
                if self.heading == "up":
                    self.heading = "down"
                elif self.heading == "right":
                     self.heading = "left"   
                elif self.heading == "down":
                     self.heading = "up"  
                elif self.heading == "left":
                     self.heading = "right"    
                
        # update position
        if movement > 0:
            if self.heading == "up":
                self.location = [x, y+movement]
            elif self.heading == "right":
                self.location = [x+movement, y]
            elif self.heading == "left":
                self.location = [x-movement, y]
            elif self.heading == "down":
                self.location = [x, y-movement]
                
    def get_next_step_coordinates(self, robot_rel_heading, movement):
        """Return coordinates of the next potential move in a given direction
                
        Args: 
            robot_rel_heading: string indicating relative change of the robot heading
                taking one of three values: "up", "right", "left"
            movement: integer indicating the robot’s movement on that timestep
                movement follows the rotiation in the range [-3, 3] inclusive
                
        Returns: 
            robot_location: integer [location_x, location_y] 
            indicating coordinates for the potential move in a given direction
            
        Examples:
            >>> robot_rel_heading = "up"
            >>> movement = 1
            >>> self.get_next_step_coordinates(robot_rel_heading, movement)
        """
        
        robot_heading = robot_rel_heading
        robot_location = [0, 0]
        
        x = self.location[0]
        y = self.location[1]
        
        # Transform relative heading to the real heading relative to the maze
        if robot_rel_heading == "up": #robot intends to continue in the direction
            robot_heading = self.heading
        elif robot_rel_heading == "right": #robot intends to turn right
            if self.heading == "up":
                robot_heading = "right"
            elif self.heading == "right":
                 robot_heading = "down"
            elif self.heading == "down":
                robot_heading = "left"
            else: # robot is heading left relative to the maze
                    robot_heading = "up"
        elif robot_rel_heading == "left": #robot intends to turn left
            if self.heading == "up":
                    robot_heading = "left"
            elif self.heading == "right":
                     robot_heading = "up"
            elif self.heading == "down":
                    robot_heading = "right"
            else: # robot is heading left relative to the maze
                    robot_heading = "down"
        
        if robot_heading == "up":
            robot_location = [x, y+movement]
        elif robot_heading == "right":
            robot_location = [x+movement, y]
        elif robot_heading == "left":
            robot_location = [x-movement, y]
        else: # robot is heading down
            robot_location = [x, y-movement]
            
        return robot_location
                