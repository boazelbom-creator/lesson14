"""
Utility functions for vectorization, file I/O, and visualization.
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
from datetime import datetime

import config


class EmbeddingEngine:
    """Handles text vectorization using sentence transformers."""

    def __init__(self, model_name: str = config.EMBEDDING_MODEL):
        """Initialize the embedding model."""
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Embedding model loaded successfully.")

    def encode(self, sentences: List[str]) -> np.ndarray:
        """
        Encode sentences into vectors.

        Args:
            sentences: List of sentences to encode

        Returns:
            Numpy array of embeddings
        """
        return self.model.encode(sentences, show_progress_bar=True)

    def calculate_cosine_distances(
        self,
        original_embeddings: np.ndarray,
        final_embeddings: np.ndarray
    ) -> List[float]:
        """
        Calculate cosine distance between original and final embeddings.

        Args:
            original_embeddings: Embeddings of original sentences
            final_embeddings: Embeddings of final sentences

        Returns:
            List of cosine distances (1 - cosine_similarity)
        """
        distances = []
        for i in range(len(original_embeddings)):
            similarity = cosine_similarity(
                [original_embeddings[i]],
                [final_embeddings[i]]
            )[0][0]
            distance = 1 - similarity
            distances.append(float(distance))
        return distances


class FileManager:
    """Handles file I/O operations."""

    @staticmethod
    def save_sentences(
        sentences: List[str],
        filepath: Path,
        numbered: bool = True
    ) -> None:
        """
        Save sentences to a file.

        Args:
            sentences: List of sentences to save
            filepath: Path to output file
            numbered: Whether to prefix with sentence numbers
        """
        with open(filepath, 'w', encoding=config.FILE_ENCODING) as f:
            for i, sentence in enumerate(sentences, 1):
                if numbered:
                    f.write(f"[{i}] {sentence}\n")
                else:
                    f.write(f"{sentence}\n")

        file_size = filepath.stat().st_size / 1024  # KB
        print(f"[✓] Saved: {filepath.name} ({len(sentences)} sentences, {file_size:.1f} KB)")

    @staticmethod
    def load_sentences(filepath: Path) -> List[str]:
        """
        Load sentences from a file.

        Args:
            filepath: Path to input file

        Returns:
            List of sentences (without numbering)
        """
        sentences = []
        with open(filepath, 'r', encoding=config.FILE_ENCODING) as f:
            for line in f:
                # Remove numbering if present: [N] sentence
                line = line.strip()
                if line.startswith('['):
                    # Extract sentence after "] "
                    parts = line.split('] ', 1)
                    if len(parts) == 2:
                        sentences.append(parts[1])
                    else:
                        sentences.append(line)
                else:
                    sentences.append(line)
        return sentences

    @staticmethod
    def save_metrics(
        metrics: Dict,
        filepath: Path = config.QUALITY_METRICS_FILE
    ) -> None:
        """
        Save quality metrics to JSON file.

        Args:
            metrics: Dictionary containing metrics
            filepath: Path to output JSON file
        """
        with open(filepath, 'w', encoding=config.FILE_ENCODING) as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)

        file_size = filepath.stat().st_size / 1024  # KB
        print(f"[✓] Saved: {filepath.name} ({file_size:.1f} KB)")


class Visualizer:
    """Handles graph generation and visualization."""

    @staticmethod
    def plot_quality_graph(
        distances: List[float],
        mean_distance: float,
        output_path: Path = config.QUALITY_GRAPH_FILE
    ) -> None:
        """
        Create and save quality analysis graph.

        Args:
            distances: List of cosine distances
            mean_distance: Mean distance value
            output_path: Path to save the graph
        """
        plt.figure(figsize=config.GRAPH_FIGSIZE)

        # Plot individual distances
        sentence_numbers = list(range(1, len(distances) + 1))
        plt.plot(
            sentence_numbers,
            distances,
            marker='o',
            linestyle='-',
            linewidth=2,
            markersize=6,
            color='#2E86AB',
            label='Cosine Distance'
        )

        # Plot mean line
        plt.axhline(
            y=mean_distance,
            color='#E63946',
            linestyle='--',
            linewidth=2.5,
            label=f'Mean Distance ({mean_distance:.4f})'
        )

        # Styling
        plt.xlabel('Sentence Number', fontsize=12, fontweight='bold')
        plt.ylabel('Cosine Distance', fontsize=12, fontweight='bold')
        plt.title(
            'Round-Trip Translation Quality Analysis\n(Hebrew → English → French → Hebrew)',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        plt.legend(loc='best', fontsize=10, framealpha=0.9)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()

        # Save
        plt.savefig(output_path, dpi=config.GRAPH_DPI, bbox_inches='tight')
        print(f"[✓] Saved: {output_path.name} ({output_path.stat().st_size / 1024:.0f} KB)")

        # Close to free memory
        plt.close()


class StatsCalculator:
    """Statistical analysis utilities."""

    @staticmethod
    def calculate_statistics(distances: List[float]) -> Dict:
        """
        Calculate statistical metrics for distances.

        Args:
            distances: List of cosine distances

        Returns:
            Dictionary with statistical metrics
        """
        distances_array = np.array(distances)

        return {
            "num_sentences": len(distances),
            "mean_distance": float(np.mean(distances_array)),
            "std_distance": float(np.std(distances_array)),
            "min_distance": float(np.min(distances_array)),
            "max_distance": float(np.max(distances_array)),
            "median_distance": float(np.median(distances_array)),
            "distances": distances,
            "timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def print_statistics(stats: Dict) -> None:
        """
        Print statistics in a formatted way.

        Args:
            stats: Statistics dictionary
        """
        print("\n" + "="*60)
        print("QUALITY METRICS SUMMARY")
        print("="*60)
        print(f"Total Sentences:     {stats['num_sentences']}")
        print(f"Mean Distance:       {stats['mean_distance']:.4f}")
        print(f"Std Deviation:       {stats['std_distance']:.4f}")
        print(f"Min Distance:        {stats['min_distance']:.4f}")
        print(f"Max Distance:        {stats['max_distance']:.4f}")
        print(f"Median Distance:     {stats['median_distance']:.4f}")
        print("="*60)


def print_translation_journey(
    hebrew_original: List[str],
    english: List[str],
    french: List[str],
    hebrew_final: List[str],
    distances: List[float] = None,
    max_display: int = 5
) -> None:
    """
    Print translation journey for sentences.

    Args:
        hebrew_original: Original Hebrew sentences
        english: English translations
        french: French translations
        hebrew_final: Final Hebrew translations
        distances: Optional cosine distances
        max_display: Maximum number of sentences to display
    """
    print("\n" + "="*60)
    print("TRANSLATION JOURNEY RESULTS")
    print("="*60 + "\n")

    num_to_display = min(max_display, len(hebrew_original))

    for i in range(num_to_display):
        print(f"Sentence {i+1}:")
        print(f"  Original (HE):  {hebrew_original[i]}")
        print(f"  English (EN):   {english[i]}")
        print(f"  French (FR):    {french[i]}")
        print(f"  Final (HE):     {hebrew_final[i]}")
        if distances:
            print(f"  Distance:       {distances[i]:.4f}")
        print()

    if len(hebrew_original) > max_display:
        print(f"... and {len(hebrew_original) - max_display} more sentences\n")

    print("="*60)


def print_file_summary() -> None:
    """Print summary of generated files."""
    print("\n" + "="*60)
    print("FILES GENERATED")
    print("="*60)

    files = [
        config.SENTENCES_HEBREW_ORIGINAL,
        config.SENTENCES_ENGLISH,
        config.SENTENCES_FRENCH,
        config.SENTENCES_HEBREW_FINAL,
        config.QUALITY_METRICS_FILE,
        config.QUALITY_GRAPH_FILE
    ]

    for filepath in files:
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print(f"✓ {filepath.name}")

    print("="*60 + "\n")
