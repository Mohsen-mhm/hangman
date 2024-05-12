import os
import random
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
WELCOME_MESSAGE = 'Welcome to Hangman game!'
HINT = 'Guess the word!'
SEPARATOR = '*' * 30
API_KEY = os.getenv('API_KEY')

game_difficulty = {
    'e': 20,
    'm': 15,
    'h': 10
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


def set_word_locally():
    selected_word = random.choice(some_words)
    word_letters = list(selected_word)
    user_letters = ['_' for _ in selected_word]
    word_count = len(selected_word)
    return selected_word, word_letters, user_letters, word_count


def set_word_api():
    url = "https://a-randomizer-data-api.p.rapidapi.com/api/random/words"
    querystring = {"count": "1"}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "a-randomizer-data-api.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            selected_word = response.json()[0]
            word_letters = list(selected_word)
            user_letters = ['_' for _ in selected_word]
            word_count = len(selected_word)
            return selected_word, word_letters, user_letters, word_count
    except requests.exceptions.RequestException as e:
        pass
    return None, [], [], 0


def set_word():
    selected_word, word_letters, user_letters, word_count = set_word_api()
    if selected_word is None:
        selected_word, word_letters, user_letters, word_count = set_word_locally()
    return selected_word, word_letters, user_letters, word_count


def set_difficulty(difficulty):
    chance = game_difficulty.get(difficulty, 10)
    return chance


def check_letter(guessed_letter, word_letters, user_letters, word_count, chance):
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
    return word_count, chance


def start_game(difficulty, selected_word, word_letters, user_letters, word_count):
    chance = set_difficulty(difficulty)
    while word_count > 0 and chance > 0:
        print('Remaining chance:', chance)
        guessed_letter = input('Enter a letter to guess: ')
        if len(guessed_letter) != 1:
            print('🤥 Please enter only one letter at a time. 🤥')
            print(SEPARATOR)
            continue
        word_count, chance = check_letter(guessed_letter, word_letters, user_letters, word_count, chance)
        print(SEPARATOR)
    return chance


if __name__ == '__main__':
    some_words = [
        'apple', 'banana', 'cherry', 'orange', 'pear', 'mango', 'strawberry', 'grape', 'blueberry',
        'pineapple', 'kiwi', 'watermelon', 'peach', 'apricot', 'plum', 'lemon', 'lime', 'coconut', 'avocado',
        'tangerine', 'nectarine', 'guava', 'papaya', 'ugly', 'melon', 'sugar', 'sour', 'sea', 'white', 'american',
        'wild',
        'cucumber', 'beach', 'black', 'blue', 'california', 'carolina', 'chinese', 'clammy', 'climb',
        'common', 'tomato', 'desert', 'date', 'eastern', 'florida', 'fuzzy', 'garden', 'georgia', 'rice', 'indian',
        'japanese', 'korean', 'nut', 'mallow', 'mountain', 'oak', 'holly', 'tree', 'pumpkin', 'purple', 'red',
        'rock', 'salal', 'saw', 'shiny', 'leaf', 'silver', 'wisteria'
    ]
    difficulty = select_difficulty()
    selected_word, word_letters, user_letters, word_count = set_word()
    chance = start_game(difficulty, selected_word, word_letters, user_letters, word_count)
    clear_screen()
    if chance == 0:
        print('😬 You LOSE! 😬')
    else:
        print('🤩 You WON! 🤩')
    print('Word is:', selected_word)
    print('Thanks for playing...!')
