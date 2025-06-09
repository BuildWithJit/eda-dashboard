#!/usr/bin/env python3
"""
EDA Dashboard - Run Script
Simple script to launch the Streamlit application
"""

import subprocess
import sys


def main():
    """Launch the Streamlit EDA Dashboard"""

    print("🚀 Starting EDA Dashboard...")
    print("📊 Loading Streamlit application...")

    try:
        # Run the streamlit app
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "main.py",
                "--theme.base",
                "light",
                "--theme.backgroundColor",
                "#FFFFFF",
                "--theme.secondaryBackgroundColor",
                "#F0F2F6",
            ]
        )

    except KeyboardInterrupt:
        print("\n👋 Thanks for using EDA Dashboard!")

    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")


if __name__ == "__main__":
    main()
