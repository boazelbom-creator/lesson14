"""
Configuration settings for the multi-agent translation system.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")

# Validate API key
if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY not found. Please create a .env file with your API key. "
        "See .env.example for reference."
    )

# Directory Configuration
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "output"))
OUTPUT_DIR.mkdir(exist_ok=True)

# Prompt Files
PROMPTS_DIR = BASE_DIR
ORCHESTRATOR_PROMPT_FILE = PROMPTS_DIR / "orchestrator_prompt.md"
AGENT1_PROMPT_FILE = PROMPTS_DIR / "agent1_hebrew_to_english_prompt.md"
AGENT2_PROMPT_FILE = PROMPTS_DIR / "agent2_english_to_french_prompt.md"
AGENT3_PROMPT_FILE = PROMPTS_DIR / "agent3_french_to_hebrew_prompt.md"

# Translation Configuration
MAX_SENTENCE_WORDS = 30
MIN_SENTENCES = 10
MAX_SENTENCES = 100

# Embedding Configuration
EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2"

# Graph Configuration
GRAPH_DPI = 300
GRAPH_FIGSIZE = (12, 6)

# File Configuration
FILE_ENCODING = "utf-8"

# Output Files
SENTENCES_HEBREW_ORIGINAL = OUTPUT_DIR / "sentences_hebrew_original.txt"
SENTENCES_ENGLISH = OUTPUT_DIR / "sentences_english.txt"
SENTENCES_FRENCH = OUTPUT_DIR / "sentences_french.txt"
SENTENCES_HEBREW_FINAL = OUTPUT_DIR / "sentences_hebrew_final.txt"
QUALITY_METRICS_FILE = OUTPUT_DIR / "quality_metrics.json"
QUALITY_GRAPH_FILE = OUTPUT_DIR / "translation_quality_graph.png"

# API Configuration
API_TIMEOUT = 30
MAX_RETRIES = 3
MAX_TOKENS = 4096
TEMPERATURE = 0.3  # Lower temperature for more consistent translations
