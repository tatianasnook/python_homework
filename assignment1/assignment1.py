# Task 1.
def hello():
    return "Hello!"

print(hello())


# Task 2.
def greet(name):
    return f"Hello, {name}!"

print(greet("Amy"))


# Task 3.
def calc(num1, num2, operation="multiply"):
    try:
        match operation:
            case "add":
                result = num1 + num2
            case "subtract":
                result = num1 - num2
            case "multiply":
                result = num1 * num2
            case "divide":
                result = num1 / num2
            case "modulo":
                result = num1 % num2
            case "int_divide":
                result = num1 // num2
            case "power":
                result = num1 ** num2
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
    return result

print(calc("two", "four"))


#Task 4.
def data_type_conversion(value, data_type):
    try:
        if data_type == "float":
            return float(value)
        elif data_type == "str":
            return str(value)
        elif data_type == "int":
            return int(value)
        else:
            return f"You can't convert {value} into a {data_type}."
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {data_type}."

print(data_type_conversion("two", "int"))


#Task 5.
def grade(*args):
    if len(args) == 0:
        return "No data was provided."
    try:
        average = sum(args) / len(args)
        if average < 60:
            return "F"
        elif average < 70:
            return "D"
        elif average < 80:
            return "C"
        elif average < 90:
            return "B"
        else:
            return "A"
    except TypeError:
        return "Invalid data was provided."

print(grade("two", 6))


#Task 6.
def repeat(string, count):
    new_string = ""
    for i in range(count):
        new_string += string
    return new_string

print(repeat("hello", 5))


# Task 7.
def student_scores(pos_parameter, **kwargs):
    if pos_parameter == "best":
        best_student = None
        best_score = 0
        for student, score in kwargs.items():
            if score > best_score:
                best_score = score
                best_student = student
        return best_student

    if pos_parameter == "mean":
        total = 0
        for value in kwargs.values():
            total += value
        average = total / len(kwargs)
        return average

print(student_scores("mean", Tom=75, Dick=89, Angela=91))


#Task 8.
def titleize(title):
    little_words = {"a", "on", "an", "the", "of", "and", "is","in"}
    words = title.split(" ")

    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1:
            words[i] = word.capitalize()

        elif word not in little_words:
            words[i] = word.capitalize()

    return " ".join(words)

print(titleize("a separate peace"))


#Task 9.
def hangman(secret, guess):
    guess_set = set(guess)
    result = ""

    for letter in secret:
        if letter in guess_set:
            result += letter
        else:
            result += "_"

    return result

print(hangman("alphabet", "ab"))


# Task 10.
def pig_latin(text):
    vowels = set("aeiou")
    text_list = text.split(" ")
    new_text_list = []

    for word in text_list:
        if word[0] in vowels:
            new_word = word + "ay"
            new_text_list.append(new_word)
        else:
            for i, letter in enumerate(word):
                if letter in vowels:
                    new_word = word[i:] + word[0:i] + "ay"
                    new_text_list.append(new_word)
                    break
                if word[i] == "q" and word[i+1] == "u":
                    new_word = word[i+2:] + word[0:i+2] + "ay"
                    new_text_list.append(new_word)
                    break
    return " ".join(new_text_list)

print(pig_latin("the quick brown fox"))
