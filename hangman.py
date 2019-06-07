#!/usr/bin/env python3

import re

def play_round_of_hangman():
	# Get input from user of what is the word at the running of the script.
	current_word = input("What is currently on the board? ").lower()
	# The total number of characters in the word.
	num_of_characters = len(current_word)
	
	# Wrong guesses should be inputted as a single word.
	wrong_guesses = input("What are the wrong guesses? ")
	
	words = []
	
	# Open the file with all the words in the English language.
	with open("words.txt") as word_file:
		# Get all the words without any newlines.
		words_temp = map(lambda s: s.strip(), word_file.readlines())
		# filter the words so that they have the same number of characters as the word in play.
		words = [word.lower() for word in words_temp if len(word) is num_of_characters]
	
	# Get all words with just letters.
	words = list(filter(lambda w: w.isalpha(), words))
	
	# Make the current_word a regex.
	current_word_regex = current_word.replace('_', f"[^{wrong_guesses}]")
	
	# Get the regex object for the current word
	regex_obj = re.compile(current_word_regex)
	
	# Get all possible matches to the word.
	possible_matches = list(map(lambda word: regex_obj.match(word), words))
	
	# Get all the words from those matches (filter None matches)
	possible_words = [match.string for match in possible_matches if not match is None]
	
	# Print the list of possible words.
	print(possible_words)
	print(f"The last wrong guesses were {wrong_guesses}.")
	print(f"The current word was {current_word}.")
	return wrong_guesses

# TODO: Make this play multiple rounds of Hangman.
