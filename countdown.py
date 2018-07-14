import argparse
import sys


def load_words(filename):
    """Load all words (9 letters or less) from dictionary into memory
    
    :param filename: A string, the filename to load
    :return: A set, all relevant words in the file
    """

    valid_words = set()
    with open(filename, 'r') as word_file:
        for word in word_file:
            if len(word) < 11:  # only want 9 letter words (accounts for \n extra char)
                valid_words.add(word.rstrip('\n'))

        return valid_words


def generate_solutions(words, letters, sort=True):
    """Generate a list of all possible solutions from the given letters

    :param words: A set of all valid words
    :param letters: A string, the letters from which is derive the solution
    :return: A list of strings, the solutions
    """
    
    solutions = []

    def check_all_letters_valid(word):
        """Check whether a word can be made from the given letters"""
        
        temp_letters = letters
        for letter in word:
            if letter in temp_letters:
                index_of_letter = temp_letters.index(letter)
                temp_letters = temp_letters[:index_of_letter] + temp_letters[index_of_letter + 1:]
            else:
                return False

        return True

    for word in words:
        if check_all_letters_valid(word):
            solutions.append(word)

    if sort:
        solutions.sort(key=lambda w: len(w))

    return solutions


def pretty_print_solutions(solutions, reverse=False):
    """Print out the solutions organised by word length

    :param solutions: A list of strings containing the possible solutions
    :param reverse: A bool, whether to print longest to shortest (True) or shortest to longest (False)
    """
    
    word_lists = [[word for word in solutions if len(word) == i] for i in range(1, 10)]
    for i, sublist in enumerate(word_lists):
        print('=== {} letter words ==='.format(i + 1))
        for word in sorted(sublist, reverse=reverse):
            print(word)


def main():
    """Main function"""

    parser = argparse.ArgumentParser(description='Generate possible solutions to a Countdown puzzle.')
    parser.add_argument('dictionary', type=str, help='A dictionary filename')
    parser.add_argument('--letters', type=str, help='The puzzle letters')
    args = parser.parse_args()

    words = load_words(args.dictionary)

    if args.letters:
        solutions = generate_solutions(words, args.letters)
        pretty_print_solutions(solutions)
    else:
        while True:
            try:
                letters = input('Enter letters (or Ctrl-D to quit): ')
            except EOFError:
                print('Quitting...')
                sys.exit()
            
            solutions = generate_solutions(words, letters)
            print('Solutions are:')
            pretty_print_solutions(solutions)
            print()


if __name__ == '__main__':
    main()
