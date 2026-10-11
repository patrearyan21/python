"""
Rock, Paper and Scissors Game
UTILITY 4 : FULLY DEVELOPED GAME

The complete, polished version of the game, built on top of Utilities 2
and 3. This is an enhanced version of the original fully-developed game:
it keeps every existing feature and adds a Hard difficulty level and a
log of the player's last 10 matches.

Features
  * Object-oriented design (class RockPaperScissors)
  * Menu-driven interface
  * Three difficulty levels:
        Easy  -> computer picks completely at random
        Smart -> computer leans towards countering your most-used move
        Hard  -> computer counters your most-used move more aggressively
  * Best-of-N matches with a full round-by-round history
  * Lifetime statistics saved to a file (rps_stats.json): matches,
    rounds, wins, losses, ties, win percentage, best win streak
  * A log of your last 10 matches (date not required - match number,
    result and score), also saved to rps_stats.json
  * Exception handling for invalid input and file read/write problems

How to run:
    1. Save this file as Utility4_full_game.py
    2. Open a terminal in the same folder
    3. Run:  python Utility4_full_game.py
No extra installation is needed - only the Python standard library
(random, json, os) is used, so no pip install is required.
"""

import json
import os
import random

CHOICES = ("rock", "paper", "scissors")
SHORTCUTS = {"r": "rock", "p": "paper", "s": "scissors"}
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}   # key beats value
COUNTER = {v: k for k, v in BEATS.items()}                            # what beats a move
STATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rps_stats.json")
DEFAULT_STATS = {"matches": 0, "match_wins": 0, "match_losses": 0,
                 "rounds": 0, "round_wins": 0, "round_losses": 0,
                 "round_ties": 0, "best_streak": 0, "match_log": []}


class Stats:
    """Loads, updates and saves the player's lifetime statistics."""

    def __init__(self, path=STATS_FILE):
        self.path = path
        self.data = {k: (list(v) if isinstance(v, list) else v) for k, v in DEFAULT_STATS.items()}
        self.load()

    def load(self):
        try:
            with open(self.path, "r") as f:
                saved = json.load(f)
            for key, default in DEFAULT_STATS.items():
                if key == "match_log":
                    self.data[key] = list(saved.get(key, []))[-10:]
                else:
                    self.data[key] = int(saved.get(key, 0))
        except (FileNotFoundError, ValueError, OSError):
            pass                                   # first run or damaged file

    def save(self):
        try:
            with open(self.path, "w") as f:
                json.dump(self.data, f, indent=2)
        except OSError:
            print("  (Could not save statistics.)")

    def reset(self):
        self.data = {k: (list(v) if isinstance(v, list) else v) for k, v in DEFAULT_STATS.items()}
        self.save()

    def log_match(self, result, you, computer):
        self.data["match_log"].append(f"#{self.data['matches']}: {result} ({you}-{computer})")
        self.data["match_log"] = self.data["match_log"][-10:]

    def show(self):
        d = self.data
        rounds = d["rounds"]
        pct = (d["round_wins"] / rounds * 100) if rounds else 0.0
        print("\n" + "=" * 40)
        print("          YOUR STATISTICS")
        print("=" * 40)
        print(f"Matches played : {d['matches']}  (won {d['match_wins']}, lost {d['match_losses']})")
        print(f"Rounds played  : {rounds}")
        print(f"Round wins     : {d['round_wins']}")
        print(f"Round losses   : {d['round_losses']}")
        print(f"Round ties     : {d['round_ties']}")
        print(f"Win percentage : {pct:.1f}%")
        print(f"Best win streak: {d['best_streak']}")
        print("=" * 40)

    def show_match_log(self):
        print("\n" + "-" * 40)
        print("       LAST MATCHES (most recent last)")
        print("-" * 40)
        if not self.data["match_log"]:
            print("  No matches played yet.")
        else:
            for line in self.data["match_log"]:
                print(" ", line)
        print("-" * 40)


