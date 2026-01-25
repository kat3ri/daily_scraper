"""LLM analyzer using Ollama for content analysis."""
import logging
import json
from typing import List, Dict, Optional
import ollama
from .prompts import (
    ANALYSIS_SYSTEM_PROMPT,
    CONTENT_ANALYSIS_PROMPT,
    BATCH_ANALYSIS_PROMPT,
    DIGEST_SUMMARY_PROMPT
)

logger = logging.getLogger(__name__)


class LLMAnalyzer:
    """Analyzer using local LLM via Ollama."""
    
    def __init__(self, host: str = "http://localhost:11434", 
                 model: str = "mistral:7b"):
        """
        Initialize LLM analyzer.
        
        Args:
            host: Ollama server host
            model: Model to use for analysis
        """
        self.host = host
        self.model = model
        self.client = None
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test connection to Ollama."""
        try:
            # Try to list models to verify connection
            client = ollama.Client(host=self.host)
            client.list()
            logger.info(f"Successfully connected to Ollama at {self.host}")
            logger.info(f"Using model: {self.model}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            logger.error(f"Make sure Ollama is running at {self.host}")
            logger.error(f"Install: https://ollama.ai")
            logger.error(f"Run: ollama pull {self.model}")
            return False
    
    def analyze_items(self, items: List[Dict], temperature: float = 0.3,
                     max_tokens: int = 500) -> List[Dict]:
        """
        Analyze a list of items for novelty and significance.
        
        Args:
            items: List of content items to analyze
            temperature: LLM temperature parameter
            max_tokens: Maximum tokens for response
            
        Returns:
            List of items with analysis added
        """
        analyzed_items = []
        
        for idx, item in enumerate(items):
            try:
                analysis = self._analyze_single_item(
                    item, temperature, max_tokens
                )
                
                if analysis:
                    item['llm_analysis'] = analysis
                    item['llm_score'] = analysis.get('score', 0)
                    analyzed_items.append(item)
                    
                    if (idx + 1) % 10 == 0:
                        logger.info(f"Analyzed {idx + 1}/{len(items)} items")
                        
            except Exception as e:
                logger.error(f"Error analyzing item {idx}: {e}")
                # Still include item without analysis
                item['llm_score'] = 0
                analyzed_items.append(item)
                continue
        
        logger.info(f"Completed analysis of {len(analyzed_items)} items")
        return analyzed_items
    
    def _analyze_single_item(self, item: Dict, temperature: float,
                            max_tokens: int) -> Optional[Dict]:
        """Analyze a single item."""
        # Prepare content for analysis
        title = item.get('title', '')
        source = item.get('source', '')
        description = item.get('description', item.get('selftext', ''))
        
        # Limit description length
        if len(description) > 500:
            description = description[:500] + '...'
        
        # Create prompt
        prompt = CONTENT_ANALYSIS_PROMPT.format(
            title=title,
            source=source,
            description=description
        )
        
        try:
            client = ollama.Client(host=self.host)
            response = client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': ANALYSIS_SYSTEM_PROMPT
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': temperature,
                    'num_predict': max_tokens
                }
            )
            
            # Parse JSON response
            content = response['message']['content']
            
            # Try to extract JSON from response
            analysis = self._extract_json(content)
            return analysis
            
        except Exception as e:
            logger.debug(f"Error in LLM analysis: {e}")
            return None
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from LLM response."""
        # Try direct JSON parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in code blocks
        if '```json' in text:
            try:
                json_text = text.split('```json')[1].split('```')[0].strip()
                return json.loads(json_text)
            except (IndexError, json.JSONDecodeError):
                pass
        
        # Try to find JSON between braces
        try:
            start = text.index('{')
            end = text.rindex('}') + 1
            json_text = text[start:end]
            return json.loads(json_text)
        except (ValueError, json.JSONDecodeError):
            pass
        
        logger.debug(f"Could not extract JSON from response: {text[:100]}")
        return None
    
    def generate_digest_summary(self, top_items: List[Dict]) -> str:
        """
        Generate an introductory summary for the digest.
        
        Args:
            top_items: Top-ranked items for the digest
            
        Returns:
            Summary text
        """
        # Create a brief overview of top items
        items_text = "\n".join([
            f"- {item.get('title', 'Untitled')} (score: {item.get('llm_score', 0)})"
            for item in top_items[:5]
        ])
        
        prompt = DIGEST_SUMMARY_PROMPT.format(top_items=items_text)
        
        try:
            client = ollama.Client(host=self.host)
            response = client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': ANALYSIS_SYSTEM_PROMPT
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.7,
                    'num_predict': 200
                }
            )
            
            summary = response['message']['content'].strip()
            return summary
            
        except Exception as e:
            logger.error(f"Error generating digest summary: {e}")
            return "Here are today's most interesting AI developments:"
    
    def rank_and_filter(self, items: List[Dict], top_n: int = 15,
                       min_score: int = 5) -> List[Dict]:
        """
        Rank items by LLM score and filter to top N.
        
        Args:
            items: Items with LLM analysis
            top_n: Number of top items to return
            min_score: Minimum score threshold
            
        Returns:
            Filtered and sorted list of top items
        """
        # Filter by minimum score
        filtered = [item for item in items if item.get('llm_score', 0) >= min_score]
        
        # Sort by score (descending)
        sorted_items = sorted(
            filtered,
            key=lambda x: x.get('llm_score', 0),
            reverse=True
        )
        
        # Return top N
        top_items = sorted_items[:top_n]
        
        logger.info(f"Selected {len(top_items)} top items (min_score={min_score})")
        return top_items
