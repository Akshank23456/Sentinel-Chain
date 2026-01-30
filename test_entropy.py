#!/usr/bin/env python3
"""
Test script for entropy calculation
"""

import os
import math
from collections import Counter

def calculate_entropy(file_path):
    """
    Calculate Shannon entropy of a file in binary.

    Args:
        file_path (str): Path to the file to analyze

    Returns:
        float: Shannon entropy value (0-8 bits per byte)
    """
    try:
        # Initialize byte counter and total data length
        byte_counts = Counter()
        data_len = 0
        chunk_size = 8192  # Read in 8KB chunks to avoid memory issues

        # Read file in binary mode in chunks
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                byte_counts.update(chunk)
                data_len += len(chunk)

        # Empty file has zero entropy
        if data_len == 0:
            return 0.0

        # Calculate entropy
        entropy = 0.0

        for count in byte_counts.values():
            # Calculate probability of this byte
            probability = count / data_len
            # Add to entropy sum: -p * log2(p)
            entropy -= probability * math.log2(probability)

        return entropy

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return 0.0
    except PermissionError:
        print(f"Error: Permission denied - {file_path}")
        return 0.0
    except Exception as e:
        print(f"Error calculating entropy for {file_path}: {e}")
        return 0.0

if __name__ == "__main__":
    # Test with empty file
    empty_file = "MyData/empty.txt"
    entropy = calculate_entropy(empty_file)
    print(f"Entropy of empty file: {entropy} (expected: 0.0)")

    # Test with a text file
    text_file = "MyData/test.txt"
    with open(text_file, 'w') as f:
        f.write("Hello World")
    entropy = calculate_entropy(text_file)
    print(f"Entropy of 'Hello World': {entropy:.4f}")

    # Test with random data (high entropy)
    random_file = "MyData/random.bin"
    import random
    with open(random_file, 'wb') as f:
        f.write(bytes([random.randint(0, 255) for _ in range(1000)]))
    entropy = calculate_entropy(random_file)
    print(f"Entropy of random data: {entropy:.4f} (expected: close to 8.0)")

    # Test with large file
    large_file = "MyData/large.bin"
    entropy = calculate_entropy(large_file)
    print(f"Entropy of large file: {entropy:.4f}")

    print("Tests completed.")
