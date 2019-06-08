# HangmanSolver
A simple hangman game where the computer can either help you 
play your own game of hangman or can try to guess your word.

This was inspired by a game of Hangman at work today where I
said I would make a solver for the game.

Thankfully, this (possibly cheating) software also showcases a
good bit of functional programming in Python, which I am
currently trying to improve upon in my own time.

Hope you enjoy!

## Tools Used
* Standard [Python 3.6](https://www.python.org/) install 

## Regex
For help with understanding Regex (regular expressions), [this
site](https://regexr.com/) helped me a lot when I was first learning them.

## Example Game
Here is an example of a game where the word was `jawbreaker`.
```
What is currently on the board?
(Input unknown characters with _) __________
There are 7943 possible words.
Your most likely letter is...
e with a likelihood of 11.47%
Was I correct? (y/n) y

What is currently on the board?
(Input unknown characters with _) _____e__e_
There are 149 possible words.
Your most likely letter is...
s with a likelihood of 14.68%
Was I correct? (y/n) n

There are 52 possible words.
Your most likely letter is...
r with a likelihood of 12.02%
Was I correct? (y/n) y

What is currently on the board?
(Input unknown characters with _) ____re__er
There are 3 possible words.
daydreamer
jawbreaker
lawbreaker
Your most likely letter is...
a with a likelihood of 33.33%
Was I correct? (y/n) y

What is currently on the board?
(Input unknown characters with _) _a__rea_er
There are 3 possible words.
daydreamer
jawbreaker
lawbreaker
Your most likely letter is...
k with a likelihood of 16.67%
Was I correct? (y/n) y

What is currently on the board?
(Input unknown characters with _) _a__reaker
There are 2 possible words.
jawbreaker
lawbreaker
Your most likely letter is...
b with a likelihood of 33.33%
Was I correct? (y/n) y

What is currently on the board?
(Input unknown characters with _) _a_breaker
There are 2 possible words.
jawbreaker
lawbreaker
Your most likely letter is...
w with a likelihood of 50.00%
Was I correct? (y/n) y

What is currently on the board?
(Input unknown characters with _) _awbreaker
There are 2 possible words.
jawbreaker
lawbreaker
Your most likely letter is...
j with a likelihood of 50.00%
Was I correct? (y/n) y

What is currently on the board?
(Input unknown characters with _) jawbreaker
It took me 8 guesses to get it.
```