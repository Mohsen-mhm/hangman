import os
import random
import requests
from dotenv import load_dotenv
from db import Database
import bcrypt

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

some_words = []

db = Database()


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
            db.insert_word(selected_word)
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


def register_or_login():
    while True:
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        user = db.get_user(username)

        if user is None:
            # User doesn't exist, so register
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db.insert_user(username, hashed_password)
            user = db.get_user(username)

            print(SEPARATOR)
            print(f'Welcome {user[1]}')
            print("Total score:", user[3])
            print(SEPARATOR)

            return user[0]  # Assuming user[0] is ID
        else:
            # User exists, check password
            if bcrypt.checkpw(password.encode('utf-8'), user[2]):

                print(SEPARATOR)
                print(f'Welcome back {user[1]}')
                print("Total score:", user[3])
                print(SEPARATOR)

                return user[0]
            else:
                print("Invalid credentials! Try again.")


if __name__ == '__main__':
    try:
        db.create_users_table()
        db.create_words_table()
        db.create_games_table()

        if os.path.exists('words.txt'):
            with open('words.txt', 'r') as f:
                for line in f:
                    word = db.get_word(line.strip())
                    if word is None:
                        db.insert_word(line.strip())

        some_words = db.get_all_words()

        for word in some_words:
            if not db.get_word(word):
                db.insert_word(word)

        user_id = register_or_login()
        difficulty = select_difficulty()
        selected_word, word_letters, user_letters, word_count = set_word()
        chance = start_game(difficulty, selected_word, word_letters, user_letters, word_count)
        clear_screen()
        if chance == 0:
            won = 0
            print('😬 You LOSE! 😬')
        else:
            won = 1
            print('🤩 You WON! 🤩')
            db.update_user_score(user_id, word_count)

        word = db.get_word(selected_word)
        db.insert_game(user_id, word[0], won)

        print('Word is:', selected_word)
        print('Thanks for playing...!')
    finally:
        db.close_connection()
