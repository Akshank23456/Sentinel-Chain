
"""
Folder Monitor with Shannon Entropy Detection
Monitors the 'MyData' folder for file changes and calculates entropy.
High entropy (>7.5) may indicate encrypted, compressed, or randomized data.
"""

import os
import sys
import time
import math
import hashlib
from collections import Counter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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


def calculate_hash(file_path):
    """
    Calculate SHA256 hash of a file.

    Args:
        file_path (str): Path to the file to hash

    Returns:
        str: SHA256 hash in hexadecimal format
    """
    try:
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None


class EntropyMonitorHandler(FileSystemEventHandler):
    """Handler for file system events that calculates entropy on changes."""
    
    def __init__(self, entropy_threshold=7.5):
        """
        Initialize the handler.
        
        Args:
            entropy_threshold (float): Entropy threshold for alerts
        """
        self.entropy_threshold = entropy_threshold
        super().__init__()
    
    def process_file(self, file_path, event_type):
        """
        Process a file and check its entropy.
        
        Args:
            file_path (str): Path to the file
            event_type (str): Type of event (created/modified)
        """
        # Skip directories
        if os.path.isdir(file_path):
            return
        
        # Skip temporary and hidden files
        if os.path.basename(file_path).startswith('.'):
            return
        
        print(f"\n[{event_type.upper()}] {file_path}")
        
        # Calculate entropy
        entropy = calculate_entropy(file_path)
        print(f"Shannon Entropy: {entropy:.4f} bits/byte")
        
        # Check if entropy exceeds threshold
        if entropy > self.entropy_threshold:
            print("=" * 70)
            print("🚨 HIGH-PRIORITY ALERT 🚨")
            print(f"File: {file_path}")
            print(f"Entropy: {entropy:.4f} bits/byte (threshold: {self.entropy_threshold})")
            print("WARNING: High entropy detected! This may indicate:")
            print("  - Encrypted data")
            print("  - Compressed files")
            print("  - Random/obfuscated content")
            print("  - Potential malware activity")
            print("=" * 70)

            # Pass to entropy analysis (already done above)
            print("🔍 Passing to entropy analysis... Analysis complete.")

            # Calculate digital hash for blockchain
            file_hash = calculate_hash(file_path)
            if file_hash:
                print(f"🔐 Digital Hash (SHA256): {file_hash}")
                print("📤 Path to Blockchain: Ready for immutable storage.")
                print("   -> Transmit hash to blockchain network for permanent record.")
                print("   -> Use hash as unique identifier for file integrity verification.")
            else:
                print("❌ Failed to calculate hash.")
            print("=" * 70)
    
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            # Small delay to ensure file is fully written
            time.sleep(0.1)
            self.process_file(event.src_path, "created")
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory:
            # Small delay to ensure file is fully written
            time.sleep(0.1)
            self.process_file(event.src_path, "modified")


def main():
    """Main function to start the folder monitor."""
    # Define the folder to monitor
    monitor_folder = os.path.join(os.path.dirname(__file__), 'MyData')
    
    # Create the folder if it doesn't exist
    if not os.path.exists(monitor_folder):
        print(f"Creating folder: {monitor_folder}")
        os.makedirs(monitor_folder)
    
    # Get absolute path
    monitor_path = os.path.abspath(monitor_folder)
    
    print("=" * 70)
    print("Shannon Entropy File Monitor")
    print("=" * 70)
    print(f"Monitoring folder: {monitor_path}")
    print(f"Entropy threshold: 7.5 bits/byte")
    print("Press Ctrl+C to stop monitoring...")
    print("=" * 70)
    
    # Create event handler and observer
    event_handler = EntropyMonitorHandler(entropy_threshold=7.5)
    observer = Observer()
    observer.schedule(event_handler, monitor_path, recursive=True)
    
    # Start monitoring
    try:
        observer.start()
        print("Observer started successfully.")
    except Exception as e:
        print(f"Error starting observer: {e}")
        return
    
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping monitor...")
        observer.stop()
    
    observer.join()
    print("Monitor stopped.")


if __name__ == "__main__":
    main()
