#!/usr/bin/env python3
"""
Multi-Agent Translation System - Main Entry Point

This system performs round-trip translation quality testing between Hebrew, English, and French
using a multi-agent architecture with Claude Sonnet.

Architecture:
  - Agent 1: Hebrew → English
  - Agent 2: English → French
  - Agent 3: French → Hebrew
  - Orchestrator: Coordinates workflow and performs quality analysis

Usage:
  python main.py --sentences 20 --round-trip
  python main.py --sentences 50 --no-round-trip --topic "technology"
  python main.py --help
"""

import argparse
import sys
from orchestrator import OrchestratorAgent
import config


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Translation System with Round-Trip Quality Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 20 sentences with round-trip analysis
  python main.py --sentences 20

  # Generate 50 sentences without round-trip analysis
  python main.py --sentences 50 --no-round-trip

  # Generate 30 sentences on a specific topic
  python main.py --sentences 30 --topic "science and technology"

  # Use custom number of sentences
  python main.py -n 15
        """
    )

    parser.add_argument(
        '-n', '--sentences',
        type=int,
        default=20,
        help=f'Number of sentences to generate ({config.MIN_SENTENCES}-{config.MAX_SENTENCES}). Default: 20'
    )

    parser.add_argument(
        '--round-trip',
        action='store_true',
        default=True,
        help='Perform round-trip quality analysis (default: True)'
    )

    parser.add_argument(
        '--no-round-trip',
        action='store_false',
        dest='round_trip',
        help='Skip round-trip quality analysis'
    )

    parser.add_argument(
        '--topic',
        type=str,
        default=None,
        help='Optional topic/domain for sentence generation (e.g., "technology", "nature")'
    )

    return parser.parse_args()


def validate_arguments(args):
    """Validate command line arguments."""
    errors = []

    # Validate number of sentences
    if args.sentences < config.MIN_SENTENCES:
        errors.append(f"Number of sentences must be at least {config.MIN_SENTENCES}")
    if args.sentences > config.MAX_SENTENCES:
        errors.append(f"Number of sentences must not exceed {config.MAX_SENTENCES}")

    if errors:
        print("Error: Invalid arguments\n", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        print("\nUse --help for usage information", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    # Parse and validate arguments
    args = parse_arguments()
    validate_arguments(args)

    try:
        # Initialize orchestrator
        orchestrator = OrchestratorAgent()

        # Run the system
        orchestrator.run(
            num_sentences=args.sentences,
            round_trip=args.round_trip,
            topic=args.topic
        )

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)

    except ValueError as e:
        print(f"\nConfiguration Error: {e}", file=sys.stderr)
        sys.exit(1)

    except RuntimeError as e:
        print(f"\nRuntime Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"\nUnexpected Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
