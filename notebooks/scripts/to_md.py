import argparse
import os
import sys

from datalab_sdk import DatalabClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATALAB_KEY = os.getenv("DATALAB_API_KEY")

if not DATALAB_KEY:
    print("Error: DATALAB_API_KEY is not set. Set it in the environment or .env file.", file=sys.stderr)
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a PDF document to Markdown using Datalab SDK."
    )
    parser.add_argument(
        "input_pdf",
        help="Path to the input PDF file to convert.",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="output",
        help="Directory to save the converted Markdown and assets. Defaults to 'output'.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_pdf = args.input_pdf
    output_dir = args.output_dir

    if not os.path.isfile(input_pdf):
        print(f"Error: input PDF not found: {input_pdf}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    client = DatalabClient(api_key=DATALAB_KEY)

    result = client.convert(input_pdf)
    print(result.markdown)  # type: ignore
    result.save_output(output_dir)  # type: ignore
    print(f"Saved converted output to: {output_dir}")


if __name__ == "__main__":
    main()