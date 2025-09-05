import random
import time
from enum import Enum
from typing import List, Set


class GameLevel(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"


class HangmanGame:
    def __init__(self, level: GameLevel):
        self.level = level
        self.max_lives = 6
        self.current_lives = 6
        self.time_limit = 15
        self.guessed_letters: Set[str] = set()
        self.game_over = False
        self.won = False
        self.target_word = ""
        self.display_word: List[str] = []
        self.start_time = 0
        self.dictionary = self._load_dictionary()
        self._select_target()

    def _load_dictionary(self) -> List[str]:
        try:
            if self.level == GameLevel.BASIC:
                with open('data/words.txt', 'r') as file:
                    return [word.strip().lower() for word in file.readlines()]
            else:
                with open('data/phrases.txt', 'r') as file:
                    return [phrase.strip().lower() for phrase in file.readlines()]
        except FileNotFoundError:
            fallback_words = ['python', 'programming', 'computer', 'algorithm', 'software']
            fallback_phrases = ['hello world', 'unit testing', 'software development']
            return fallback_words if self.level == GameLevel.BASIC else fallback_phrases

    def _select_target(self):
        self.target_word = random.choice(self.dictionary)
        self.display_word = []
        for char in self.target_word:
            if char.isalpha():
                self.display_word.append('_')
            else:
                self.display_word.append(char)

    def start_timer(self):
        self.start_time = time.time()

    def get_remaining_time(self) -> float:
        if self.start_time == 0:
            return self.time_limit
        elapsed = time.time() - self.start_time
        remaining = max(0, self.time_limit - elapsed)
        return remaining

    def is_time_up(self) -> bool:
        return self.get_remaining_time() <= 0

    def make_guess(self, letter: str) -> bool:
        if len(letter) != 1 or not letter.isalpha():
            raise ValueError("Please enter a single letter")

        letter = letter.lower()

        if letter in self.guessed_letters:
            raise ValueError(f"Letter '{letter}' has already been guessed")

        self.guessed_letters.add(letter)

        if letter in self.target_word:
            for i, char in enumerate(self.target_word):
                if char == letter:
                    self.display_word[i] = letter

            if self.is_won():
                self.won = True
                self.game_over = True

            return True
        else:
            self.current_lives -= 1
            if self.current_lives <= 0:
                self.game_over = True
            return False

    def is_won(self) -> bool:
        return '_' not in self.display_word

    def is_game_over(self) -> bool:
        return self.game_over or self.is_time_up() or self.current_lives <= 0

    def get_display_string(self) -> str:
        return ' '.join(self.display_word)

    def get_hangman_drawing(self) -> str:
        hangman_parts = [
            "  ____",
            "  |  |",
            "  |  O" if self.max_lives - self.current_lives >= 1 else "  |   ",
            self._get_body_part(),
            self._get_legs_part(),
            "__|__"
        ]

        drawing = '\n'.join(hangman_parts)
        drawing += f"\n\nLives remaining: {self.current_lives}"

        wrong_guesses = [letter for letter in self.guessed_letters
                         if letter not in self.target_word]
        if wrong_guesses:
            drawing += f"\nWrong guesses: {', '.join(sorted(wrong_guesses))}"

        return drawing

    def _get_body_part(self) -> str:
        lives_lost = self.max_lives - self.current_lives
        if lives_lost >= 3:
            return "  | /|\\"
        elif lives_lost >= 2:
            return "  | /|"
        elif lives_lost >= 1:
            return "  |  |"
        else:
            return "  |   "

    def _get_legs_part(self) -> str:
        lives_lost = self.max_lives - self.current_lives
        if lives_lost >= 5:
            return "  | / \\"
        elif lives_lost >= 4:
            return "  | /"
        elif lives_lost >= 1:
            return "  |"
        else:
            return "  |   "

    def get_game_status(self) -> str:
        if self.won:
            return f"Congratulations! You guessed the word: '{self.target_word}'"
        elif self.is_time_up():
            return f"Time's up! The answer was: '{self.target_word}'"
        elif self.current_lives <= 0:
            return f"Game over! The answer was: '{self.target_word}'"
        else:
            remaining_time = int(self.get_remaining_time())
            return f"Time remaining: {remaining_time} seconds"

    def reset_game(self):
        self.current_lives = self.max_lives
        self.guessed_letters = set()
        self.game_over = False
        self.won = False
        self.start_time = 0
        self._select_target()


def main():
    print("Welcome to Hangman Game!")
    print("Choose difficulty level:")
    print("1. Basic (single words)")
    print("2. Intermediate (phrases)")

    while True:
        try:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice == '1':
                level = GameLevel.BASIC
                break
            elif choice == '2':
                level = GameLevel.INTERMEDIATE
                break
            else:
                print("Please enter 1 or 2")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return

    game = HangmanGame(level)

    while True:
        game.start_timer()
        print(f"\n{game.get_hangman_drawing()}")
        print(f"Word: {game.get_display_string()}")
        print(game.get_game_status())

        if game.is_game_over():
            play_again = input("\nWould you like to play again? (y/n): ")
            if play_again.strip().lower() == 'y':
                game.reset_game()
                continue
            else:
                print("Thanks for playing!")
                break

        try:
            guess = input("Enter a letter: ").strip()

            if game.is_time_up():
                print(game.get_game_status())
                continue

            result = game.make_guess(guess)

            if result:
                print(f"Good guess! '{guess}' is in the word.")
            else:
                print(f"Sorry, '{guess}' is not in the word.")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()
