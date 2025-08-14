# """
# Question 1:
# Write to a text file called 'example.txt' with some sample content.
# """
with open("example.txt", "w") as file:
    file.write("Hello, this is a sample text file.\n")
    file.write("Python file handling example.\n")


# """
# Question 2:
# Read the contents of 'example.txt' and print them.
# """
try:
    with open("example.txt", "r") as file:
        content = file.read()
    print(content)
except FileNotFoundError:
    print("Error: File not found!")


# """
# Question 3:
# Append text to an existing file.
# """
with open("example.txt", "a") as file:
    file.write("This line is appended to the file.\n")


# """
# Question 4:
# Read a file line by line and print each line without extra newlines.
# """
try:
    with open("example.txt", "r") as file:
        for line in file:
            print(line.strip())
except FileNotFoundError:
    print("Error: File not found!")


# """
# Question 5:
# Write a list of strings to a file using writelines().
# """
lines = ["First line\n", "Second line\n", "Third line\n"]
with open("list_lines.txt", "w") as file:
    file.writelines(lines)


# """
# Question 6:
# Read only the first line from a file.
# """
try:
    with open("list_lines.txt", "r") as file:
        first_line = file.readline()
    print(first_line.strip())
except FileNotFoundError:
    print("Error: File not found!")


# """
# Question 7:
# Read all lines into a list.
# """
try:
    with open("list_lines.txt", "r") as file:
        all_lines = file.readlines()
    print(all_lines)
except FileNotFoundError:
    print("Error: File not found!")


# """
# Question 8:
# Count the number of words in a file.
# """
try:
    with open("example.txt", "r") as file:
        text = file.read()
    word_count = len(text.split())
    print(f"Word count: {word_count}")
except FileNotFoundError:
    print("Error: File not found!")


# """
# Question 9:
# Copy the contents of one file to another.
# """
try:
    with open("example.txt", "r") as source_file:
        data = source_file.read()

    with open("copy_example.txt", "w") as target_file:
        target_file.write(data)

    print("File copied successfully.")
except FileNotFoundError:
    print("Error: Source file not found!")


# """
# Question 10:
# Check if a file exists before reading.
# """
import os

file_name = "example.txt"
if os.path.exists(file_name):
    with open(file_name, "r") as file:
        print(file.read())
else:
    print(f"Error: '{file_name}' does not exist.")
