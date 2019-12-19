from maze import Maze
import turtle
import sys
import json
 
def draw_maze(testmaze, sq_size, origin):
    # Intialize the window and drawing turtle.
    
    """Draw the maze structure
        
        Args: 
            testmaze:   instance of the Maze
            sq_size:    size of one square
            origin:     innitial coordinates of the robot
            
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
                wally.goto(origin + sq_size * x, origin + sq_size * (y+1))
                wally.setheading(0)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            if not testmaze.is_permissible([x,y], 'right'):
                wally.goto(origin + sq_size * (x+1), origin + sq_size * y)
                wally.setheading(90)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            # only check bottom wall if on lowest row
            if y == 0 and not testmaze.is_permissible([x,y], 'down'):
                wally.goto(origin + sq_size * x, origin)
                wally.setheading(0)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()

            # only check left wall if on leftmost column
            if x == 0 and not testmaze.is_permissible([x,y], 'left'):
                wally.goto(origin, origin + sq_size * y)
                wally.setheading(90)
                wally.pendown()
                wally.forward(sq_size)
                wally.penup()
                
def draw_destination_area(sq_size, origin):
    """Highlight in the maze the destination area
          
         Highlights 2x2 area in the center
        
        Args: 
            sq_size:    size of one square
            origin:     innitial coordinates of the robot
            
        Returns: 
            None
    """
    dest_area = turtle.Turtle()
    dest_area.hideturtle()
    dest_area.penup()
    dest_area.fillcolor('gold')
    dest_area.goto(0 - sq_size + 1, 0 + sq_size - 1) # left border corner
    dest_area.begin_fill()
    for i in range(4):
        dest_area.forward(sq_size * 2 - 2)
        dest_area.right(90)
    dest_area.end_fill()
    
def draw_robot_starting_point(sq_size, origin):
    """Highlight the robot's starting point
        
        Args: 
            sq_size:    size of one square
            origin:     innitial coordinates of the robot
            
        Returns: 
            None
    """
    robot_start_point = turtle.Turtle()
    robot_start_point.color("green")
    robot_start_point.shape("circle")
    robot_start_point.hideturtle()
    robot_start_point.penup()
    robot_start_point.goto(origin + sq_size / 2, origin + sq_size / 2)
    robot_start_point.showturtle()
    
def draw_robot_movement(testmaze, sq_size, origin):
    """Highlight the robot's movement in the maze
        
        Args: 
            sq_size:    size of one square
            origin:     innitial coordinates of the robot
            
        Returns: 
            None
    """
    draw_robot_starting_point(sq_size, origin)
    
    # draw robot movement
    robot = turtle.Turtle()
    
    robot.shape("turtle")
    robot.pencolor("green")
    robot.speed(10)
    
    #set innitial robot position
    robot.hideturtle()
    robot.penup()
    robot.goto(origin + sq_size / 2, origin + sq_size / 2)
    
    
    robot.showturtle()
    robot.pendown()
    
    heading_dict = {"up": 90, "right": 0, "down": 270, "left": 180}

    
    with open("travelled_path.json", 'r') as file:
        file.readline() # skip headline
        for line in file:
            x, y, visited, heading = json.loads(line)
            
            pos_x = origin + sq_size * x + sq_size / 2
            pos_y = origin + sq_size * y + sq_size / 2
            
            robot.setheading(heading_dict[heading]) 
            robot.pendown()
            robot.goto(pos_x, pos_y)
            robot.penup()
            
if __name__ == '__main__':
    """
    This function uses Python's turtle library to draw a 
    - picture of the maze given as an argument when running the script.
    - movement of the robot in the maze
    
    Args: 
        maze:       text file containing the maze to be visualized
        robot_path: json file containing the path travelled by the robot
            
    Returns: 
        None
        
    Examples:
        >>> showmaze.py test_maze_01.txt travelled_path.json
    """
    
    # Create a maze based on input argument on command line.
    testmaze = Maze( str(sys.argv[1]) )
    # maze centered on (0,0), squares are 20 units in length.
    sq_size = 20
    origin = testmaze.dim * sq_size / -2
    
    window = turtle.Screen()
      
    draw_maze(testmaze, sq_size, origin)
    draw_destination_area(sq_size, origin)
    draw_robot_movement(testmaze, sq_size, origin)
    
    window.exitonclick()