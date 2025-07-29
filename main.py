# This is my attempt at creating Mancala in Python
 
# Import packages
import math
import random

import pygame 
  

 
###########
#Functions#
###########

# Create Game function to create a named game with option of player/CPU
def Game(name):

  # Initialise Pygame bits
  pygame.init() 
  pygame.font.init()
  # Set variables
  global player, skippit, home

  # Initialise Game with a board of 3 seeds and show
  BoardObj=Board(name,3)


  # COLOURS
  white = (255,255,255) 
  black = (0,0,0)
  # CREATING CANVAS 
  screen_size=1000
  circle_size=40
  circle_offset=20
  global canvas,objects
  canvas = pygame.display.set_mode((screen_size,screen_size)) 
  # TITLE OF CANVAS 
  pygame.display.set_caption("Mancala")
  # OBJECTS LIST
  objects = []

  # Player or CPU option
  # cpu=input("Game with Player or CPU?")
  # if cpu=="CPU":
  #     cpu_flag=1
  # else:
  #     cpu_flag=0
  cpu_flag=1 

  # Texts
  font1 = pygame.font.SysFont('freesanbold.ttf', 50)
  for i in range(14):
    globals()["text"+str(i)] = font1.render(str(BoardObj.arr[i]), True, black)
    
  # Define Buttons
  # Homes
  Button(x=60,y=screen_size/2
         ,width=40,height=40
         ,buttonText=BoardObj.arr[13]
         ,font=font1,colour=black
         ,onclickFunction=BoardObj.move,functionParam=13,onePress=True)
  Button(x=screen_size-60,y=screen_size/2
         ,width=40,height=40
         ,buttonText=BoardObj.arr[6]
         ,font=font1,colour=black
         ,onclickFunction=BoardObj.move,functionParam=6,onePress=True)
  # North pits
  for i in range(6):
    Button(x=screen_size-180-i*screen_size/8-circle_offset
          ,y=screen_size/2+50
          ,width=40,height=40
          ,buttonText=BoardObj.arr[i+7]
          ,font=font1,colour=black
          ,onclickFunction=BoardObj.move,functionParam=i+7,onePress=True)
  # South pits
  for i in range(6):
    Button(x=180+i*screen_size/8-circle_offset
           ,y=screen_size/2-50
           ,width=40,height=40
           ,buttonText=BoardObj.arr[i]
           ,font=font1,colour=black
           ,onclickFunction=BoardObj.move,functionParam=i,onePress=True)
  # Loop over game until end
  while True:
    
    # Show board + initialise pygame
        # EVENT CHECKER
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()

    #Determine which player is moving/which pit to skip
    if BoardObj.turn%2==1:
        player=2
        skippit=6
        home=13
    if BoardObj.turn%2==0:
        player=1
        skippit=13
        home=6

    # UPDATES
    canvas.fill(white)

    for object in objects:
      object.process(boardObj=BoardObj)
    pygame.display.flip()

    # Do CPU move if CPU playing
    if cpu_flag==1 and player==2:
      pygame.time.wait(1000)
      BoardObj.move(cpu_move(BoardObj,"random"))  

    # Check if end of game
    if end_check(BoardObj):
       quit_flag=0
       while quit_flag==0:
          for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
              quit_flag=1
       pygame.quit()


# Create Board class to create a named board for a given seed number in each pit
class Board:
  def __init__(self, name, seeds):
    self.name = name
    self.arr = [seeds,seeds,seeds,seeds,seeds,seeds,0,seeds,seeds,seeds,seeds,seeds,seeds,0]
    self.turn = 0


  # Method to choose piece, update board and show
  def move(self,pos):

    if move_valid(self,pos,err_msg=1):
      # Increment turn counter
      self.turn += 1
      #Store number of seeds in numSeed
      numSeed=self.arr[pos]
      #Set seed count in pos to 0
      self.arr[pos]=0
      #Set current pit to next one along
      currentPit=pos+1

      #Increment pits along the chain, starting from next position along until the count runs out
      while numSeed > 0:
          #"Attach" the ends of the boards together
          if currentPit==14:
              currentPit = currentPit-14
          #Check if pit needs skipping
          if currentPit != skippit:
              #Move seed from numSeed to currentPit
              numSeed -= 1
              self.arr[currentPit] += 1
              #Check for free turn (last seed + home)
              if numSeed==0 and currentPit==home:
                  print("Free turn!")
                  # Give another turn
                  self.turn -= 1
              #Check if capture happened (last seed + single seed in pit + opposite side non empty + not home + landing in own pit)
              elif numSeed==0 and self.arr[currentPit]==1 and self.arr[12-currentPit] != 0 and currentPit != home and math.floor(currentPit/7)+1==player:
                  #Capture opponents seeds and remove single seed
                  print("Capture!")
                  self.arr[home] += self.arr[12-currentPit] + 1
                  self.arr[12-currentPit]=0
                  self.arr[currentPit]=0
             
          #Increment current pit
          currentPit += 1
 


