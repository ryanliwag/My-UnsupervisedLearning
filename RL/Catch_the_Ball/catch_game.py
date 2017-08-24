import pygame
import random 


#Catch The ball implentation using Deep Q network


#                           ,|     
#                         //|                              ,|
#                       //,/                             -~ |
#                     // / |                         _-~   /  ,
#                   /'/ / /                       _-~   _/_-~ |
#                  ( ( / /'                   _ -~     _-~ ,/'
#                   \~\/'/|             __--~~__--\ _-~  _/,
#           ,,)))))));, \/~-_     __--~~  --~~  __/~  _-~ /
#        __))))))))))))));,>/\   /        __--~~  \-~~ _-~
#       -\(((((''''(((((((( >~\/     --~~   __--~' _-~ ~|
#--==//////((''  .     `)))))), /     ___---~~  ~~\~~__--~ 
#      ))| @    ;-.     (((((/           __--~~~'~~/
#      ( `|    /  )      )))/      ~~~~~__\__---~~__--~~--_
#         |   |   |       (/      ---~~~/__-----~~  ,;::'  \         ,
#         o_);   ;        /      ----~~/           \,-~~~\  |       /|
#               ;        (      ---~~/         `:::|      |;|      < >
#              |   _      `----~~~~'      /      `:|       \;\_____// 
#        ______/\/~    |                 /        /         ~------~
#      /~;;.____/;;'  /          ___----(   `;;;/               
#     / //  _;______;'------~~~~~    |;;/\    /          
#    //  | |                        /  |  \;;,\              
#   (<_  | ;                      /',/-----'  _>
#    \_| ||_                     //~;~~~~~~~~~ 
#        `\_|                   (,~~ 
#                                \~\
                                     


#frame rate per second
FPS = 60

#size of window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

#size of our paddle
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 10

#distance from the edge of the window
PADDLE_BUFFER = 10

#size of our ball
BALL_WIDTH = 10
BALL_HEIGHT = 10

#speed of paddle and ball
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

#Color for player paddle
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
 

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


#draw ball
def draw_ball(ballXPos, ballYPos):
    #small rectangle, create it
    ball = pygame.Rect(ballXPos, ballYPos, BALL_WIDTH, BALL_HEIGHT)
    #draw it
    pygame.draw.rect(screen, WHITE, ball)

#draw paddle
def draw_paddle(paddleXPos):
    #create the paddle
    paddle = pygame.Rect(paddleXPos, WINDOW_HEIGHT - PADDLE_BUFFER - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
    #draw it
    pygame.draw.rect(screen, WHITE, paddle)


def reset_ball():
    ballXPos = random.randint(0,WINDOW_WIDTH - BALL_WIDTH)    
    ballYPos = 10
    return [ballXPos, ballYPos]

def update_ball(paddleXPos, ballXPos, ballYPos, ballYDirection):

    #ball is always falling down :)

    score = 0


    ballYPos = ballYPos + ballYDirection * BALL_Y_SPEED


    #if it hits the bottom, score -1
    if (ballYPos >= WINDOW_HEIGHT):
        score = -1
        [ballXpos, ballYPos] = reset_ball()
        return [score, paddleXPos, ballXPos, ballYPos]
    #if the ball is caught, score +1
    elif (ballYPos >= WINDOW_HEIGHT - (PADDLE_BUFFER + PADDLE_HEIGHT) and ballXPos + BALL_WIDTH <= paddleXPos + PADDLE_WIDTH and ballXPos - BALL_WIDTH >= paddleXPos):
        score = 1
        [ballXpos, ballYPos] = reset_ball()
        return [score, paddleXPos, ballXPos, ballYPos]

        '''
    #if it hits left wall
    if (ballXPos <= 0):
        ballXDirection = 1
    elif (ballXPos >= WINDOW_WIDTH - BALL_WIDTH)
        ballXDirection = -1
        '''
    return [score, paddleXPos, ballXPos, ballYPos]

def update_paddle(action, paddleXPos):
    # if action move left
    if (action[0] == 1):
        paddleXPos = paddleXPos - PADDLE_SPEED
    elif (action[1] == 1):
        paddleXPos = paddleXPos + PADDLE_SPEED

    # BOUNDARIES OF SCREEN

    if (paddleXPos < 0):
        paddleXPos = 0
    elif (paddleXPos > WINDOW_WIDTH - PADDLE_WIDTH):
        paddleXPos = WINDOW_WIDTH - PADDLE_WIDTH

    return paddleXPos


#game
class catch_game:

    def __init__(self):

        # randomize starting postion of ball

        #Initialize player paddle
        self.paddleXPos = WINDOW_WIDTH / 2 - PADDLE_WIDTH / 2

        #BALL SPAWNING 
        [self.ballXPos, self.ballYPos] = reset_ball()

        #BALL DIRECTIONs
        self.ballYDirection = 1
        self.ballXDirection = 0

        #score
        self.tally = 0

    def get_present_frame(self):
         #for each frame, calls the event queue, like if the main window needs to be repainted
        pygame.event.pump()
        #make the background black
        screen.fill(BLACK)
        #draw our paddles
        draw_paddle(self.paddleXPos)
        #draw our ball
        draw_ball(self.ballXPos, self.ballYPos)
        #copies the pixels from our surface to a 3D array. we'll use this for RL
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #updates the window
        pygame.display.flip()
        #return our surface data
        return image_data

    def get_next_frame(self, action):
        pygame.event.pump()
        score = 0
        screen.fill(BLACK)
        #update our paddle
        self.paddleXPos = update_paddle(action, self.paddleXPos)
        draw_paddle(self.paddleXPos)

        #update our vars by updating ball position
        [score, self.paddleXPos, self.ballXPos, self.ballYPos] = update_ball(self.paddleXPos, self.ballXPos, self.ballYPos, self.ballYDirection)
        #draw the ball

        if score != 0:
            [self.ballXPos, self.ballYPos] = reset_ball()
        draw_ball(self.ballXPos, self.ballYPos)
        #get the surface data
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #update the window
        pygame.display.flip()
        #record the total score
        self.tally = self.tally + score
        print("Tally is " + str(self.tally))
        #return the score and the surface data
        return [score, image_data]
