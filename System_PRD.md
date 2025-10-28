# Multi-Agent Translation System - Product Requirements Document

## 1. Overview

### 1.1 Purpose
Build a multi-agent LLM-based translation system that performs round-trip translation quality testing between Hebrew, English, and French with quantitative similarity analysis.

### 1.2 System Architecture
- **4 Agents Total**: 3 specialized translation agents + 1 orchestrator agent
- **Technology Stack**:
  - LLM: Anthropic Claude (Sonnet model)
  - Programming Language: Python
  - Vectorization: Sentence embeddings
  - Visualization: matplotlib
  - Distance Metric: Cosine distance

---

## 2. Agent Specifications

### 2.1 Agent 1: Hebrew to English Translator
- **Input**: Hebrew text
- **Output**: English translation
- **Model**: Claude Sonnet
- **Specialization**: Hebrew → English translation

### 2.2 Agent 2: English to French Translator
- **Input**: English text
- **Output**: French translation
- **Model**: Claude Sonnet
- **Specialization**: English → French translation

### 2.3 Agent 3: French to Hebrew Translator
- **Input**: French text
- **Output**: Hebrew translation
- **Model**: Claude Sonnet
- **Specialization**: French → Hebrew translation

### 2.4 Agent 4: Orchestrator (Coordinator)
- **Role**: System controller and quality analyzer
- **Model**: Claude Sonnet
- **Responsibilities**: See Section 3

---

## 3. Orchestrator Responsibilities

### 3.1 Sentence Generation
- Generate N meaningful sentences (N ∈ [10, 100], user-specified)
- Each sentence: maximum 30 words
- Sentences must be contextually meaningful and grammatically correct
- Language: Hebrew (starting language)

### 3.2 Translation Pipeline Execution
- Execute agents in sequence: **Agent 1 → Agent 2 → Agent 3**
- Track intermediate results at each stage:
  1. Original sentence (Hebrew)
  2. After Agent 1 (English)
  3. After Agent 2 (French)
  4. After Agent 3 (Hebrew - round-trip complete)

### 3.3 File Output Requirements
Export sentences to separate files for each language:

#### 3.3.1 Output Files
1. **sentences_hebrew_original.txt** - Original Hebrew sentences
2. **sentences_english.txt** - English translations (after Agent 1)
3. **sentences_french.txt** - French translations (after Agent 2)
4. **sentences_hebrew_final.txt** - Final Hebrew translations (after Agent 3, round-trip)

#### 3.3.2 File Format
- **Encoding**: UTF-8 (to support Hebrew, French characters)
- **Format**: One sentence per line
- **Line numbering**: Optional, prefixed format `[N] sentence text`
- **Location**: Configurable output directory

#### 3.3.3 File Structure Example
```
sentences_hebrew_original.txt:
[1] משפט ראשון בעברית
[2] משפט שני בעברית
...

sentences_english.txt:
[1] First sentence in English
[2] Second sentence in English
...

sentences_french.txt:
[1] Première phrase en français
[2] Deuxième phrase en français
...

sentences_hebrew_final.txt:
[1] משפט ראשון בעברית (after round-trip)
[2] משפט שני בעברית (after round-trip)
...
```

### 3.4 Round-Trip Quality Analysis
When round-trip translation is requested:

#### 3.4.1 Vectorization Process
- Tokenize original Hebrew sentences
- Tokenize final Hebrew sentences (after round-trip)
- Convert tokens to vector embeddings
- Use appropriate embedding model compatible with Hebrew text

#### 3.4.2 Similarity Calculation
- Calculate cosine distance for each sentence pair:
  - `distance = 1 - cosine_similarity(original_vector, final_vector)`
- Store distance for each of N sentences

#### 3.4.3 Statistical Analysis
- Calculate mean distance across all sentences:
  - `mean_distance = sum(distances) / N`

### 3.5 Visualization Requirements
Generate a graph with the following specifications:

**Graph Components**:
- **X-axis**: Sentence number (1 to N)
- **Y-axis**: Cosine distance (0 to 2, typical range 0 to 1)
- **Data points**: Individual sentence distances (scatter/line plot)
- **Mean line**: Horizontal line showing mean distance across all sentences
- **Title**: "Round-Trip Translation Quality Analysis"
- **Labels**: Clear axis labels and legend
- **Grid**: Optional grid for readability

**Graph Format**:
- Save as PNG: `translation_quality_graph.png`
- Display inline if in notebook environment
- Resolution: 300 DPI minimum

### 3.6 Results Presentation
Present comprehensive results including:

1. **Translation Journey Table** (Console/Display):
   ```
   Sentence # | Original (Hebrew) | English | French | Final (Hebrew)
   -----------|-------------------|---------|--------|----------------
   1          | [text]            | [text]  | [text] | [text]
   2          | [text]            | [text]  | [text] | [text]
   ...        | ...               | ...     | ...    | ...
   ```