class RockPaperScissors:
    DIFFICULTIES = ["easy", "smart", "hard"]

    def __init__(self):
        self.stats = Stats()
        self.difficulty = "easy"
        self.player_moves = {c: 0 for c in CHOICES}    # used by Smart/Hard mode

    # ---------- computer logic ----------
    def computer_choice(self):
        if self.difficulty in ("smart", "hard") and sum(self.player_moves.values()) >= 3:
            favourite = max(self.player_moves, key=self.player_moves.get)
            chance = 0.6 if self.difficulty == "smart" else 0.85
            if random.random() < chance:
                return COUNTER[favourite]
        return random.choice(CHOICES)

    # ---------- helpers ----------
    @staticmethod
    def decide(player, computer):
        if player == computer:
            return "tie"
        return "player" if BEATS[player] == computer else "computer"

    @staticmethod
    def ask(prompt):
        try:
            return input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return "q"

    def get_move(self):
        while True:
            text = self.ask("Your move (rock/paper/scissors or r/p/s, q = stop): ")
            if text in ("q", "quit"):
                return None
            text = SHORTCUTS.get(text, text)
            if text in CHOICES:
                return text
            print("  Invalid move. Try again.")

    def ask_target(self):
        while True:
            text = self.ask("First to how many wins? (1-10): ")
            if text == "q":
                return 3
            try:
                n = int(text)
                if 1 <= n <= 10:
                    return n
            except ValueError:
                pass
            print("  Enter a whole number from 1 to 10.")

    # ---------- one full match ----------
    def play_match(self):
        target = self.ask_target()
        score = {"player": 0, "computer": 0, "tie": 0}
        history, streak = [], 0
        print(f"\nMatch started ({self.difficulty.upper()} mode) - first to {target} wins.\n")

        while score["player"] < target and score["computer"] < target:
            player = self.get_move()
            if player is None:
                print("Match abandoned (not counted).")
                self.stats.save()
                return
            computer = self.computer_choice()
            self.player_moves[player] += 1
            winner = self.decide(player, computer)
            score[winner] += 1
            history.append((len(history) + 1, player, computer, winner))

            d = self.stats.data
            d["rounds"] += 1
            if winner == "player":
                d["round_wins"] += 1
                streak += 1
                d["best_streak"] = max(d["best_streak"], streak)
            elif winner == "computer":
                d["round_losses"] += 1
                streak = 0
            else:
                d["round_ties"] += 1

            words = {"player": "You win the round!", "computer": "Computer wins the round!",
                     "tie": "Tie round!"}[winner]
            print(f"  You: {player} | Computer: {computer}  ->  {words}"
                  f"  [{score['player']} - {score['computer']}]\n")

        self.stats.data["matches"] += 1
        if score["player"] > score["computer"]:
            self.stats.data["match_wins"] += 1
            result = "WON"
            print("*** MATCH WON! Congratulations! ***")
        else:
            self.stats.data["match_losses"] += 1
            result = "LOST"
            print("*** MATCH LOST. Better luck next time! ***")
        self.stats.log_match(result, score["player"], score["computer"])
        self.show_history(history)
        self.stats.save()

    @staticmethod
    def show_history(history):
        print("-" * 42)
        print(f"{'Round':<7}{'You':<12}{'Computer':<12}{'Winner'}")
        print("-" * 42)
        for n, p, c, w in history:
            print(f"{n:<7}{p:<12}{c:<12}{w}")
        print("-" * 42)

    # ---------- menu ----------
    @staticmethod
    def show_rules():
        print("\nRULES")
        print("  Rock     beats Scissors")
        print("  Scissors beats Paper")
        print("  Paper    beats Rock")
        print("  Same choice = Tie\n")
        print("DIFFICULTY LEVELS")
        print("  Easy  - the computer always picks at random")
        print("  Smart - the computer sometimes counters your favourite move")
        print("  Hard  - the computer more often counters your favourite move\n")

    def change_difficulty(self):
        i = self.DIFFICULTIES.index(self.difficulty)
        self.difficulty = self.DIFFICULTIES[(i + 1) % len(self.DIFFICULTIES)]
        print(f"\nDifficulty changed to: {self.difficulty.upper()}\n")

    def run(self):
        print("=" * 44)
        print("   ROCK - PAPER - SCISSORS  (Utility 4)")
        print("=" * 44)
        while True:
            print("\nMAIN MENU")
            print("  1. Play a match")
            print("  2. View statistics")
            print(f"  3. Change difficulty (now: {self.difficulty.upper()})")
            print("  4. Rules")
            print("  5. Reset statistics")
            print("  6. View last matches")
            print("  0. Exit")
            choice = self.ask("Choose an option: ")
            if choice == "1":
                self.play_match()
            elif choice == "2":
                self.stats.show()
            elif choice == "3":
                self.change_difficulty()
            elif choice == "4":
                self.show_rules()
            elif choice == "5":
                if self.ask("Really reset all statistics? (y/n): ") == "y":
                    self.stats.reset()
                    print("Statistics reset.")
            elif choice == "6":
                self.stats.show_match_log()
            elif choice in ("0", "q", "quit"):
                print("\nThanks for playing. Goodbye!")
                break
            else:
                print("Please choose a number from the menu.")


if __name__ == "__main__":
    RockPaperScissors().run()
