import re


def get_words(word_len):
    # Open the file with all the words in the English language.
    with open("words.txt") as word_file:
        # Get all the words without any newlines.
        words_temp = map(lambda s: s.strip(), word_file.readlines())
        # filter the words so that they have the same number of characters as the word in play.
        words = [word.lower() for word in words_temp if len(word) is word_len]
        # Get rid of any possible duplicates in the file.
        words = list(set(words))
    return words


def get_possible_words(guesses, current_word):
    # The total number of characters in the word.
    num_of_characters = len(current_word)

    # Load the words in from the words.txt file.
    words = get_words(num_of_characters)

    # Get all words with just letters.
    words = list(filter(lambda w: w.isalpha(), words))

    # Regex will give us an error if we have
    # no wrong guesses, so if we don't need to exclude
    # anything, include everything!
    if len(guesses) is 0:
        substitute = '.'
    else:
        # exclude all of the wrong guesses
        substitute = f"[^{guesses}]"

    # Make the current_word a regex phrase.
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


def get_likeliest_letter(stats):
    # Get the most likely letter to guess.
    likeliest_letter = max(stats, key=stats.get)

    # Get the likelihood of the letter as a percent.
    likelihood = stats[likeliest_letter] / sum(stats.values()) * 100.0

    return likeliest_letter, likelihood


def play_hangman():
    is_playing = True
    # All of the characters that the computer guessed wrong.
    guesses = ""

    # the number of guesses the computer has made.
    num_of_guesses = 0

    current_word = ""

    was_correct = True

    while is_playing:
        # Get input from the user if the current word on the board
        # changed or is new.
        if was_correct:
            print("What is currently on the board?")
            current_word = input("(Input unknown characters with _) ").lower()

        # if we found the word, we can stop playing.
        if current_word.count('_') is 0:
            break

        # Get all of the possible words that can be guessed
        possible_words = get_possible_words(guesses, current_word)

        print(f"There are {len(possible_words)} possible words.")

        # Print all of the possible words if there's not too many of them.
        if len(possible_words) <= 10:
            [print(word) for word in possible_words]

        # Early exit if it we only have one guess.
        if len(possible_words) is 1:
            print(f"It's obviously {possible_words[0]}.")
            break

        # Get the frequencies of each character in the possible words.
        stats = get_statistics(possible_words)

        # Remove characters we've already guessed from the statistics.
        [stats.pop(guessed_letter, None) for guessed_letter in guesses]

        print("Your most likely letter is...")

        likeliest_letter, likelihood = get_likeliest_letter(stats)

        print(f"{likeliest_letter} with a likelihood of {likelihood:.2f}%")

        was_correct = input("Was I correct? (y/n) ").lower() == 'y'

        # add our guess to the total listing of guesses.
        num_of_guesses += 1
        guesses += likeliest_letter

        # Print a new line to break each round up.
        print("")

    print(f"It took me {num_of_guesses} guesses to get it.")


if __name__ == '__main__':
    play_hangman()
