"""
Rock, Paper and Scissors Game
MODULE 1 : UTILITY 1 - Basic single-round game (Player vs Computer)

Concepts used : import, list, input(), random.choice(), if / elif / else, print()
Works in any standard terminal (no extra libraries needed).
"""

import random

# Step 1: Set up - the three valid moves, stored in a list
choices = ["rock", "paper", "scissors"]

print("=" * 40)
print("   ROCK - PAPER - SCISSORS  (Utility 1)")
print("=" * 40)

# Step 2: Get the player's move
# input() reads what the player types; strip() removes extra spaces,
# lower() makes the comparison case-insensitive (Rock == rock == ROCK)
player = input("Enter rock, paper or scissors: ").strip().lower()

# Step 3: Get the computer's move
# random.choice() picks one item from the list purely by chance
computer = random.choice(choices)

print("You chose      :", player)
print("Computer chose :", computer)

# Step 4: Decide the winner
if player not in choices:
    # Anything the player typed that isn't in the list is invalid
    print("Invalid choice! Please type rock, paper or scissors.")
elif player == computer:
    # Same move from both sides -> tie
    print("It's a TIE!")
elif (player, computer) in [("rock", "scissors"),
                             ("paper", "rock"),
                             ("scissors", "paper")]:
    # These three combinations are the only ways the player can win
    print("You WIN!")
else:
    # Anything left over means the computer's move beats the player's
    print("Computer WINS!")
