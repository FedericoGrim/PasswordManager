# GitHub Copilot Custom Instructions

## Core Programming Principles
- **Adhere to core principles:** Always follow SOLID, KISS, SRP (Single Responsibility Principle), and DRY (Don't Repeat Yourself).
- **Clean Code Philosophy:** Code must be self-explanatory. Use comments ONLY to explain the "why" (intent) behind complex decisions, never the "what" (obvious logic).

## Structural Rules
- **Single Responsibility Principle (SRP):** Strictly break down functions. If a function handles more than 3 arguments or contains excessive logic, refactor it into smaller, focused modules or functions.
- **Vertical Whitespace:** Use blank lines to logically segment code blocks. This improves visual navigation between different areas of responsibility.
- **Code Organization:** Maintain a consistent structure. Place class definitions and main functions at the top of the file, immediately following the import statements.
- **Variable Grouping:** Group logically related variables together, even if it creates a slight separation from the immediate logic, to maintain block coherence.

## Readability & Logic
- **Multi-line Logic:** Avoid complex one-line expressions and one-line conditional logic (if/else). Spread logic across multiple lines to enhance readability and facilitate debugging.
- **Avoid Method Chaining:** Do not use long method chains (e.g., `obj.methodA().methodB().methodC()`). Break operations into intermediate steps using descriptive variable names.
- **Clarity over Brevity:** Always prioritize readability. Prefer creating intermediate variables to explain steps rather than nesting multiple function calls in a single statement.

## Language Applicability
- Apply these rules consistently across all programming languages, including but not limited to **Python**, **C#**, **JavaScript**, and **TypeScript**.

## Summary Example Style
Instead of:
```python
print(f"Total: {unitaryPrice(float(input()), calculateArea(float(input()), float(input())))}")```

Follow this style:
```# Imports
import math

def calculate_area(width, height):
    area = width * height
    return area

def get_total_price(price, area):
    total = price * area
    return total

width = float(input("Enter width: "))
height = float(input("Enter height: "))
area = calculate_area(width, height)

price = float(input("Enter price: "))
final_price = get_total_price(price, area)

print(f"Calculated Area: {area}")
print(f"Total Price: {final_price}")```
