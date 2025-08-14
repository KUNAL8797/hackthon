
# prompt_templates.py
from typing import List, Dict, Any

class GeminiPrompts:
    @staticmethod
    def pre_analysis_prompt(article_text: str) -> str:
        return f"""
You are a master investigative journalist. Before analyzing the following article in detail, 
perform a quick pre-analysis. Read through the text and provide a brief, internal monologue 
(3-4 sentences) outlining your initial impressions.

Focus on:
- The article's apparent purpose (e.g., inform, persuade, entertain).
- Any immediate red flags or signs of quality journalism.
- The key topics or entities that seem most important to scrutinize.

This pre-analysis is for your own internal context and will help guide your detailed analysis later.

Article to pre-analyze:
{article_text}

Your internal monologue:
"""

    @staticmethod
    def claims_extraction_prompt(article_text: str) -> str:
        return f"""
You are an expert investigative journalist analyzing news content for factual claims.

Article to analyze:
{article_text}

Task: Extract and categorize the core factual claims made in this article.

For each claim, provide:
1. The exact claim as stated
2. Classification (Statistical, Causal, Predictive, Historical, etc.)
3. Confidence level of the claim's presentation (High/Medium/Low)
4. Supporting evidence mentioned (if any)

Return your analysis in this JSON format:
```
{{
    "analysis_certainty": "High/Medium/Low",
    "core_claims": [
        {{
            "claim": "exact statement from article",
            "type": "Statistical/Causal/Predictive/Historical/Other",
            "confidence_level": "High/Medium/Low",
            "evidence_provided": "description of supporting evidence or 'None'",
            "verifiability": "Easy/Moderate/Difficult"
        }}
    ],
    "claim_summary": "Brief overview of main claims",
    "claim_count": 0
}}
```

Focus on verifiable, concrete claims rather than opinions or general statements.
"""
    
    @staticmethod
    def language_analysis_prompt(article_text: str) -> str:
        return f"""
You are a linguistic expert analyzing news article tone and language patterns.

Article to analyze:
{article_text}

Analyze the language and tone of this article:

1. Overall tone (objective/subjective/emotional/neutral)
2. Language intensity (measured/inflammatory/neutral)
3. Certainty indicators (hedging language vs absolute statements)
4. Emotional appeals vs logical reasoning
5. Loaded language examples

Return your analysis in this JSON format:
```
{{
    "analysis_certainty": "High/Medium/Low",
    "overall_tone": "objective/subjective/emotional/neutral",
    "language_intensity": "measured/inflammatory/neutral",
    "certainty_level": "high/medium/low",
    "reasoning_type": "logical/emotional/mixed",
    "loaded_language_examples": [
        {{
            "phrase": "specific phrase",
            "type": "positive/negative/neutral bias",
            "impact": "description of effect"
        }}
    ],
    "hedging_language": ["examples of uncertain language"],
    "absolute_statements": ["examples of definitive claims"],
    "emotional_indicators": ["words/phrases that appeal to emotion"]
}}
```
"""
    
    @staticmethod
    def bias_detection_prompt(article_text: str) -> str:
        return f"""
You are a critical thinking expert specializing in media bias detection.

Article to analyze:
{article_text}

Analyze this article for potential bias indicators and red flags:

1. **Language Bias**: Loaded/emotional language, unqualified superlatives
2. **Structural Bias**: Cherry-picked data, missing context, unbalanced sources
3. **Logical Fallacies**: Ad hominem, strawman, false dichotomies
4. **Source Issues**: Anonymous sources, conflicts of interest, lack of expert perspectives

Return your analysis in this JSON format:
```
{{
    "analysis_certainty": "High/Medium/Low",
    "bias_risk_level": "LOW/MEDIUM/HIGH",
    "red_flags": [
        {{
            "category": "Language/Structural/Logical/Source",
            "issue": "specific problem identified",
            "example": "quote from article",
            "severity": "Minor/Moderate/Major",
            "explanation": "why this is problematic"
        }}
    ],
    "missing_perspectives": ["what viewpoints are absent"],
    "source_quality": {{
        "expert_sources": 0,
        "anonymous_sources": 0,
        "potential_conflicts": ["any conflicts identified"]
    }},
    "overall_balance": "Balanced/Somewhat biased/Heavily biased"
}}
```

Provide specific examples with quotes and explain why each is problematic.
"""
    
    @staticmethod
    def verification_questions_prompt(article_text: str, claims: List[str]) -> str:
        # Handle the case where claims might be empty or contain dicts
        if isinstance(claims, list) and claims:
            if isinstance(claims[0], dict):
                claims_text = "\n".join([f"- {claim.get('claim', str(claim))}" for claim in claims])
            else:
                claims_text = "\n".join([f"- {str(claim)}" for claim in claims])
        else:
            claims_text = "No specific claims provided"
        
        return f"""
You are a fact-checking expert creating verification questions.

Article: {article_text}

Key Claims:
{claims_text}

Generate specific, actionable questions that would help verify the main claims in this article.

Return your questions in this JSON format:
```
{{
    "verification_questions": [
        {{
            "question": "specific question to verify claim",
            "claim_related": "which claim this verifies",
            "verification_method": "Statistical check/Source verification/Expert consultation/Data analysis",
            "difficulty": "Easy/Moderate/Difficult",
            "suggested_sources": ["specific sources to check"]
        }}
    ],
    "quick_checks": ["simple facts that can be quickly verified"],
    "expert_consultation_needed": ["complex claims requiring expert analysis"],
    "data_sources_to_check": ["specific databases or sources to consult"]
}}
```

Focus on creating practical, actionable verification steps.
"""
    
    @staticmethod
    def entity_extraction_prompt(article_text: str) -> str:
        return f"""
You are an information analyst extracting key entities for research.

Article to analyze:
{article_text}

Extract and categorize key entities that would benefit from additional research:

Return your analysis in this JSON format:
```
{{
    "people": [
        {{
            "name": "person's name",
            "role": "their relevance to the story",
            "credibility_factors": ["factors affecting their reliability"],
            "research_priority": "High/Medium/Low"
        }}
    ],
    "organizations": [
        {{
            "name": "organization name",
            "type": "government/corporate/non-profit/academic/etc.",
            "relevance": "how they relate to the story",
            "potential_bias": "any known bias or agenda"
        }}
    ],
    "key_terms": ["important technical or specialized terms"],
    "locations": ["relevant places mentioned"],
    "dates_events": ["significant dates or events referenced"],
    "research_priorities": {{
        "high_priority": ["entities requiring immediate fact-checking"],
        "background_research": ["entities worth understanding better"]
    }}
}}
```
"""
    
    @staticmethod
    def counter_argument_prompt(claims: List[str], language_analysis: Dict) -> str:
        # Handle both dict and string claims safely
        if isinstance(claims, list) and claims:
            if isinstance(claims[0], dict):
                claims_text = "\n".join([f"- {claim.get('claim', str(claim))}" for claim in claims])
            else:
                claims_text = "\n".join([f"- {str(claim)}" for claim in claims])
        else:
            claims_text = "No specific claims provided"
        
        # Safely extract tone information
        overall_tone = language_analysis.get('overall_tone', 'Unknown') if isinstance(language_analysis, dict) else 'Unknown'
        
        return f"""
You are an intellectual devil's advocate providing balanced perspective.

Original Claims:
{claims_text}

Article Tone: {overall_tone}

Generate thoughtful counter-arguments or alternative perspectives for the main claims.

Consider:
1. What opposing evidence might exist?
2. What alternative interpretations are possible?
3. What questions would a skeptic raise?
4. What might critics of this position argue?

Return your analysis in this JSON format:
```
{{
    "counter_arguments": [
        {{
            "original_claim": "claim being countered",
            "counter_perspective": "alternative viewpoint",
            "supporting_reasoning": "logical basis for counter-argument",
            "evidence_type": "what kind of evidence would support this view",
            "strength": "Strong/Moderate/Weak"
        }}
    ],
    "alternative_interpretations": [
        "different ways to interpret the main points"
    ],
    "skeptical_questions": [
        "questions a critical thinker would ask"
    ],
    "balance_assessment": "How balanced or one-sided is the original article"
}}
```

Be intellectually honest - don't create strawman counter-arguments.
Focus on legitimate alternative viewpoints that reasonable people might hold.
"""
    
    @staticmethod
    def overall_assessment_prompt(analysis_results: Dict[str, Any]) -> str:
        # Extract key information safely
        claims_info = analysis_results.get('claims', {})
        language_info = analysis_results.get('language_analysis', {})
        red_flags_info = analysis_results.get('red_flags', {})
        entities_info = analysis_results.get('entities', {})
        
        # Create summary of analysis for context
        claims_count = len(claims_info.get('core_claims', [])) if 'core_claims' in claims_info else 0
        red_flags_count = len(red_flags_info.get('red_flags', [])) if 'red_flags' in red_flags_info else 0
        people_count = len(entities_info.get('people', [])) if 'people' in entities_info else 0
        orgs_count = len(entities_info.get('organizations', [])) if 'organizations' in entities_info else 0
        
        analysis_summary = f"""
Claims Analysis: {claims_info.get('claim_summary', 'No summary available')} ({claims_count} claims identified)
Language Tone: {language_info.get('overall_tone', 'Unknown')}
Language Intensity: {language_info.get('language_intensity', 'Unknown')}
Bias Risk Level: {red_flags_info.get('bias_risk_level', 'Unknown')}
Red Flags Count: {red_flags_count} issues identified
Key Entities: {people_count + orgs_count} entities identified
Overall Balance: {red_flags_info.get('overall_balance', 'Unknown')}
"""
        
        return f"""
You are a media literacy expert providing an overall credibility assessment.

Based on the complete analysis:
{analysis_summary}

Provide a comprehensive credibility assessment based on:
- Quality and verifiability of claims
- Language bias and tone
- Presence of red flags
- Source quality and balance
- Overall journalistic standards

Return your assessment in this JSON format:
```
{{
    "credibility_score": {{
        "value": 75,
        "reasoning": "Explain how you arrived at this score based on the scoring criteria."
    }},
    "credibility_level": "Very High/High/Medium/Low/Very Low",
    "key_strengths": ["positive aspects of the article"],
    "key_concerns": ["main issues identified"],
    "recommendation": "How should readers approach this article",
    "fact_check_priority": "High/Medium/Low - urgency of fact-checking",
    "reader_guidance": {{
        "trust_level": "High/Medium/Low",
        "verification_needed": "Yes/No",
        "additional_sources": "Should readers seek other perspectives?"
    }},
    "summary": "Brief overall assessment for readers"
}}
```

**Scoring Criteria (100 points total):**
- **Claims & Evidence (35 points):** How verifiable, well-supported, and precise are the claims?
- **Sourcing & Balance (30 points):** Are diverse, high-quality sources used? Are alternative views represented?
- **Language & Tone (25 points):** Is the language objective and the tone neutral?
- **Structure & Fairness (10 points):** Does the article avoid structural bias like cherry-picking or misleading headlines?

Your `credibility_score.reasoning` must explicitly reference these criteria and the analysis summary.
"""


