import os
import random

# Constants
WELCOME_MESSAGE = 'Welcome to Hangman game!'
HINT = 'Guess the word! HINT: word is a name of a fruit.'
SEPARATOR = '*' * 30

# Words for the game
some_words = ['apple', 'banana', 'mango', 'strawberry', 'orange', 'grape', 'pineapple', 'apricot', 'lemon',
              'coconut', 'watermelon', 'cherry', 'papaya', 'berry', 'peach', 'lychee', 'muskmelon']

selected_word = random.choice(some_words)
word_letters = list(selected_word)
user_letters = ['_' for _ in selected_word]
word_count = len(selected_word)
chance = None
game_difficulty = {
    'e': 10,
    'm': 7,
    'h': 5
}


def clear_screen():
    """Clears the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def select_difficulty():
    """Selects the game difficulty."""
    while True:
        difficulty = input("Choose difficulty: 'e' for easy, 'm' for medium, 'h' for hard: ")
        if difficulty in ['e', 'm', 'h']:
            return difficulty
        else:
            print("Select a valid difficulty option! ('e' for easy, 'm' for medium, 'h' for hard)")


def set_difficulty(difficulty):
    """Sets the game difficulty."""
    global chance
    chance = game_difficulty.get(difficulty, 10)


def check_letter(guessed_letter):
    """Checks if the guessed letter is correct and updates the game state."""
    global word_count, chance
    if guessed_letter in word_letters:
        indexes = [index for index, item in enumerate(word_letters) if item == guessed_letter]

        for index in indexes:
            if user_letters[index] == '_':
                user_letters[index] = guessed_letter
                word_count -= 1
            else:
                print('🤨 You have already guessed that letter. 🤨')

        print(' '.join(user_letters))
    else:
        print('🫣 Incorrect! Try again! 🫣')
        chance -= 1

    print(SEPARATOR)


def start_game(difficulty):
    """Starts the Hangman game."""
    clear_screen()
    set_difficulty(difficulty)
    print(WELCOME_MESSAGE)
    print(HINT)
    print(SEPARATOR)

    while word_count > 0 and chance > 0:
        print('Remaining chance:', chance)
        guessed_letter = input('Enter a letter to guess: ')
        if len(guessed_letter) != 1:
            print('🤥 Please enter only one letter at a time. 🤥')
            print(SEPARATOR)
            continue
        check_letter(guessed_letter)


if __name__ == '__main__':
    difficulty = select_difficulty()
    start_game(difficulty)
    clear_screen()
    if chance == 0:
        print('😬 You LOSE! 😬')
    else:
        print('🤩 You WON! 🤩')
    print('Word is:', selected_word)
    print('Thanks for playing...!')
