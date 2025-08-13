# """
# Question 1:
# Append 'orange' to a fruit list and remove 'banana'.
# """
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
fruits.remove("banana")
print(fruits)


# """
# Question 2:
# Print the 3rd element (index 2) from a number list.
# """
numbers = [1, 2, 3, 4, 5]
print(numbers[2])


# """
# Question 3:
# Replace 'green' with 'yellow' in a color list.
# """
colors = ["red", "green", "blue"]
colors[1] = "yellow"
print(colors)


# """
# Question 4:
# Print each fruit from the list using a loop.
# """
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)


# """
# Question 5:
# Calculate and print the average of a list of grades.
# """
grades = [85, 90, 78, 92, 88]
total_sum = 0
for x in grades:
    total_sum += x
average = total_sum / len(grades)
print(average)


# """
# Question 6:
# Find the largest number from a list of ages.
# """
ages = [22, 35, 19, 45, 30]
print(max(ages))


# """
# Question 7:
# Print words longer than 5 characters from a list.
# """
words = ["hello", "world", "python", "programming"]
for x in words:
    if len(x) > 5:
        print(x)


# """
# Question 8:
# Create a list of squares from 1 to 10.
# """
new_list = [x * x for x in range(1, 11)]
print(new_list)


# """
# Question 9:
# Join words into a single sentence with spaces.
# """
sentence = ["I", "love", "Python"]
joined_sentence = " ".join(sentence)
print(joined_sentence)


# """
# Question 10:
# Reverse a list using slicing.
# """
my_list = [10, 20, 30, 40, 50, 60]
print(my_list[::-1])


# """
# Question 11:
# Create a list of squares for even numbers from 0 to 10.
# """
even_squares = [x * x for x in range(11) if x % 2 == 0]
print(even_squares)


# """
# Question 12:
# Convert each word in a list to uppercase.
# """
words = ["apple", "banana", "cherry"]
upper_words = [x.upper() for x in words]
print(upper_words)


# """
# Question 13:
# Create a list of word lengths from a given list.
# """
words = ["cat", "dog", "elephant", "fox"]
word_lengths = [len(x) for x in words]
print(word_lengths)


# """
# Question 14:
# Filter numbers greater than 5 from a list.
# """
numbers = [1, 7, 3, 9, 2, 8]
greater_than_5 = [x for x in numbers if x > 5]
print(greater_than_5)


# """
# Question 15:
# Create a list of fruits that start with 'p'.
# """
fruits = ["apple", "pear", "grape", "pineapple"]
start_with_p = [x for x in fruits if x[0] == "p"]
print(start_with_p)


# """
# Question 16:
# Remove vowels from a string and store the result in a list.
# """
text = "programming"
vowels = {'a', 'e', 'i', 'o', 'u'}
no_vowel_list = [x for x in text if x not in vowels]
print(no_vowel_list)


# """
# Question 17:
# Create a list of double the numbers from 1 to 20, only for odd numbers.
# """
double_odds = [2 * x for x in range(1, 21) if x % 2 != 0]
print(double_odds)


# """
# Question 18:
# Convert words longer than 3 characters to uppercase from a sentence.
# """
sentence = "The quick brown fox jumps over the lazy dog"
upper_words_long = [x.upper() for x in sentence.split() if len(x) > 3]
print(upper_words_long)


# """
# Question 19:
# Count the number of vowels in each word of a list.
# """
words = ["apple", "banana", "kiwi"]
vowels = {'a', 'e', 'i', 'o', 'u'}
vowel_counts = [sum(1 for y in x if y in vowels) for x in words]
print(vowel_counts)


# """
# Question 20:
# Create a dictionary by zipping two lists together.
# """
keys = ["name", "age", "city"]
values = ["Alice", 30, "New York"]
dict_from_lists = {key: value for key, value in zip(keys, values)}
print(dict_from_lists)
