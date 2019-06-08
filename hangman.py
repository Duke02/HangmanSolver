import re
from functools import reduce
from itertools import chain
from collections import Counter
import typing


def get_words(word_len: int, filename: str = "words.txt") -> typing.Set[str]:
    """
    Get all words that have the desired length from the given text file.

    :param filename: The name of the file to load the words from.
    :param word_len: The desired length of words.
    :return: an iterable of words of the given length.
    """
    with open(filename) as word_file:
        return {
            word.lower()
            for word in map(str.strip, word_file.readlines())
            if len(word) == word_len and word.isalpha()
        }


def get_possible_words(guesses: str, current_word: str, all_words: typing.Iterable) -> typing.List[str]:
    """
    Get all possible words based on the given `current_word` and `guesses`

    :param all_words: All of the words that have been loaded in.
    :param guesses: what the player has already submitted as a guess
    :param current_word: The current word at play.
    :return: A list of all possible words.
    """

    substitute: str = '.' if len(guesses) == 0 else f"[^{guesses}]"
    # Make the current word a regex phrase.
    current_word_regex: typing.Pattern = re.compile(current_word.replace('_', substitute))
    return [word for word in all_words if current_word_regex.match(word)]


def get_statistics(possible_words: typing.Iterable) -> Counter:
    """
    Gets the number of occurrences of the letters in the list possible_words

    :param possible_words: The words that are to be analyzed.
    :return: a Counter object with a count of each letter in possible_words
    """
    return Counter(chain.from_iterable(possible_words))


def get_likeliest_letter(stats: Counter) -> typing.Tuple[str, float]:
    """
    Gets the likeliest letter and its likelihood in the given stats dict.

    :param stats: a dict as key: character, value: frequency of key
    :return: the likeliest_letter and its likelihood.
    """
    likeliest_letter, count = stats.most_common(1)[0]
    likelihood = count / sum(stats.values()) * 100.0
    return likeliest_letter, likelihood


def sanitize_user_input(user_input: str, last_user_input: str, initial_len_of_input: int) -> typing.Tuple[str, int]:
    """
    Corrects the user's input based on previous input.

    :param last_user_input: The previous user input.
    :param user_input: The current user input.
    :param initial_len_of_input: The initial length of the user input.
    :return: The correct user input and the correct length of the user input.
    """

    if initial_len_of_input == -1:
        return user_input, len(user_input)

    corrected_input: str = user_input

    while len(corrected_input) != initial_len_of_input:
        print("Your input is not the same length as it was the first time.")
        print(f"Your last input was {last_user_input} and had {len(last_user_input)} characters in it.")
        corrected_input = input("Try again. ").lower()

    differences: typing.List[bool] = [last_user_input[i] != corrected_input[i]
                                      for i in range(initial_len_of_input)
                                      if last_user_input[i] != '_']

    if len(differences) == 0:
        return corrected_input, initial_len_of_input

    has_differences: bool = all(differences) or reduce(lambda x, y: x != y, differences)

    while has_differences:
        print("Your input is not the same as it was the first time.")
        print("You may have put a character in the wrong place.")
        print(f"Your last input was {last_user_input}.")
        corrected_input = input("Try again. ").lower()

        differences = [last_user_input[i] != corrected_input[i]
                       for i in range(initial_len_of_input)
                       if last_user_input[i] != '_']
        has_differences = all(differences) or reduce(lambda x, y: x != y, differences)

    return corrected_input, initial_len_of_input


def play_hangman():
    """
    Plays a game of hangman.
    """

    is_playing: bool = True
    was_correct: bool = True

    guesses: str = ""
    current_word: str = ""

    len_of_word: int = -1

    words: typing.Set[str] = set()

    while is_playing:
        # Get input from the user if the current word on the board
        # changed or is new.
        if was_correct:
            last_word: str = current_word
            print("What is currently on the board?")
            current_word = input("(Input unknown characters with _) ").lower()
            current_word, len_of_word = sanitize_user_input(current_word, last_word, len_of_word)

        # if we found the word, we can stop playing.
        if current_word.count('_') == 0:
            break

        # Add any guesses that might have been missed in between rounds.
        guesses += ''.join([guess for guess in current_word if guess != '_' and guess not in guesses])

        if len(words) == 0:
            words = get_words(len(current_word))

        possible_words: typing.List[str] = get_possible_words(guesses, current_word, words)

        print(f"There are {len(possible_words)} possible words.")

        if len(possible_words) <= 10:
            [print(word) for word in possible_words]

        if len(possible_words) == 1:
            print(f"It's obviously {possible_words[0]}.")
            break

        stats_temp: Counter = get_statistics(possible_words)

        stats: Counter = Counter({key: value for key, value in stats_temp.items() if key not in guesses})

        print("Your most likely letter is...")
        likeliest_letter: typing.Tuple[str, float] = get_likeliest_letter(stats)
        print(f"{likeliest_letter[0]} with a likelihood of {likeliest_letter[1]:.2f}%")

        was_correct = input("Was I correct? (y/n) ").lower() == 'y'

        guesses += likeliest_letter[0]

        # Print a new line to break each round up.
        print("")

    print(f"It took me {len(guesses)} guesses to get it.")


if __name__ == '__main__':
    play_again: bool = True
    while play_again:
        play_hangman()

        play_again = input("Want to play again? (y/n) ").lower() == 'y'

        # Print a new line to separate games.
        print("")
