#!/usr/bin/env python3
"""
Simple runner script for the painting pipeline.
Usage: python run.py input/your_photo.jpg
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(override=True)  # Override shell env vars with .env values

from src.pipeline import PaintingPipeline


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <input_image_path> [session_name]")
        print("\nExample:")
        print("  python run.py input/L1080585.jpg my_painting")
        sys.exit(1)

    input_path = sys.argv[1]
    session_name = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    print(f"Starting painting pipeline for: {input_path}")

    pipeline = PaintingPipeline(output_dir="output")
    results = pipeline.run_full_pipeline(
        input_image_path=input_path,
        session_name=session_name,
    )

    if results["success"]:
        print(f"\nSuccess! Check output at: {results['session_dir']}")
    else:
        print("\nPipeline completed with errors.")

    return 0 if results["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
