"""
Translation agents implementation.
Each agent is a specialized translator using Claude API.
"""
import json
from typing import Dict, Optional
from pathlib import Path
from anthropic import Anthropic

import config


class TranslationAgent:
    """Base class for translation agents."""

    def __init__(
        self,
        agent_id: str,
        prompt_file: Path,
        source_lang: str,
        target_lang: str
    ):
        """
        Initialize translation agent.

        Args:
            agent_id: Unique identifier for this agent
            prompt_file: Path to the agent's system prompt
            source_lang: Source language code
            target_lang: Target language code
        """
        self.agent_id = agent_id
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

        # Load system prompt
        with open(prompt_file, 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()

    def translate(
        self,
        sentence_id: int,
        text: str,
        timestamp: Optional[str] = None
    ) -> Dict:
        """
        Translate a sentence.

        Args:
            sentence_id: Unique sentence identifier
            text: Text to translate
            timestamp: Optional timestamp

        Returns:
            Dictionary with translation result
        """
        from datetime import datetime

        if timestamp is None:
            timestamp = datetime.now().isoformat()

        # Prepare request
        request = {
            "sentence_id": sentence_id,
            "text": text,
            "source_language": self.source_lang,
            "target_language": self.target_lang,
            "timestamp": timestamp
        }

        # Create user message
        user_message = f"""Please translate the following sentence:

{json.dumps(request, ensure_ascii=False, indent=2)}

Respond with ONLY a valid JSON object in the format specified in your system prompt. Do not include any other text or explanation."""

        # Call Claude API
        try:
            response = self.client.messages.create(
                model=config.MODEL_NAME,
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            # Extract response text
            response_text = response.content[0].text.strip()

            # Parse JSON response
            # Sometimes Claude wraps JSON in markdown code blocks, handle that
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

            result = json.loads(response_text)
            return result

        except Exception as e:
            # Return error response
            return {
                "sentence_id": sentence_id,
                "translation": "",
                "confidence": 0.0,
                "agent_id": self.agent_id,
                "notes": f"ERROR: {str(e)}"
            }

    def batch_translate(self, sentences: list[str]) -> list[str]:
        """
        Translate a batch of sentences.

        Args:
            sentences: List of sentences to translate

        Returns:
            List of translated sentences
        """
        translations = []
        from tqdm import tqdm

        print(f"\n{self.agent_id} processing {len(sentences)} sentences...")

        for i, sentence in enumerate(tqdm(sentences, desc=f"{self.agent_id}")):
            result = self.translate(sentence_id=i+1, text=sentence)
            translation = result.get("translation", "")
            translations.append(translation)

            # Log low confidence translations
            confidence = result.get("confidence", 0.0)
            if confidence < 0.7:
                print(f"  ⚠ Low confidence ({confidence:.2f}) on sentence {i+1}")

        return translations


class Agent1HebrewToEnglish(TranslationAgent):
    """Agent 1: Hebrew to English translator."""

    def __init__(self):
        super().__init__(
            agent_id="agent1_hebrew_to_english",
            prompt_file=config.AGENT1_PROMPT_FILE,
            source_lang="he",
            target_lang="en"
        )


class Agent2EnglishToFrench(TranslationAgent):
    """Agent 2: English to French translator."""

    def __init__(self):
        super().__init__(
            agent_id="agent2_english_to_french",
            prompt_file=config.AGENT2_PROMPT_FILE,
            source_lang="en",
            target_lang="fr"
        )


class Agent3FrenchToHebrew(TranslationAgent):
    """Agent 3: French to Hebrew translator."""

    def __init__(self):
        super().__init__(
            agent_id="agent3_french_to_hebrew",
            prompt_file=config.AGENT3_PROMPT_FILE,
            source_lang="fr",
            target_lang="he"
        )
