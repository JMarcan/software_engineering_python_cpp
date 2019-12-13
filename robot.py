import numpy as np

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
        
        self.visited_fields =[[0 for j in range(maze_dim)] for i in range(maze_dim)]
    

    def wall_follower(self, sensors):
        # wall follower algo will not work for non simple-connected type of maze
        movement = 0
        rotation = 0
        
        if sensors[1] > 0:
            movement = 1
            rotation = 0
            print ("move 1 forward")
        else:
            movement = 1
            rotation = 90
            print ("move right")
            
        return rotation, movement
    
    
    def tremaux_algo(self, sensors):
        movement = 0
        rotation = 0
        
        if self.visited_fields[self.location[0]][self.location[1]] == True:
            print ("Warrning: Looping in the same location")

        self.visited_fields[self.location[0]][self.location[1]] = True
        
        if sensors[1] > 0:
            movement = 1
            rotation = 0
            print ("move 1 forward")
        else:
            movement = 1
            rotation = 90
            print ("move right")
            
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

       
        # wall follower algo will not work for this type of maze
        rotation, movement = self.tremaux_algo(sensors)
        
  
      
       

        return rotation, movement