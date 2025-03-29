# This is my attempt at creating Mancala in Python
 
# Import packages
import math
 
###########
#Functions#
###########
 
# Create Board class to create a named board for a given seed number in each pit
class Board:
  def __init__(self, name, seeds, turn):
    self.name = name
    self.arr = [seeds,seeds,seeds,seeds,seeds,seeds,0,seeds,seeds,seeds,seeds,seeds,seeds,0]
    self.turn = 0
    print("Board name: "+self.name)
    self.show_board()

  # Method to show state of board (simple for now...)
  def show_board(self):
    print("____________")
    print(" "+str(self.arr[12])+" "+str(self.arr[11])+" "+str(self.arr[10])+" "+str(self.arr[9])+" "+str(self.arr[8])+" "+str(self.arr[7])+" ")
    print(str(self.arr[13])+"           "+str(self.arr[6]))
    print(" "+str(self.arr[0])+" "+str(self.arr[1])+" "+str(self.arr[2])+" "+str(self.arr[3])+" "+str(self.arr[4])+" "+str(self.arr[5])+" ")
    print("____________")
 
  # Method to choose piece, update board and show
  def move(self,pos):
 
    #Determine which player is moving/which pit to skip
    if self.turn%2==1:
        player=2
        skippit=13
        home=6
    if self.turn%2==0:
        player=1
        skippit=6
        home=13
    print("pos="+str(pos)+"turn="+str(self.turn)+""+"player="+str(player))
    #Check if choosing valid pit (cannot be home pits or empty pits or out of range or not your turn)
    if pos==6 or pos==13:
        return print("ERROR: Cannot select home pits")
    elif self.arr[pos]==0:
      return print("ERROR: Cannot select empty pits")
    elif pos<0 or pos>13:
      return print("ERROR: Pit choice out of range")
    elif math.floor(pos/7)+1!=player:
      return print("ERROR: Not your turn!")
    else:
      print("Turn number: "+str(self.turn))
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
            turn -= 1
          #Check if capture happened (last seed + single seed in pit + opposite side non empty + not home)
          elif numSeed==0 and self.arr[currentPit]==1 and self.arr[12-currentPit] != 0 and currentPit != home:
            #Capture opponents seeds and remove single seed
            print("Capture!")
            self.arr[home] += self.arr[12-currentPit] + 1
            self.arr[12-currentPit]=0
            self.arr[currentPit]=0
             
          #Increment current pit
          currentPit += 1
     
 
      self.show_board()
 
      #Check if end of game
      if self.arr[0]+self.arr[1]+self.arr[2]+self.arr[3]+self.arr[4]+self.arr[5]==0 or self.arr[7]+self.arr[8]+self.arr[9]+self.arr[10]+self.arr[11]+self.arr[12]==0:
          south_score=self.arr[0]+self.arr[1]+self.arr[2]+self.arr[3]+self.arr[4]+self.arr[5]+self.arr[6]
          north_score=self.arr[7]+self.arr[8]+self.arr[9]+self.arr[10]+self.arr[11]+self.arr[12]+self.arr[13]
          print("End of game!")
          print("North score: "+str(north_score))
          print("South score: "+str(south_score))
     
 
###########
#   Run   #
###########
 
# Initialise a Board object
b = Board("Bob",3, 0)
 
#Try a valid move
b.move(0)
b.move(7)
b.move(2)
b.move(3)
b.move(8)
b.move(1)




# Create a "computer" function who plays "one move think"
# 