# Function to check valid move
def move_valid(board,pos,err_msg):
  #Determine which player is moving/which pit to skip
  if board.turn%2==1:
      player=2
      skippit=6
      home=13
  if board.turn%2==0:
      player=1
      skippit=13
      home=6
  
  if math.floor(pos/7)+1!=player:
    if err_msg==1:
      print("ERROR: Not your turn!")
    return False
  elif pos==6 or pos==13:
    if err_msg==1:
      print("ERROR: Cannot select home pits")
    return False
  elif board.arr[pos]==0:
    if err_msg==1:
      print("ERROR: Cannot select empty pits")
    return False
  elif pos<0 or pos>13:
    if err_msg==1:
      print("ERROR: Pit choice out of range")
    return False
  else:
     return True


# Function to check end of game given board
def end_check(board):
  if sum([board.arr[i] for i in range(0,6)])==0 or sum([board.arr[i] for i in range(7,13)])==0:
    south_score=sum([board.arr[i] for i in range(0,7)])
    north_score=sum([board.arr[i] for i in range(7,14)])
    print("End of game!")
    print("North score: "+str(north_score))
    print("South score: "+str(south_score))
    return True

# Function to show board given board
def show_board(board):
  print("____________")
  print(" "+str(board.arr[12])+" "+str(board.arr[11])+" "+str(board.arr[10])+" "+str(board.arr[9])+" "+str(board.arr[8])+" "+str(board.arr[7])+" ")
  print(str(board.arr[13])+"           "+str(board.arr[6]))
  print(" "+str(board.arr[0])+" "+str(board.arr[1])+" "+str(board.arr[2])+" "+str(board.arr[3])+" "+str(board.arr[4])+" "+str(board.arr[5])+" ")
  print("____________")
  pygame.display.update()

# Function to make a CPU
def cpu_move(board,cpu_option):
   if cpu_option=="random":
      choice_count=0
      # Keep trying to pick random moves until valid one picked (max limit of 100)
      while choice_count <= 100:
        cpu_choice=random.choice([7,8,9,10,11,12])
        if move_valid(board,cpu_choice,err_msg=0):
          return cpu_choice
        choice_count += 1
      print("Cannot pick move")
      quit
 
class Button():
  def __init__(self, x, y, width, height, buttonText, font, colour, onclickFunction=None, functionParam=None, onePress=False):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.onclickFunction = onclickFunction
    self.functionParam = functionParam
    self.onePress = onePress
    self.alreadyPressed = False
    self.font = font
    self.buttonText = buttonText
    self.fillColors = {
    'normal': '#FFFFFF',
    'hover': '#666666',
    'pressed': '#333333',
    }
    self.buttonSurface = pygame.Surface((self.width, self.height))
    self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.buttonSurf = font.render(f"{buttonText}", True, colour)
    objects.append(self)

  def process(self,boardObj):
    mousePos = pygame.mouse.get_pos()
    self.buttonText=boardObj.arr[self.functionParam]
    self.buttonSurf = self.font.render(f"{self.buttonText}", True, (0,0,0))
    self.buttonSurface.fill(self.fillColors['normal'])
    # If mouse on button then hover
    if self.buttonRect.collidepoint(mousePos):
        self.buttonSurface.fill(self.fillColors['hover'])
        # If mouse left click button then press
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
          self.buttonSurface.fill(self.fillColors['pressed'])
          if self.onePress and self.alreadyPressed==False:
            self.onclickFunction(self.functionParam)
            self.alreadyPressed = True
          elif self.onePress==False:
            self.onclickFunction(self.functionParam)
        else:
          # Button not being pressed
          self.alreadyPressed = False
    # Draw text
    self.buttonSurface.blit(self.buttonSurf, [
        self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
        self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
    ])
    canvas.blit(self.buttonSurface, self.buttonRect)

def testfunc():
  return print("test")