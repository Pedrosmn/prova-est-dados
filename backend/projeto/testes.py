# backend/testes.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.routes import generate_binary_tree, generate_fibonacci_tree

# Teste BST
print("Testing BST...")
bst_image = generate_binary_tree(5, 3, [10, 15])
print(f"BST Image (first 50 chars): {bst_image[:50]}...")

from app.routes import generate_binary_tree, generate_fibonacci_tree

# Teste Fibonacci com diferentes valores
for n in range(1, 8):
    print(f"\nTesting Fibonacci({n})...")
    fib_image = generate_fibonacci_tree(n)
    print(f"Fibonacci Image (first 50 chars): {fib_image[:50]}...")