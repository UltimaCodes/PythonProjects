# Basic Binary, Denary and Hexadecimal converter

def binary_to_decimal(binary_str):
    try:
        decimal_num = int(binary_str, 2)
        return decimal_num
    except ValueError:
        raise ValueError("Invalid binary number")

def decimal_to_binary(decimal_num):
    try:
        decimal_num = int(decimal_num)
        return bin(decimal_num)[2:]  # Remove the '0b' prefix
    except ValueError:
        raise ValueError("Invalid decimal number")

def decimal_to_hex(decimal_num):
    try:
        decimal_num = int(decimal_num)
        return hex(decimal_num)[2:]  # Remove the '0x' prefix
    except ValueError:
        raise ValueError("Invalid decimal number")

def hex_to_decimal(hex_str):
    try:
        decimal_num = int(hex_str, 16)
        return decimal_num
    except ValueError:
        raise ValueError("Invalid hexadecimal number")

def binary_to_hex(binary_str):
    decimal_num = binary_to_decimal(binary_str)
    return decimal_to_hex(decimal_num)

def hex_to_binary(hex_str):
    decimal_num = hex_to_decimal(hex_str)
    return decimal_to_binary(decimal_num)

def main():
    while True:
        print("\nChoose an option:")
        print("1: Binary to Decimal")
        print("2: Decimal to Binary")
        print("3: Decimal to Hexadecimal")
        print("4: Hexadecimal to Decimal")
        print("5: Binary to Hexadecimal")
        print("6: Hexadecimal to Binary")
        print("7: Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            binary_str = input("Enter a binary number: ")
            try:
                print(f"Decimal equivalent: {binary_to_decimal(binary_str)}")
            except ValueError as e:
                print(e)
        
        elif choice == '2':
            decimal_num = input("Enter a decimal number: ")
            try:
                print(f"Binary equivalent: {decimal_to_binary(decimal_num)}")
            except ValueError as e:
                print(e)
        
        elif choice == '3':
            decimal_num = input("Enter a decimal number: ")
            try:
                print(f"Hexadecimal equivalent: {decimal_to_hex(decimal_num)}")
            except ValueError as e:
                print(e)
        
        elif choice == '4':
            hex_str = input("Enter a hexadecimal number: ")
            try:
                print(f"Decimal equivalent: {hex_to_decimal(hex_str)}")
            except ValueError as e:
                print(e)
        
        elif choice == '5':
            binary_str = input("Enter a binary number: ")
            try:
                print(f"Hexadecimal equivalent: {binary_to_hex(binary_str)}")
            except ValueError as e:
                print(e)
        
        elif choice == '6':
            hex_str = input("Enter a hexadecimal number: ")
            try:
                print(f"Binary equivalent: {hex_to_binary(hex_str)}")
            except ValueError as e:
                print(e)
        
        elif choice == '7':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
