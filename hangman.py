import re


def get_words(word_len):
    # Open the file with all the words in the English language.
    with open("words.txt") as word_file:
        # Get all the words without any newlines.
        words_temp = map(lambda s: s.strip(), word_file.readlines())
        # filter the words so that they have the same number of characters as the word in play.
        words = [word.lower() for word in words_temp if len(word) is word_len]
    return words


def play_round_of_hangman(wrong_guesses, current_word):
    # The total number of characters in the word.
    num_of_characters = len(current_word)

    words = get_words(num_of_characters)

    # Get all words with just letters.
    words = list(filter(lambda w: w.isalpha(), words))

    if len(wrong_guesses) is 0:
        substitute = '.'
    else:
        substitute = f"[^{wrong_guesses}]"

    # Make the current_word a regex.
    current_word_regex = current_word.replace('_', substitute)

    # Get the regex object for the current word
    regex_obj = re.compile(current_word_regex)

    # Get all possible matches to the word.
    possible_matches = list(map(lambda word: regex_obj.match(word), words))

    # Get all the words from those matches (filter None matches)
    possible_words = [match.string for match in possible_matches if match is not None]

    # Print the list of possible words.
    return possible_words


def get_statistics(possible_words):
    # Join all of the words in the list into a giant string.
    words_as_str = ''.join(possible_words)
    # sort the characters in each word.
    words_as_str = ''.join(sorted(words_as_str))

    # get all of the characters in the words.
    characters_in_words = ''.join(set(words_as_str))

    # Get the frequencies of each letter in the words.
    frequencies = {c: words_as_str.count(c) for c in characters_in_words}

    return frequencies


def play_hangman():
    is_playing = True
    wrong_guesses = ""

    num_of_guesses = 0

    while is_playing:
        # Get input from user of what is the word at the running of the script.
        current_word: str = input("What is currently on the board? ").lower()

        if current_word.count('_') is 0:
            break

        num_of_guesses += 1

        possible_words = play_round_of_hangman(wrong_guesses, current_word)

        print(f"There are {len(possible_words)} possible words.")

        if len(possible_words) <= 10:
            [print(word) for word in possible_words]

        stats = get_statistics(possible_words)

        [stats.pop(guessed_letter, None) for guessed_letter in current_word.replace('_', '')]
        [stats.pop(guessed_letter, None) for guessed_letter in wrong_guesses]

        print("Your most likely letter is...")

        likeliest_letter = max(stats, key=stats.get)

        likelihood = stats[likeliest_letter] / sum(stats.values()) * 100.0

        print(f"{likeliest_letter} with a likelihood of {likelihood:.2f}%")

        was_correct = input("Was I correct? (y/n) ").lower() == 'y'

        if not was_correct:
            wrong_guesses += likeliest_letter

    print(f"It took me {num_of_guesses} guesses to get it.")


if __name__ == '__main__':
    play_hangman()
