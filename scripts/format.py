#!/usr/bin/env python3
"""Script for automatically formatting code."""

import subprocess
import sys


def main():
    """Run all formatting commands."""
    print("🎨 Formatting code...\n")
    
    commands = [
        ("black app/", "Code formatting (Black)"),
        ("isort app/", "Import sorting (isort)"),
    ]
    
    for command, description in commands:
        print(f"🚀 {description}...")
        subprocess.run(command, shell=True)
        print(f"✅ {description} completed!")
    
    print("\n✨ Formatting complete! You can now run: poetry run lint")
    sys.exit(0)


if __name__ == "__main__":
    main()