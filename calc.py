# A basic arithmetic calculator

import operator

def add(a, b):
    return operator.add(a, b)

def subtract(a, b):
    return operator.sub(a, b)

def multiply(a, b):
    return operator.mul(a, b)

def divide(a, b):
    try:
        return operator.truediv(a, b)
    except ZeroDivisionError:
        return "Error: Division by zero"

def get_user_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid number.")

def calculator():
    print("Professional Optimized Calculator")
    operations = {'1': add, '2': subtract, '3': multiply, '4': divide}

    while True:
        print("1. Add\n2. Subtract\n3. Multiply\n4. Divide\n5. Exit")
        choice = input("Enter choice (1/2/3/4/5): ")

        if choice == '5':
            print("Exiting the calculator.")
            break

        if choice in operations:
            num1 = get_user_input("Enter first number: ")
            num2 = get_user_input("Enter second number: ")
            result = operations[choice](num1, num2)
            print("Result:", result)
        else:
            print("Error: Invalid input. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    calculator()
