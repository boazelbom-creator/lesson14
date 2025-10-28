"""
Orchestrator Agent - Coordinates the multi-agent translation system.
"""
import json
from typing import List, Optional
from pathlib import Path
from anthropic import Anthropic

import config
from agents import Agent1HebrewToEnglish, Agent2EnglishToFrench, Agent3FrenchToHebrew
from utils import (
    EmbeddingEngine,
    FileManager,
    Visualizer,
    StatsCalculator,
    print_translation_journey,
    print_file_summary
)


class OrchestratorAgent:
    """Orchestrator agent that coordinates the translation workflow."""

    def __init__(self):
        """Initialize orchestrator and translation agents."""
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

        # Load orchestrator prompt
        with open(config.ORCHESTRATOR_PROMPT_FILE, 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()

        # Initialize translation agents
        print("Initializing translation agents...")
        self.agent1 = Agent1HebrewToEnglish()
        self.agent2 = Agent2EnglishToFrench()
        self.agent3 = Agent3FrenchToHebrew()
        print("All agents initialized.\n")

        # Initialize utilities
        self.file_manager = FileManager()
        self.visualizer = Visualizer()
        self.stats_calculator = StatsCalculator()
        self.embedding_engine = None  # Lazy load when needed

    def generate_hebrew_sentences(
        self,
        num_sentences: int,
        topic: Optional[str] = None
    ) -> List[str]:
        """
        Generate meaningful Hebrew sentences.

        Args:
            num_sentences: Number of sentences to generate
            topic: Optional topic/domain for sentences

        Returns:
            List of Hebrew sentences
        """
        print(f"\nGenerating {num_sentences} Hebrew sentences...")

        # Validate input
        if num_sentences < config.MIN_SENTENCES or num_sentences > config.MAX_SENTENCES:
            raise ValueError(
                f"Number of sentences must be between {config.MIN_SENTENCES} "
                f"and {config.MAX_SENTENCES}"
            )

        # Prepare prompt
        user_message = f"""Generate exactly {num_sentences} meaningful Hebrew sentences.

Requirements:
- Each sentence must be maximum {config.MAX_SENTENCE_WORDS} words
- Sentences must be grammatically correct and contextually meaningful
- Vary the sentence structures and topics
- Use modern Hebrew (עברית מודרנית)
{'- Focus on topic: ' + topic if topic else '- Cover diverse topics (technology, nature, daily life, science, culture)'}

Respond with ONLY a JSON array of sentences, like this:
["משפט ראשון", "משפט שני", "משפט שלישי", ...]

Do not include any other text or explanation."""

        try:
            response = self.client.messages.create(
                model=config.MODEL_NAME,
                max_tokens=config.MAX_TOKENS,
                temperature=0.7,  # Higher temperature for creative sentence generation
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            # Extract response
            response_text = response.content[0].text.strip()

            # Parse JSON
            if response_text.startswith("```"):
                # Extract JSON from code block
                lines = response_text.split('\n')
                json_lines = []
                in_json = False
                for line in lines:
                    if line.strip().startswith("```"):
                        if in_json:
                            break
                        else:
                            in_json = True
                            continue
                    if in_json:
                        json_lines.append(line)
                response_text = '\n'.join(json_lines)

            sentences = json.loads(response_text)

            # Validate
            if not isinstance(sentences, list):
                raise ValueError("Response is not a list")

            if len(sentences) != num_sentences:
                print(f"  ⚠ Generated {len(sentences)} sentences instead of {num_sentences}")

            print(f"✓ Generated {len(sentences)} Hebrew sentences")

            return sentences

        except Exception as e:
            raise RuntimeError(f"Failed to generate sentences: {str(e)}")

    def run_translation_pipeline(
        self,
        hebrew_original: List[str]
    ) -> tuple[List[str], List[str], List[str]]:
        """
        Run the translation pipeline through all 3 agents.

        Args:
            hebrew_original: Original Hebrew sentences

        Returns:
            Tuple of (english, french, hebrew_final) translations
        """
        print("\n" + "="*60)
        print("STARTING TRANSLATION PIPELINE")
        print("="*60)

        # Agent 1: Hebrew → English
        english = self.agent1.batch_translate(hebrew_original)
        self.file_manager.save_sentences(english, config.SENTENCES_ENGLISH)

        # Agent 2: English → French
        french = self.agent2.batch_translate(english)
        self.file_manager.save_sentences(french, config.SENTENCES_FRENCH)

        # Agent 3: French → Hebrew
        hebrew_final = self.agent3.batch_translate(french)
        self.file_manager.save_sentences(hebrew_final, config.SENTENCES_HEBREW_FINAL)

        print("\n✓ Translation pipeline completed")

        return english, french, hebrew_final

    def analyze_quality(
        self,
        hebrew_original: List[str],
        hebrew_final: List[str]
    ) -> dict:
        """
        Analyze translation quality using cosine distance.

        Args:
            hebrew_original: Original Hebrew sentences
            hebrew_final: Final Hebrew sentences after round-trip

        Returns:
            Dictionary with quality metrics
        """
        print("\n" + "="*60)
        print("STARTING QUALITY ANALYSIS")
        print("="*60)

        # Lazy load embedding engine
        if self.embedding_engine is None:
            self.embedding_engine = EmbeddingEngine()

        # Vectorize sentences
        print("\nVectorizing original Hebrew sentences...")
        original_embeddings = self.embedding_engine.encode(hebrew_original)

        print("Vectorizing final Hebrew sentences...")
        final_embeddings = self.embedding_engine.encode(hebrew_final)

        # Calculate cosine distances
        print("\nCalculating cosine distances...")
        distances = self.embedding_engine.calculate_cosine_distances(
            original_embeddings,
            final_embeddings
        )

        # Calculate statistics
        stats = self.stats_calculator.calculate_statistics(distances)

        # Save metrics
        self.file_manager.save_metrics(stats)

        # Generate graph
        print("\nGenerating quality graph...")
        self.visualizer.plot_quality_graph(
            distances,
            stats['mean_distance']
        )

        print("\n✓ Quality analysis completed")

        return stats

    def run(
        self,
        num_sentences: int,
        round_trip: bool = True,
        topic: Optional[str] = None
    ) -> None:
        """
        Main orchestration method.

        Args:
            num_sentences: Number of sentences to generate
            round_trip: Whether to perform round-trip quality analysis
            topic: Optional topic for sentence generation
        """
        print("\n" + "="*60)
        print("MULTI-AGENT TRANSLATION SYSTEM")
        print("="*60)
        print(f"Configuration:")
        print(f"  - Sentences: {num_sentences}")
        print(f"  - Round-trip analysis: {round_trip}")
        print(f"  - Topic: {topic if topic else 'Mixed'}")
        print(f"  - Model: {config.MODEL_NAME}")
        print("="*60)

        # Step 1: Generate Hebrew sentences
        hebrew_original = self.generate_hebrew_sentences(num_sentences, topic)
        self.file_manager.save_sentences(hebrew_original, config.SENTENCES_HEBREW_ORIGINAL)

        # Step 2: Run translation pipeline
        english, french, hebrew_final = self.run_translation_pipeline(hebrew_original)

        # Step 3: Quality analysis (if enabled)
        stats = None
        if round_trip:
            stats = self.analyze_quality(hebrew_original, hebrew_final)

        # Step 4: Present results
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)

        # Print sample translations
        print_translation_journey(
            hebrew_original,
            english,
            french,
            hebrew_final,
            stats['distances'] if stats else None,
            max_display=5
        )

        # Print statistics
        if stats:
            self.stats_calculator.print_statistics(stats)

        # Print file summary
        print_file_summary()

        # Final message
        print("\n" + "="*60)
        print("SYSTEM COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"\nAll output files are saved in: {config.OUTPUT_DIR}")
        print("\nFiles generated:")
        print(f"  1. {config.SENTENCES_HEBREW_ORIGINAL.name} - Original Hebrew")
        print(f"  2. {config.SENTENCES_ENGLISH.name} - English translations")
        print(f"  3. {config.SENTENCES_FRENCH.name} - French translations")
        print(f"  4. {config.SENTENCES_HEBREW_FINAL.name} - Final Hebrew (round-trip)")
        if round_trip:
            print(f"  5. {config.QUALITY_METRICS_FILE.name} - Quality metrics (JSON)")
            print(f"  6. {config.QUALITY_GRAPH_FILE.name} - Quality visualization (PNG)")
        print("="*60 + "\n")
