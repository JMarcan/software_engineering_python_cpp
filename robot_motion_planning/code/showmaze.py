from maze import Maze
import turtle
import sys
import json
import argparse

class MazeVizualization(object): 
    def __init__(self, sq_size, origin):
        """
        set up attributes of the maze to be visualized
        
        Args: 
            sq_size:  int size of each square in the maze
            origin:   int position of the robot's origin
            
        Returns: 
            None
        """

        self.sq_size = sq_size
        self.origin = origin
        
        self.DEBUG = False # in debug mode are drawn even field numbers to simplify debugging
         
    def draw_maze(self, testmaze):
        """Draw the maze structure
        
            Args: 
                testmaze: instance of the maze
            
            Returns: 
                None
        """
        wally = turtle.Turtle()
        wally.speed(0)
        wally.hideturtle()
        wally.penup()
    
        # iterate through squares one by one to decide where to draw walls
        for x in range(testmaze.dim):
            for y in range(testmaze.dim):
                if not testmaze.is_permissible([x,y], 'up'):
                    wally.goto(self.origin + self.sq_size * x, self.origin + self.sq_size * (y+1))
                    wally.setheading(0)
                    wally.pendown()
                    wally.forward(self.sq_size)
                    wally.penup()

                if not testmaze.is_permissible([x,y], 'right'):
                    wally.goto(self.origin + self.sq_size * (x+1), self.origin + self.sq_size * y)
                    wally.setheading(90)
                    wally.pendown()
                    wally.forward(self.sq_size)
                    wally.penup()

                # only check bottom wall if on lowest row
                if y == 0 and not testmaze.is_permissible([x,y], 'down'):
                    wally.goto(self.origin + self.sq_size * x, self.origin)
                    wally.setheading(0)
                    wally.pendown()
                    wally.forward(self.sq_size)
                    wally.penup()

                # only check left wall if on leftmost column
                if x == 0 and not testmaze.is_permissible([x,y], 'left'):
                    wally.goto(self.origin, self.origin + self.sq_size * y)
                    wally.setheading(90)
                    wally.pendown()
                    wally.forward(self.sq_size)
                    wally.penup()
                    
        self.__draw_destination_area()
                
    def __draw_destination_area(self):
        """Highlight in the maze the destination area
          
            Highlights 2x2 area in the center
        
            Args: 
                None
            
            Returns: 
                None
        """
        dest_area = turtle.Turtle()
        dest_area.hideturtle()
        dest_area.penup()
        dest_area.fillcolor('gold')
        dest_area.goto(0 - sq_size + 1, 0 + self.sq_size - 1) # left border corner
        dest_area.begin_fill()
        for i in range(4):
            dest_area.forward(self.sq_size * 2 - 2)
            dest_area.right(90)
        dest_area.end_fill()
    
    def __draw_robot_starting_point(self):
        """Highlight the robot's starting point
        
            Args: 
                None
            
            Returns: 
                None
        """
        robot_start_point = turtle.Turtle()
        robot_start_point.color("green")
        robot_start_point.shape("circle")
        robot_start_point.hideturtle()
        robot_start_point.penup()
        robot_start_point.goto(self.origin + self.sq_size / 2, self.origin + self.sq_size / 2)
        robot_start_point.showturtle()
    
    def draw_robot_movement(self, robot_path):
        """Highlight the robot's movement in the maze
        
            Args: 
                sq_size:    size of one square
                origin:     innitial coordinates of the robot
            
            Returns: 
                None
        """
        self.__draw_robot_starting_point()
    
        # draw robot movement
        robot = turtle.Turtle()
    
        robot.shape("turtle")
        robot.pencolor("green")
        robot.speed(10)
    
        #set innitial robot position
        robot.hideturtle()
        robot.penup()
        robot.goto(self.origin + self.sq_size / 2, self.origin + self.sq_size / 2)
            
        robot.showturtle()
        robot.pendown()
    
        heading_dict = {"up": 90, "right": 0, "down": 270, "left": 180}

    
        with open(robot_path, "r") as file:
            file.readline() # skip headline
            for line in file:
                step_count, x, y, visited, heading = json.loads(line)
            
                pos_x = self.origin + self.sq_size * x + self.sq_size / 2
                pos_y = self.origin + self.sq_size * y + self.sq_size / 2
            
                if visited == 1:
                    robot.pencolor("green")
                elif visited == 2:
                    robot.pencolor("brown")
                elif visited == 3:
                    robot.pencolor("orange")
                    
                robot.setheading(heading_dict[heading]) 
                robot.pendown()
                robot.goto(pos_x, pos_y)
                 
                if self.DEBUG == True:
                    # in debug mode are drawn even field numbers to simplify debugging
                    text = "[{0}, {1}".format(x, y)
                    robot.write(text, False, align="center", font=("Arial", 5, "normal"))

                robot.penup()
            
if __name__ == '__main__':
    """
    This function uses Python's turtle library to draw a 
    - picture of the maze given as an argument when running the script.
    - movement of the robot in the maze
    
    Args: 
        maze:       path to a text file containing the maze to be visualized
        robot_path: json file containing the path travelled by the robot
            
    Returns: 
        None
        
    Examples:
        >>> showmaze.py test_maze_01.txt travelled_path.json
    """
    
    parser = argparse.ArgumentParser() 
    parser.add_argument("maze", type=str, help="file containing the maze to be visualized")  
    parser.add_argument("robot_path", type=str, help="json file containing the path travelled by the robot") 

    args = parser.parse_args()
    
    maze_path = args.maze
    robot_path = args.robot_path

    # Create a maze based on input argument on command line.
    testmaze = Maze(maze_path)
    
    # maze centered on (0,0), squares are 20 units in length.
    sq_size = 20
    origin = testmaze.dim * sq_size / -2
    
    window = turtle.Screen()
    
    visualisation = MazeVizualization(sq_size, origin)
    visualisation.draw_maze(testmaze)
    visualisation.draw_robot_movement(robot_path)
    
    window.exitonclick()