from collections import Counter
from itertools import chain


# read in word dictionary
dictionary = set()
word_file = open("word_list.txt", "r")
lines = word_file.readlines()
for word in lines:
    if (len(word.rstrip('\n')) == 5):
        dictionary.add(word.rstrip('\n'))

# loop over all 6 guesses
for i in range(6):
    # count frequency of letters in all words
    letter_count = Counter(chain.from_iterable(dictionary))
    letter_frequency = {
        character: value
        for character, value in letter_count.items()
    }
    # count frequency of letters in all positions
    position_frequency = [{}, {}, {}, {}, {}]
    for word in dictionary:
        for i in range(5):
            if word[i] not in position_frequency[i]:
                position_frequency[i][word[i]] = 0
            position_frequency[i][word[i]] += 1

    # assign a weight to each word
    # weight is based upon total letter frequency and also positional letter frequency
    # aims to guess the word that will reduce the dictionary the most after the guess is complete
    def calculate_score(word):
        score = 0
        for i in range(5): # increase score for positional frequency
            score += position_frequency[i][word[i]]
        for char in set(word): # increase score for letter frequency
            score += letter_frequency[char]
        return score
    word_scores = {
        word: calculate_score(word)
        for word in dictionary
    }

    # guess and read in response
    sorted_guesses = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    guess = sorted_guesses[0][0]
    if len(dictionary) <= 10:
        print("Possible words: ", dictionary)
    else:
        print("Possible words: ", len(dictionary))

    # the guess word is printed in green using a color code
    # see this link for a full table of color codes: https://stackoverflow.com/a/21786287     
    print("Guess: " + '\x1b[6;30;42m' + guess +  '\x1b[0m')
    print("probability = ", word_scores[guess] / sum(word_scores.values()) * 100)
    result = input("Enter results (g for green, y for yellow, b for black) in order: ")
    result = result[0:5] # trim off newline

    # figure out what letters MUST be in the word
    char_counts = {}
    for i in range(5):
        if result[i] == "g" or result[i] == "y":
            if guess[i] not in char_counts:
                char_counts[guess[i]] = 0
            char_counts[guess[i]] += 1

    # parse results to reduce dictionary
    new_dictionary = dictionary.copy()
    for word in dictionary:
        i = 0
        for char in result:
            if char == 'g': # green
                if word[i] != guess[i]:
                    new_dictionary.remove(word)
                    break
            elif char == 'y': # yellow
                if word[i] == guess[i] or guess[i] not in word:
                    new_dictionary.remove(word)
                    break
            elif char == 'b': # black
                if guess[i] in word:
                    if guess[i] not in char_counts: # we know the letter shouldn't be in the word
                        new_dictionary.remove(word)
                        break
                    elif word.count(guess[i]) > char_counts[guess[i]]: # the letter is in the word more times than we know it can be
                        new_dictionary.remove(word)
                        break
            i += 1
    dictionary = new_dictionary
