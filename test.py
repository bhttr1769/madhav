# Calculator Program

class Calculator:
    def __init__(self):
        pass
    
    # Method to add two numbers
    def add(self, a, b):
        return a + b
    
    # Method to subtract two numbers
    def subtract(self, a, b):
        return a - b
    
    # Method to multiply two numbers
    def multiply(self, a, b):
        return a * b
    
    # Method to divide two numbers
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# Main function to run the calculator
def main():
    calc = Calculator()
    
    while True:
        print("\nChoose an operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")
        
        choice = input("Enter your choice (1/2/3/4/5): ")
        
        if choice == '5':
            break
        
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == '1':
                print(f"{num1} + {num2} = {calc.add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {calc.subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {calc.multiply(num1, num2)}")
            elif choice == '4':
                print(f"{num1} / {num2} = {calc.divide(num1, num2)}")
            else:
                print("Invalid input. Please try again.")
        
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()