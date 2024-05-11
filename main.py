import os
import random

# Constants
WELCOME_MESSAGE = 'Welcome to Hangman game!'
HINT = 'Guess the word! HINT: word is a name of a fruit.'
SEPARATOR = '*' * 30

# Words for the game
some_word = ['apple', 'banana', 'mango', 'strawberry', 'orange', 'grape', 'pineapple', 'apricot', 'lemon', 'coconut',
             'watermelon', 'cherry', 'papaya', 'berry', 'peach', 'lychee', 'muskmelon']

selected_word = random.choice(some_word)
word_letters = list(selected_word)
user_letters = ['_' for _ in selected_word]
word_count = len(selected_word)
chance = 10


def start_game():
    """Starts the Hangman game."""
    clear_screen()
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


def check_letter(guessed_letter):
    """Checks if the guessed letter is correct and updates the game state."""
    global word_count, chance
    if guessed_letter in word_letters:
        indexes = [index for index, item in enumerate(word_letters) if item == guessed_letter]

        for index in indexes:
            if user_letters[index] is '_':
                user_letters[index] = guessed_letter
                word_count -= 1
            else:
                print('🤨 You have already guessed that letter. 🤨')

        print(' '.join(user_letters))
    else:
        print('🫣 Incorrect! Try again! 🫣')
        chance -= 1

    print(SEPARATOR)


def clear_screen():
    """Clears the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    start_game()
    clear_screen()
    if chance == 0:
        print('😬 You LOSE! 😬')
    else:
        print('🤩 You WON! 🤩')
    print('Word is:', selected_word)
    print('Thanks for playing...!')
