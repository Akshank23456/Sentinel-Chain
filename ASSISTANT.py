"""
Test script to demonstrate the entropy monitor.
Creates files with different entropy levels.
"""

import os
import random
import time

# Create MyData folder if it doesn't exist
os.makedirs('MyData', exist_ok=True)

print("Creating test files in MyData folder...")
print("=" * 70)

# Test 1: Low entropy file (repeated text)
print("\n1. Creating LOW entropy file (repeated text)...")
with open('MyData/low_entropy.txt', 'w') as f:
    f.write('A' * 1000)  # Repeated character = very low entropy
time.sleep(0.5)

# Test 2: Medium entropy file (normal text)
print("2. Creating MEDIUM entropy file (normal text)...")
with open('MyData/medium_entropy.txt', 'w') as f:
    text = "This is a normal text file with regular English content. " * 20
    f.write(text)
time.sleep(0.5)

# Test 3: High entropy file (random data - simulating encrypted/compressed)
print("3. Creating HIGH entropy file (random bytes - like encrypted data)...")
with open('MyData/high_entropy.bin', 'wb') as f:
    random_bytes = bytes(random.randint(0, 255) for _ in range(1000))
    f.write(random_bytes)
time.sleep(0.5)

# Test 4: Modify an existing file
print("4. Modifying the high entropy file...")
time.sleep(1)
with open('MyData/high_entropy.bin', 'ab') as f:
    random_bytes = bytes(random.randint(0, 255) for _ in range(500))
    f.write(random_bytes)

print("\n" + "=" * 70)
print("Test files created! Check the monitor output above.")
print("=" * 70)
