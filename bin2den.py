# Basic Binary to Denary converter

def binary_to_decimal(binary_str):
    try:
        decimal_num = int(binary_str, 2)
        return decimal_num
    except ValueError:
        raise ValueError("Invalid binary number")

def main():
    while True:
        user_binary = input("Enter a binary number: ")
        
        if all(bit in '01' for bit in user_binary):
            output = binary_to_decimal(user_binary)
            print(f"Decimal equivalent: {output}")
        else:
            print("Invalid binary number")

        loop_question = input("Press 'R' to input another value or press any other key to exit: ")
        if loop_question.lower() != 'r':
            break

if __name__ == "__main__":
    main()
