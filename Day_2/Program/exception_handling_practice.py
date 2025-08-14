# """
# Question 1:
# Write a program to divide 10 by 5 and handle division by zero using try-except.
# """

try:
    div = 10 / 5
    print(div)
except ZeroDivisionError:
    print("Error: Cannot divide by zero")


# """
# Question 2:
# Convert a user input into an integer and divide 10 by it.
# Handle:
# - ValueError for invalid integers
# - ZeroDivisionError for division by zero
# - Any other exception with a generic error message
# """

print("Convert number into integer and then divide 10 by it")

try:
    num = input("Enter the number: ")
    integer = int(num)
    print(f"Converted integer is: {integer}")

    div = 10 / integer
    print(f"10 divided by {integer} is: {div}")

except ValueError:
    print("Enter a whole number (integer)")
except ZeroDivisionError:
    print("Error: Cannot divide by zero")
except Exception as e:
    print(f"Something went wrong: {e}")
finally:
    print("Attempted")


# """
# Question 3:
# Read the first line from a file named 'names.txt'.
# Handle:
# - FileNotFoundError if file doesn't exist
# - Ensure file is closed in finally block
# """

try:
    file = open("names.txt", "r")
    content = file.readline()
except FileNotFoundError:
    print("Error: File not found!")
else:
    print(content)
finally:
    # Ensure file is closed if it was successfully opened
    try:
        file.close()
    except NameError:
        pass
