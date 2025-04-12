# This is my attempt at creating Mancala in Python
 
# Import packages
import math
 
###########
#Functions#
###########
 
# Create Board class to create a named board for a given seed number in each pit
class Board:
  def __init__(self, name, seeds):
    self.name = name
    self.arr = [seeds,seeds,seeds,seeds,seeds,seeds,0,seeds,seeds,seeds,seeds,seeds,seeds,0]
    self.turn = 0
    print("Board name: "+self.name)
    show_board(self)



  # Method to choose piece, update board and show
  def move(self,pos):
      
    #Determine which player is moving/which pit to skip
    if self.turn%2==1:
        player=2
        skippit=6
        home=13
    if self.turn%2==0:
        player=1
        skippit=13
        home=6

    #Check if choosing valid pit (cannot be home pits or empty pits or out of range or not your turn)
    if math.floor(pos/7)+1!=player:
      return print("ERROR: Not your turn!")
    elif pos==6 or pos==13:
        return print("ERROR: Cannot select home pits")
    elif self.arr[pos]==0:
      return print("ERROR: Cannot select empty pits")
    elif pos<0 or pos>13:
      return print("ERROR: Pit choice out of range")
    else:
      # Increment turn counter
      self.turn += 1

      print("Turn number: "+str(self.turn)+" Chosen pit: "+str(pos))

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
     
 
      show_board(self)
 
      #Check if end of game
      end_check(self)

# Function to check end of game given board
def end_check(board):
  if sum([board.arr[i] for i in range(0,6)])==0 or sum([board.arr[i] for i in range(7,13)])==0:
    south_score=sum([board.arr[i] for i in range(0,7)])
    north_score=sum([board.arr[i] for i in range(7,14)])
    print("End of game!")
    print("North score: "+str(north_score))
    print("South score: "+str(south_score))

# Function to show board given board
def show_board(board):
  print("____________")
  print(" "+str(board.arr[12])+" "+str(board.arr[11])+" "+str(board.arr[10])+" "+str(board.arr[9])+" "+str(board.arr[8])+" "+str(board.arr[7])+" ")
  print(str(board.arr[13])+"           "+str(board.arr[6]))
  print(" "+str(board.arr[0])+" "+str(board.arr[1])+" "+str(board.arr[2])+" "+str(board.arr[3])+" "+str(board.arr[4])+" "+str(board.arr[5])+" ")
  print("____________")