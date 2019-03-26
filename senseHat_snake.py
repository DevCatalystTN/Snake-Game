from random import randint                  #Allows us to place food randomly
from sense_hat import SenseHat              #Library that controls the Sense Hat
from time import sleep                      #Allows us to pause our program



#This is called a class.  It is like a blueprint for creating objects.
#The following link provides a detailed but advanced explanation of classes in python:
#https://www.python-course.eu/python3_object_oriented_programming.php
class snakeGame():

    bg_color = (0,0,0)                      #Background color
    snake_color = (255,255,255)             #Snake color
    food_color = (0,255,0)                  #Food color

        
    #All of the following def statements are called methods.  They are very
    #similar to functions except they are called inside classes and the first
    #argument is always 'self'
    
    #Self refers to the current instance of snakeGame called 'snake' (see line 157).
    #Most of the variables have 'self.' infront of them.  This means they are
    #attributes of the instance 'snake' and can be referenced throughout the program
    #with snake.attribute or self.attribute.
        
    #Method to initialize game.  This doesn't run until we call 'snake.startGame()'	(line 158)
    def startGame(self):
        sense.clear(self.bg_color)          #Sets background to bg_color
        self.direction = 'up'               #Snake starts moving up
        self.length = 3                     #Initial snake length
        self.tail = [(4,4),(4,5),(4,6)]     #Starting position  
		
        #Draws snake
        for pixel in self.tail:
            sense.set_pixel(pixel[0],pixel[1],self.snake_color)
		
        self.createFood()                   #This method places food randomly					
        self.score = 0                      #Initializes score to zero
        
        #The following listens for joystick presses and calls move method.
        #If move returns True, keep playing.  If it returns false, game ends.
        playing = True
        while playing:
            sleep(0.5)
            for event in sense.stick.get_events():
                self._handle_event(event)
            playing = self.move()
    

    #This method is called during the "while playing" loop above.  
    #It changes the direction attribute of the snake after checking that 
    #it's not moving in the opposite direction.
    def _handle_event(self, event):
        if event.direction == 'up':
            if self.direction != 'down':
                self.direction = 'up'
        elif event.direction == 'down':
            if self.direction != 'up':
                self.direction = 'down'
        elif event.direction == 'left':
            if self.direction != 'right':
                self.direction = 'left'
        elif event.direction == 'right':
            if self.direction != 'left':
                self.direction = 'right'
    

    #This method places food in a random location.  It creates a random integer
    #for x and y and checks if that location is inside the snake using
    #.checkCollision method.  If there is a collision, it generates a new x and y.
    def createFood(self):
        bad_food_placement = True
        while bad_food_placement:
            x = randint(0,7)                #'x' and 'y' don't have 'self.' infront
            y = randint(0,7)                #of them, so they are local to this method only. 
            bad_food_placement = self.checkCollision(x,y)
        self.food = [x,y]
        sense.set_pixel(x,y,self.food_color)



    #This method checks if the snake has hit a wall or itself.  
    #Also used in createFood()
    def checkCollision(self, x, y):
        if x > 7 or x < 0 or y > 7 or y < 0:
            return True
        else:
            for segment in self.tail:
                if segment[0] == x and segment[1] == y:
                    return True  
            return False

    #This method is used by move.  It adds a segment to the front of the snake and
    #deletes a segment from the end of a snake using .pop().  If the snake just ate
    #its length would increase by one and the last segment would not be deleted.
    def addSegment(self, x, y):
        sense.set_pixel(x,y,self.snake_color)
        self.tail.insert(0, (x, y))
		
        if len(self.tail) > self.length:
            lastSegment = self.tail[-1]
            sense.set_pixel(lastSegment[0],lastSegment[1], self.bg_color)
            self.tail.pop()
      
    
    #This method is responsible for snake movement.  It creates a new segment depending
    #on the snake.direction attribute.  If the new segment passes .checkCollision
    #it calls .addSegment.  If there is a collision, endgame procedure occurs.
    def move(self):
        newSegment = [self.tail[0][0], self.tail[0][1]]
        if self.direction == 'up':
            newSegment[1] -= 1
        elif self.direction == 'down':
            newSegment[1] += 1
        elif self.direction == 'left':
            newSegment[0] -= 1
        elif self.direction == 'right':
            newSegment[0] += 1
          
        if self.checkCollision(newSegment[0],newSegment[1]):
            sense.show_message("GAME OVER", scroll_speed = 0.05)
            sense.show_message("Score = " + str(self.score), scroll_speed = 0.05)
            return False
			
        else:
            self.addSegment(newSegment[0], newSegment[1])
		
            #Checks if snake just ate.  If so, length and score are increased and
            #new food is created.
            if newSegment[0] == self.food[0] and newSegment[1] == self.food[1]:
                self.length += 1
                self.score += 10 
                self.createFood()
			
            return True

#The if statement just ensures that senseHat_snake.py is the main module running,
#not an imported module.  This is unnecessary here, but it is a very common 
#convention.  For further information, see the following Stack Overflow post:
#https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    sense = SenseHat()                      #   This creates an instance of SenseHat()
                                            #called sense
                                            
    #This is an infinite loop that starts the game when the user presses the
    #joystick.  When the game finishes, it deletes the game and starts over.
    while True:
        sense.show_message("PRESS JOY TO BEGIN", scroll_speed = 0.05)
        event = sense.stick.wait_for_event(emptybuffer=True)
        if event.action == 'pressed':
            snake = snakeGame()
            snake.startGame()
            del snake
		
	
	
	

	
	
	
	
	