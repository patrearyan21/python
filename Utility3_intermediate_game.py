"""
Rock, Paper and Scissors Game
UTILITY 3 : INTERMEDIATE-LEVEL PLAYABLE GAME

Builds on Utility 2 by moving the logic into functions, validating and
cleaning input properly, supporting shortcut keys, playing a "best of N"
match, keeping a full round-by-round history, and handling unexpected
input (including Ctrl+C) with exception handling.

New concepts added over Utility 2: functions, dictionaries, try/except,
                                    round history, best-of-N matches

How to run:
    1. Save this file as Utility3_intermediate_game.py
    2. Open a terminal in the same folder
    3. Run:  python Utility3_intermediate_game.py
"""

import random

CHOICES = ("rock", "paper", "scissors")
SHORTCUTS = {"r": "rock", "p": "paper", "s": "scissors"}
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}  # key beats value


def show_banner():
    print("=" * 46)
    print("   ROCK - PAPER - SCISSORS  (Utility 3)")
    print("=" * 46)


def get_player_choice():
    """Ask until a valid choice is given. Returns None if the user quits."""
    while True:
        try:
            text = input("Your choice (rock/paper/scissors, q = quit): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if text in ("q", "quit"):
            return None
        text = SHORTCUTS.get(text, text)
        if text in CHOICES:
            return text
        print("  Invalid input. Please try again.")


def get_computer_choice():
    return random.choice(CHOICES)


def decide_winner(player, computer):
    """Return 'player', 'computer' or 'tie'."""
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "player"
    return "computer"


def ask_rounds_to_win():
    """Best-of-N: first to reach the target wins the match."""
    while True:
        try:
            n = int(input("First to how many wins? (1-10): "))
            if 1 <= n <= 10:
                return n
            print("  Please enter a number between 1 and 10.")
        except ValueError:
            print("  That is not a number. Try again.")
        except (EOFError, KeyboardInterrupt):
            return 3


def show_history(history):
    if not history:
        return
    print("-" * 46)
    print(f"{'Round':<7}{'You':<12}{'Computer':<12}{'Winner'}")
    print("-" * 46)
    for number, player, computer, winner in history:
        print(f"{number:<7}{player:<12}{computer:<12}{winner}")
    print("-" * 46)


def play_match():
    target = ask_rounds_to_win()
    score = {"player": 0, "computer": 0, "tie": 0}
    history = []

    print(f"\nMatch started! First to {target} wins.\n")
    while score["player"] < target and score["computer"] < target:
        player = get_player_choice()
        if player is None:
            print("Match stopped early.")
            break
        computer = get_computer_choice()
        winner = decide_winner(player, computer)
        score[winner] += 1
        history.append((len(history) + 1, player, computer, winner))

        print(f"  You: {player}  |  Computer: {computer}")
        label = {"player": "You win the round!", "computer": "Computer wins the round!",
                 "tie": "Tie round!"}[winner]
        print(f"  {label}   Score {score['player']} - {score['computer']}\n")

    show_history(history)
    if score["player"] > score["computer"]:
        print(f"MATCH RESULT: You won {score['player']} - {score['computer']}!")
    elif score["computer"] > score["player"]:
        print(f"MATCH RESULT: Computer won {score['computer']} - {score['player']}.")
    else:
        print("MATCH RESULT: No winner.")
    return score


def main():
    show_banner()
    while True:
        play_match()
        try:
            again = input("\nPlay another match? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            again = "n"
        if again != "y":
            break
        print()
    print("\nThanks for playing. Goodbye!")


if __name__ == "__main__":
    main()
