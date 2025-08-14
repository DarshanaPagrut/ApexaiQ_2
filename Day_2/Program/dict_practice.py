# """
# Question 1:
# Create a dictionary with numbers from 1 to 4 as keys and their cubes as values, 
# but only include even numbers.
# """
dict_cubes_even = {num: num ** 3 for num in range(1, 5) if num % 2 == 0}
print(dict_cubes_even)


# """
# Question 2:
# Create a dictionary from a list of words where the key is the word 
# and the value is its length.
# """
words = ["apple", "banana", "cat", "dog"]
dict_word_length = {word: len(word) for word in words}
print(dict_word_length)


# """
# Question 3:
# Create a dictionary from a list of numbers where the key is the number 
# and the value is its square, only for even numbers.
# """
numbers = [1, 2, 3, 4, 5, 6]
dict_square_even = {num: num ** 2 for num in numbers if num % 2 == 0}
print(dict_square_even)


# """
# Question 4:
# Create a dictionary from a list of fruits where the key is the fruit 
# and the value is its length, but only include fruits starting with 'a'.
# """
fruits = ["apple", "banana", "apricot", "cherry"]
dict_fruit_a = {fruit: len(fruit) for fruit in fruits if fruit[0] == "a"}
print(dict_fruit_a)


# """
# Question 5:
# Create a dictionary from student scores where only scores >= 90 are included.
# """
student_scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "David": 95}
dict_high_scores = {name: score for name, score in student_scores.items() if score >= 90}
print(dict_high_scores)


# """
# Question 6:
# Convert keys to uppercase in a dictionary where the value is even.
# """
data = {"one": 1, "two": 2, "three": 3, "four": 4}
dict_upper_even = {key.upper(): value for key, value in data.items() if value % 2 == 0}
print(dict_upper_even)


# """
# Question 7:
# Count the frequency of each character in a string, excluding spaces.
# """
sentence = "hello world"
dict_char_count = {char: sentence.count(char) for char in set(sentence) if char != ' '}
print(dict_char_count)


# """
# Question 8:
# Convert Celsius temperatures to Fahrenheit for days where the temperature is greater than 20°C.
# """
celsius_temps = {"Mon": 20, "Tue": 22, "Wed": 18, "Thu": 25}
fahrenheit_temp = {
    day: (temp * (9 / 5)) + 32 for day, temp in celsius_temps.items() if temp > 20
}
print(fahrenheit_temp)


# """
# Question 9:
# Swap keys and values in a dictionary.
# """
cities = {"New York": "USA", "London": "UK", "Paris": "France"}
dict_swap = {value: key for key, value in cities.items()}
print(dict_swap)


# """
# Question 10:
# Create a dictionary from a list of key-value pairs (sublists).
# """
pairs = [["a", 1], ["b", 2], ["c", 3]]
dict_from_pairs = {sublist[0]: sublist[1] for sublist in pairs}
print(dict_from_pairs)


# """
# Question 11:
# Count the number of even and odd numbers in a list and store in a dictionary.
# """
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 10]
dict_even_odd_count = {
    'even_count': sum(1 for num in numbers if num % 2 == 0),
    'odd_count': sum(1 for num in numbers if num % 2 != 0)
}
print(dict_even_odd_count)
