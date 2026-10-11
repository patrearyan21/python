"""
Rock, Paper and Scissors Game
UTILITY 2 : BASIC-LEVEL PLAYABLE GAME

A simple, complete, beginner-friendly implementation. The player can
play as many rounds as they like against the computer, with a running
score of wins, losses and ties.

Python concepts used: import, list, input(), random.choice(),
                       if / elif / else, while loop, print()

How to run:
    1. Save this file as Utility2_basic_game.py
    2. Open a terminal in the same folder
    3. Run:  python Utility2_basic_game.py   (or  python3 ... on Mac/Linux)
"""

import random

CHOICES = ["rock", "paper", "scissors"]

wins = 0
losses = 0
ties = 0

print("=" * 44)
print("   ROCK - PAPER - SCISSORS  (Utility 2)")
print("=" * 44)
print("Type rock, paper or scissors. Type 'quit' to stop.\n")

while True:
    player = input("Your choice: ").strip().lower()

    if player == "quit":
        break

    if player not in CHOICES:
        print("Invalid choice. Please type rock, paper or scissors.\n")
        continue

    computer = random.choice(CHOICES)
    print(f"Computer chose: {computer}")

    if player == computer:
        ties += 1
        print("Result: TIE\n")
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        wins += 1
        print("Result: You WIN this round!\n")
    else:
        losses += 1
        print("Result: Computer WINS this round!\n")

    print(f"Score -> Wins: {wins}  Losses: {losses}  Ties: {ties}\n")

print("=" * 44)
print(f"Final Score -> Wins: {wins}  Losses: {losses}  Ties: {ties}")
print("Thanks for playing!")
print("=" * 44)
