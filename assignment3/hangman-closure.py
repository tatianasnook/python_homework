# Task 4.
def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)

        result = ""
        for char in secret_word:
            if char in guesses:
                result += char
            else:
                result += "_"
        print(result)

        if "_" not in result:
            return True
        else:
            return False
        
    return hangman_closure

secret_word = input("Enter a secret word for the game: ")
hangman = make_hangman(secret_word)

while True:
    letter = input("Guess a letter: ")
    is_complete = hangman(letter)
    if is_complete:
        print("Congratulations! You've guessed the word:", secret_word)
        break
