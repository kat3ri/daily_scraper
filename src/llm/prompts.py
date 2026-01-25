"""Prompt templates for LLM analysis."""

ANALYSIS_SYSTEM_PROMPT = """You are an AI research analyst specializing in identifying novel and significant developments in artificial intelligence and machine learning. Your expertise includes:

- New model architectures and techniques
- Significant benchmark improvements
- Novel applications of AI/ML
- Research breakthroughs and papers
- Important tools and libraries
- Notable community discussions

Analyze content objectively and focus on technical merit and innovation."""


CONTENT_ANALYSIS_PROMPT = """Analyze the following AI/ML content and evaluate its novelty and significance.

Title: {title}
Source: {source}
Description: {description}

Provide your analysis in the following JSON format:
{{
    "score": <1-10 integer representing importance/interest>,
    "summary": "<2-3 sentence summary focusing on what's novel or significant>",
    "category": "<one of: model, paper, tool, technique, application, discussion>",
    "novelty_reason": "<brief explanation of why this is interesting>"
}}

Focus on:
- Technical novelty and innovation
- Practical applicability
- Potential impact on the field
- Quality of execution

Score guidelines:
- 9-10: Groundbreaking, paradigm-shifting developments
- 7-8: Highly significant with clear innovation
- 5-6: Moderately interesting, incremental improvements
- 3-4: Minor developments or niche applications
- 1-2: Low interest or derivative work

Be selective and honest in your scoring. Most content should score 3-6."""


BATCH_ANALYSIS_PROMPT = """You are analyzing multiple AI/ML items. For each item below, provide a score (1-10) and brief assessment.

Items to analyze:
{items}

For each item, respond with JSON in this format:
[
    {{
        "id": <item number>,
        "score": <1-10>,
        "summary": "<2-3 sentence summary>",
        "category": "<model|paper|tool|technique|application|discussion>",
        "novelty_reason": "<why it's interesting>"
    }}
]

Be selective - most items should score 3-6. Only truly exceptional items should score 8+."""


DIGEST_SUMMARY_PROMPT = """Create a brief introduction for today's AI digest email based on these top items:

{top_items}

Write 2-3 sentences highlighting the main themes and most exciting developments from today. Be enthusiastic but professional."""
