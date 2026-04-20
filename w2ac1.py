"""
Generate by Trae
Debug by ElbertS
"""

import math

from typing import Union, Optional

Numeric = Union[int, float, complex]

def arithmetic_ops(a: Numeric, b: Numeric, op: str) -> Numeric:
    """
    Performs basic arithmetic operations (+, -, *, /, %) on real and complex numbers.
    """
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b
    elif op == '%':
        if isinstance(a, complex) or isinstance(b, complex):
            raise TypeError("Modulo operation is not supported for complex numbers.")
        if b == 0:
            raise ValueError("Modulo by zero is not allowed.")
        return a % b
    else:
        raise ValueError(f"Unsupported operator: {op}")

def parse_input(value_str: str) -> Numeric:
    """
    Tries to parse input as a complex number or a float.
    """
    try:
        return complex(value_str.replace(' ', ''))
    except ValueError:
        try:
            return float(value_str)
        except ValueError:
            raise ValueError(f"Invalid numeric input: '{value_str}'")

def display_operation(a: Numeric, b: Numeric, op: str) -> Optional[Numeric]:
    """
    Executes an arithmetic operation and displays the formatted result.
    """
    try:
        result = arithmetic_ops(a, b, op)
        print(f"Result: {a} {op} {b} = {result}")
        return result
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        return None

def main():
    print("=== Interactive Math Operations ===")
    print("Supports: +, -, *, /, %")
    print("Numeric formats: 10, 5.5, 2+3j, etc.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            input_a = input("Enter first number (or 'exit'): ").strip()
            if input_a.lower() == 'exit':
                break
            
            op = input("Enter operator (+, -, *, /, %): ").strip()
            
            input_b = input("Enter second number: ").strip()
            
            a = parse_input(input_a)
            b = parse_input(input_b)
            
            display_operation(a, b, op)
            print("-" * 20)
            
        except ValueError as e:
            print(f"Input Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
