from maze import Maze
import turtle
import sys
import json
 
def draw_maze(testmaze, window):
    # Intialize the window and drawing turtle.
    wally = turtle.Turtle()
    wally.speed(0)
    wally.hideturtle()
    wally.penup()

    # maze centered on (0,0), squares are 20 units in length.
    sq_size = 20
    origin = testmaze.dim * sq_size / -2

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

def draw_robot_movement(testmaze, window):
    # maze centered on (0,0), squares are 20 units in length.
    sq_size = 20
    origin = testmaze.dim * sq_size / -2
    
    # mark starting point
    robot_start_point = turtle.Turtle()
    robot_start_point.color("green")
    robot_start_point.shape("circle")
    robot_start_point.hideturtle()
    robot_start_point.penup()
    robot_start_point.goto(origin + sq_size / 2, origin + sq_size / 2)
    robot_start_point.showturtle()
    
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
    '''
    This function uses Python's turtle library to draw a picture of the maze
    given as an argument when running the script.
    '''
    # Create a maze based on input argument on command line.
    testmaze = Maze( str(sys.argv[1]) )
    
    window = turtle.Screen()
    
    draw_maze(testmaze, window)
    draw_robot_movement(testmaze, window)
    
    window.exitonclick()