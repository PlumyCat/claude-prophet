#!/usr/bin/env python3
"""
Extract tutorial content from video frames using Azure OpenAI GPT-4.1-mini vision.

Usage:
    python extract_frames.py --frames-dir /path/to/frames --output tutorial.md
    python extract_frames.py --frames-dir /path/to/frames --sample-rate 12  # 1 frame per minute (if 5sec intervals)
"""

import os
import base64
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
from tqdm import tqdm

load_dotenv(override=True)


def get_client() -> AzureOpenAI:
    """Initialize Azure OpenAI client."""
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )


def encode_image(image_path: Path) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_frame_content(client: AzureOpenAI, image_path: Path, deployment: str) -> str:
    """Extract text content from a single frame using vision model."""
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": """You are an assistant that extracts text content from screenshots of a Claude Code video tutorial.

For each frame, extract:
1. Commands typed in the terminal
2. Code displayed (with the language if identifiable)
3. Claude's messages/responses
4. Important instructions or comments

Format your response in a structured and concise manner. If the frame is similar to the previous one or contains nothing new, simply respond "SKIP".
"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the important content from this tutorial screenshot:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000,
        temperature=0.1,
    )

    return response.choices[0].message.content


def get_frame_timestamp(frame_name: str, interval_seconds: int = 5) -> str:
    """Convert frame number to timestamp."""
    # Extract frame number from name like "frame_00001.jpg"
    frame_num = int(frame_name.split("_")[1].split(".")[0])
    total_seconds = (frame_num - 1) * interval_seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def main():
    parser = argparse.ArgumentParser(description="Extract tutorial content from video frames")
    parser.add_argument("--frames-dir", required=True, help="Directory containing frame images")
    parser.add_argument("--output", default="tutorial_extracted.md", help="Output markdown file")
    parser.add_argument("--sample-rate", type=int, default=12, help="Process every Nth frame (default: 12 = 1/min at 5sec intervals)")
    parser.add_argument("--start-frame", type=int, default=1, help="Start from this frame number")
    parser.add_argument("--end-frame", type=int, default=None, help="End at this frame number")
    parser.add_argument("--deployment", default=None, help="Azure OpenAI deployment name (overrides .env)")
    args = parser.parse_args()

    frames_dir = Path(args.frames_dir)
    if not frames_dir.exists():
        print(f"Error: Directory {frames_dir} does not exist")
        return

    # Get all frame files
    frame_files = sorted(frames_dir.glob("frame_*.jpg"))
    if not frame_files:
        frame_files = sorted(frames_dir.glob("frame_*.png"))

    if not frame_files:
        print(f"Error: No frame files found in {frames_dir}")
        return

    print(f"Found {len(frame_files)} frames")

    # Filter frames based on sample rate and range
    selected_frames = []
    for i, frame in enumerate(frame_files):
        frame_num = int(frame.name.split("_")[1].split(".")[0])
        if frame_num < args.start_frame:
            continue
        if args.end_frame and frame_num > args.end_frame:
            break
        if (i % args.sample_rate) == 0:
            selected_frames.append(frame)

    print(f"Processing {len(selected_frames)} frames (sample rate: 1/{args.sample_rate})")

    # Initialize client
    client = get_client()
    deployment = args.deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")

    # Process frames
    results = []
    for frame_path in tqdm(selected_frames, desc="Extracting content"):
        timestamp = get_frame_timestamp(frame_path.name)
        try:
            content = extract_frame_content(client, frame_path, deployment)
            if content and content.strip().upper() != "SKIP":
                results.append({
                    "frame": frame_path.name,
                    "timestamp": timestamp,
                    "content": content
                })
        except Exception as e:
            print(f"\nError processing {frame_path.name}: {e}")
            continue

    # Write output
    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Tutorial Extraction - Claude Code Multi-Agent System\n\n")
        f.write(f"Extracted from {len(selected_frames)} frames (sample rate: 1/{args.sample_rate})\n\n")
        f.write("---\n\n")

        for result in results:
            f.write(f"## [{result['timestamp']}] {result['frame']}\n\n")
            f.write(result['content'])
            f.write("\n\n---\n\n")

    print(f"\nExtraction complete! Output saved to: {output_path}")
    print(f"Processed {len(results)} frames with content (skipped {len(selected_frames) - len(results)} similar frames)")


if __name__ == "__main__":
    main()