2. **Quality Metrics**:
   - Individual cosine distances per sentence
   - Mean cosine distance
   - Standard deviation (optional)
   - Min/Max distances
   - Export to: `quality_metrics.json`

3. **Visualization**:
   - Quality graph as specified in 3.5

---

## 4. Functional Requirements

### 4.1 User Inputs
- **Required**:
  - Number of sentences (10-100)
  - Round-trip mode toggle (yes/no)

- **Optional**:
  - Sentence topic/domain
  - Complexity level
  - Output directory path

### 4.2 System Outputs

#### 4.2.1 Files Generated
- `sentences_hebrew_original.txt` - Original sentences
- `sentences_english.txt` - English translations
- `sentences_french.txt` - French translations
- `sentences_hebrew_final.txt` - Final Hebrew (round-trip)
- `translation_quality_graph.png` - Quality visualization (if round-trip)
- `quality_metrics.json` - Detailed metrics (if round-trip)

#### 4.2.2 Console Outputs
- Translation results at each stage
- Quality metrics summary
- File save confirmations

### 4.3 Error Handling
- Handle translation failures gracefully
- Validate sentence length constraints
- Handle unsupported characters
- Manage API rate limits
- Handle file I/O errors (permissions, disk space)

---

## 5. Non-Functional Requirements

### 5.1 Performance
- Process 100 sentences within reasonable time (< 5 minutes)
- Parallel processing where possible
- Efficient token/vector caching

### 5.2 Scalability
- Modular design for adding new language agents
- Configurable number of sentences
- Extensible quality metrics

### 5.3 Maintainability
- Clear separation of concerns
- Individual agent prompts
- Documented code
- Configuration files for settings

### 5.4 Data Integrity
- Ensure UTF-8 encoding for all files
- Atomic file writes (temp file + rename)
- Backup existing files before overwriting

---

## 6. Data Flow Architecture

```
User Request
    ↓
Orchestrator Agent
    ↓
Generate N Hebrew Sentences
    ↓
    Save to: sentences_hebrew_original.txt
    ↓
For each sentence:
    ↓
    Agent 1 (Hebrew → English)
    ↓
    Save to: sentences_english.txt
    ↓
    Agent 2 (English → French)
    ↓
    Save to: sentences_french.txt
    ↓
    Agent 3 (French → Hebrew)
    ↓
    Save to: sentences_hebrew_final.txt
    ↓
Store results

If round-trip requested:
    ↓
    Vectorize original & final sentences
    ↓
    Calculate cosine distances
    ↓
    Generate graph → save as translation_quality_graph.png
    ↓
    Save metrics → quality_metrics.json
    ↓
Present all results
```

---

## 7. Technical Implementation Notes

### 7.1 Embedding Model Selection
- Consider multilingual embedding models (e.g., sentence-transformers multilingual models)
- Must support Hebrew, English, and French
- Recommended: `paraphrase-multilingual-mpnet-base-v2` or Claude embeddings API

### 7.2 Cosine Distance Formula
```python
from sklearn.metrics.pairwise import cosine_similarity
distance = 1 - cosine_similarity(vec1, vec2)
```

### 7.3 Agent Communication
- Use structured JSON for inter-agent communication
- Include metadata (timestamp, agent ID, confidence scores)
- Implement retry logic for failed translations

### 7.4 File I/O Best Practices
```python
# UTF-8 encoding for all files
with open('sentences_hebrew_original.txt', 'w', encoding='utf-8') as f:
    for i, sentence in enumerate(sentences, 1):
        f.write(f"[{i}] {sentence}\n")
```

---

## 8. Success Criteria

### 8.1 Functional Success
- System generates requested number of sentences
- All translations complete successfully
- All 4 language files created with correct content
- Round-trip analysis produces valid metrics
- Graph displays and saves correctly
- All output files are readable and properly encoded

### 8.2 Quality Success
- Generated sentences are meaningful and grammatically correct
- Translations are contextually appropriate
- Cosine distance correlates with translation quality
- System provides actionable insights
- Files contain complete data without corruption

---

## 9. Future Enhancements (Out of Scope for V1)

- Support for additional languages
- Multiple embedding models comparison
- BLEU score integration
- Human evaluation interface
- Batch processing API
- Real-time streaming results
- Translation confidence scores
- Detailed error analysis per sentence
- Excel/CSV export format
- Parallel file writing optimization

---

## 10. Glossary

- **Round-trip translation**: Translating text from source → intermediate languages → back to source
- **Cosine distance**: Measure of dissimilarity between two vectors (1 - cosine similarity)
- **Embedding**: Dense vector representation of text
- **Orchestrator**: Controller agent that manages worker agents
- **Worker agents**: Specialized translation agents (Agents 1-3)
- **UTF-8**: Universal character encoding supporting all languages

---

**Document Version**: 1.0
**Last Updated**: 2025-10-28
**Status**: Draft - Ready for Implementation
