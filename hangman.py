import re


def get_words(word_len, filename="words.txt"):
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


def get_possible_words(guesses, current_word, all_words):
    """
    Get all possible words based on the given `current_word` and `guesses`

    :param guesses: what the player has already submitted as a guess
    :param current_word: The current word at play.
    :return: A list of all possible words.
    """

    substitute = '.' if len(guesses) == 0 else f"[^{guesses}]"
    # Make the current word a regex phrase.
    current_word_regex = re.compile(current_word.replace('_', substitute))
    return [word for word in all_words if current_word_regex.match(word)]


def get_statistics(possible_words):
    """
    Gets the number of occurrences of the letters in the list possible_words

    :param possible_words: The words that are to be analyzed.
    :return: a dictionary as key: character, value: frequency of key in `possible_words`
    """
    words_as_str = ''.join(possible_words)
    words_as_str = ''.join(sorted(words_as_str))

    characters_in_words = ''.join(set(words_as_str))

    frequencies = {c: words_as_str.count(c) for c in characters_in_words}

    return frequencies


def get_likeliest_letter(stats):
    """
    Gets the likeliest letter and its likelihood in the given stats dict.

    :param stats: a dict as key: character, value: frequency of key
    :return: the likeliest_letter and its likelihood.
    """
    likeliest_letter = max(stats, key=stats.get)

    # Get the likelihood of the letter as a percent.
    likelihood = stats[likeliest_letter] / sum(stats.values()) * 100.0

    return likeliest_letter, likelihood


def play_hangman():
    """
    Plays a game of hangman.
    """

    is_playing = True
    was_correct = True

    guesses = ""
    current_word = ""

    words = []

    while is_playing:
        # Get input from the user if the current word on the board
        # changed or is new.
        if was_correct:
            print("What is currently on the board?")
            current_word = input("(Input unknown characters with _) ").lower()

        # if we found the word, we can stop playing.
        if current_word.count('_') == 0:
            break

        if len(words) == 0:
            words = get_words(len(current_word))

        possible_words = get_possible_words(guesses, current_word, words)

        print(f"There are {len(possible_words)} possible words.")

        if len(possible_words) <= 10:
            [print(word) for word in possible_words]

        if len(possible_words) == 1:
            print(f"It's obviously {possible_words[0]}.")
            break

        stats_temp = get_statistics(possible_words)

        stats = {key: value for key, value in stats_temp.items() if key not in guesses}

        print("Your most likely letter is...")
        likeliest_letter, likelihood = get_likeliest_letter(stats)
        print(f"{likeliest_letter} with a likelihood of {likelihood:.2f}%")

        was_correct = input("Was I correct? (y/n) ").lower() == 'y'

        guesses += likeliest_letter

        # Print a new line to break each round up.
        print("")

    print(f"It took me {len(guesses)} guesses to get it.")


if __name__ == '__main__':
    play_hangman()
