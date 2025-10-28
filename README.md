# Multi-Agent Translation System

A sophisticated multi-agent LLM system that performs round-trip translation quality testing between Hebrew, English, and French using Claude Sonnet.

## Architecture

The system uses 4 specialized agents:

1. **Agent 1** (Hebrew → English): Translates Hebrew to English
2. **Agent 2** (English → French): Translates English to French
3. **Agent 3** (French → Hebrew): Translates French to Hebrew
4. **Orchestrator**: Coordinates workflow and performs quality analysis

### Translation Pipeline

```
Hebrew (original) → Agent 1 → English → Agent 2 → French → Agent 3 → Hebrew (final)
                                                                            ↓
                                                                     Quality Analysis
                                                                     (Cosine Distance)
```

## Features

- Generate 10-100 meaningful Hebrew sentences (max 30 words each)
- Round-trip translation through 3 languages
- Quality analysis using vector embeddings and cosine distance
- Separate output files for each language stage
- Visualization graphs showing translation quality
- Comprehensive metrics and statistics

## Installation

### 1. Clone or Download

Navigate to the project directory:
```bash
cd /mnt/c/courseAI/lesson14
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Key

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

   Get your API key from: https://console.anthropic.com/

## Usage

### Basic Usage

Generate 20 sentences with round-trip analysis (default):
```bash
python main.py --sentences 20
```

### Custom Number of Sentences

```bash
python main.py --sentences 50
```

or shorthand:
```bash
python main.py -n 50
```

### Without Round-Trip Analysis

Skip quality analysis (faster):
```bash
python main.py --sentences 30 --no-round-trip
```

### With Topic Focus

Generate sentences on a specific topic:
```bash
python main.py --sentences 25 --topic "science and technology"
```

### Help

View all options:
```bash
python main.py --help
```

## Output Files

All files are saved in the `output/` directory:

1. **sentences_hebrew_original.txt** - Original Hebrew sentences
2. **sentences_english.txt** - English translations (after Agent 1)
3. **sentences_french.txt** - French translations (after Agent 2)
4. **sentences_hebrew_final.txt** - Final Hebrew translations (after Agent 3)
5. **quality_metrics.json** - Statistical analysis (if round-trip enabled)
6. **translation_quality_graph.png** - Visualization graph (if round-trip enabled)

### File Format

Each sentence file uses UTF-8 encoding with numbered lines:
```
[1] First sentence here
[2] Second sentence here
[3] Third sentence here
...
```

## Quality Metrics

When round-trip analysis is enabled, the system calculates:

- **Cosine Distance**: Measures similarity between original and final Hebrew sentences
  - Range: 0 to 1 (lower = better quality)
  - 0.0 = identical, 1.0 = completely different
- **Mean Distance**: Average quality across all sentences
- **Standard Deviation**: Consistency of translation quality
- **Min/Max Distance**: Best and worst translations

### Visualization

The quality graph shows:
- **Blue line**: Individual sentence distances
- **Red dashed line**: Mean distance across all sentences
- **X-axis**: Sentence number
- **Y-axis**: Cosine distance

## Project Structure

```
lesson14/
├── main.py                              # Entry point
├── orchestrator.py                      # Orchestrator agent
├── agents.py                            # Translation agents
├── config.py                            # Configuration
├── utils.py                             # Utilities (vectorization, visualization)
├── requirements.txt                     # Python dependencies
├── .env                                 # API key (create from .env.example)
├── .env.example                         # Example environment file
├── .gitignore                           # Git ignore rules
├── README.md                            # This file
├── System_PRD.md                        # Product requirements document
├── orchestrator_prompt.md               # Orchestrator system prompt
├── agent1_hebrew_to_english_prompt.md   # Agent 1 prompt
├── agent2_english_to_french_prompt.md   # Agent 2 prompt
├── agent3_french_to_hebrew_prompt.md    # Agent 3 prompt
├── venv/                                # Virtual environment (created)
└── output/                              # Output files (created)
```

## Requirements

- Python 3.8+
- Anthropic API key
- Internet connection (for Claude API and downloading embedding models)
- ~500MB disk space (for embedding models)

## Dependencies

- **anthropic**: Claude API client
- **sentence-transformers**: Multilingual embeddings
- **scikit-learn**: Cosine similarity calculations
- **matplotlib**: Graph visualization
- **numpy**: Numerical operations
- **python-dotenv**: Environment variable management
- **tqdm**: Progress bars

## Technical Details

### Embedding Model

Uses `paraphrase-multilingual-mpnet-base-v2` for vectorization:
- Supports Hebrew, English, and French
- Generates 768-dimensional embeddings
- First run downloads ~420MB model

### API Usage

Each sentence requires 3 API calls (one per agent). For example:
- 20 sentences = 60 API calls
- 50 sentences = 150 API calls

Orchestrator also makes 1 call for sentence generation.

### Performance

Approximate times (depending on API latency):
- 10 sentences: ~2-3 minutes
- 20 sentences: ~4-6 minutes
- 50 sentences: ~10-15 minutes
- 100 sentences: ~20-30 minutes

## Troubleshooting

### API Key Error
```
ValueError: ANTHROPIC_API_KEY not found
```
**Solution**: Create `.env` file with your API key (see Installation step 5)

### Module Not Found
```
ModuleNotFoundError: No module named 'anthropic'
```
**Solution**: Activate virtual environment and install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Encoding Issues
If you see garbled Hebrew/French text, ensure your terminal supports UTF-8:
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

### Low Confidence Warnings
```
⚠ Low confidence (0.65) on sentence 15
```
This is normal for complex or ambiguous sentences. Check the translation manually.

## Examples

### Example 1: Quick Test (10 sentences)
```bash
python main.py -n 10
```

### Example 2: Production Run (100 sentences)
```bash
python main.py -n 100 --topic "daily life and culture"
```

### Example 3: Fast Translation Only (no analysis)
```bash
python main.py -n 30 --no-round-trip
```

## Documentation

- **System_PRD.md**: Complete product requirements
- **orchestrator_prompt.md**: Orchestrator agent specification
- **agent1_hebrew_to_english_prompt.md**: Agent 1 specification
- **agent2_english_to_french_prompt.md**: Agent 2 specification
- **agent3_french_to_hebrew_prompt.md**: Agent 3 specification

## License

This project is for educational purposes.

## Support

For issues or questions, please refer to the documentation files or check the code comments.

---

**Version**: 1.0
**Last Updated**: 2025-10-28
**Model**: Claude Sonnet 4
